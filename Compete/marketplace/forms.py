from decimal import Decimal

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import CTFEntry, HostedCTF, HostedChallenge


class CompetitionForm(forms.ModelForm):
    starts_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S"],
    )
    ends_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S"],
    )

    class Meta:
        model = HostedCTF
        fields = (
            "title",
            "summary",
            "description",
            "category",
            "entry_fee",
            "status",
            "starts_at",
            "ends_at",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields["status"].choices = [
                (HostedCTF.STATUS_DRAFT, "Draft"),
            ]
            self.fields["status"].initial = HostedCTF.STATUS_DRAFT

    def clean_entry_fee(self):
        fee = self.cleaned_data["entry_fee"]
        if fee < 0:
            raise ValidationError("Entry fee cannot be negative.")
        maximum = Decimal(getattr(settings, "MAX_ENTRY_FEE", "500.00"))
        if fee > maximum:
            raise ValidationError(f"Entry fee cannot be more than ${maximum}.")
        if fee > 0 and fee < Decimal("0.50"):
            raise ValidationError("Paid entries must be at least $0.50 so the card charge can clear.")
        return fee.quantize(Decimal("0.01"))

    def clean(self):
        cleaned = super().clean()
        starts = cleaned.get("starts_at")
        ends = cleaned.get("ends_at")
        if starts and ends and ends <= starts:
            self.add_error("ends_at", "End time must be after the start time.")

        status = cleaned.get("status")
        if status == HostedCTF.STATUS_OPEN:
            has_challenges = self.instance.pk and self.instance.challenges.exists()
            if not has_challenges:
                self.add_error(
                    "status",
                    "Add at least one challenge, then set the competition to Open.",
                )

        fee = cleaned.get("entry_fee")
        if (
            self.instance.pk
            and fee is not None
            and fee != self.instance.entry_fee
            and self.instance.entries.filter(
                status=CTFEntry.STATUS_PAID,
                gross_amount__gt=0,
            ).exists()
        ):
            self.add_error("entry_fee", "The entry fee is locked after a player has paid.")
        return cleaned


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = HostedChallenge
        fields = ("title", "description", "category", "difficulty", "points", "flag")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
            "flag": forms.TextInput(attrs={"autocomplete": "off"}),
        }

    def clean_points(self):
        points = self.cleaned_data["points"]
        if points < 1 or points > 10000:
            raise ValidationError("Points must be between 1 and 10000.")
        return points

    def clean_flag(self):
        flag = (self.cleaned_data.get("flag") or "").strip()
        if len(flag) < 4:
            raise ValidationError("Flag must be at least 4 characters.")
        if len(flag) > 200:
            raise ValidationError("Flag is too long.")
        return flag


class FlagSubmitForm(forms.Form):
    flag = forms.CharField(max_length=200, strip=True)


class PayoutForm(forms.Form):
    amount = forms.DecimalField(min_value=Decimal("1.00"), max_digits=8, decimal_places=2)
    note = forms.CharField(max_length=240, required=False)
