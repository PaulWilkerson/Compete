from django.contrib import admin

from .models import CTFEntry, FlagSubmission, HostedChallenge, HostedCTF, LedgerLine, PayoutRequest


class ChallengeInline(admin.TabularInline):
    model = HostedChallenge
    extra = 0
    fields = ("title", "category", "difficulty", "points", "flag")


@admin.register(HostedCTF)
class HostedCTFAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "status", "entry_fee", "category", "created_at")
    list_filter = ("status", "category")
    search_fields = ("title", "owner__username", "slug")
    inlines = [ChallengeInline]


@admin.register(CTFEntry)
class CTFEntryAdmin(admin.ModelAdmin):
    list_display = (
        "ctf",
        "player",
        "status",
        "gross_amount",
        "commission_amount",
        "host_amount",
        "paid_at",
    )
    list_filter = ("status",)
    search_fields = ("player__username", "ctf__title", "stripe_session_id")


@admin.register(LedgerLine)
class LedgerLineAdmin(admin.ModelAdmin):
    list_display = ("kind", "amount", "user", "ctf", "created_at")
    list_filter = ("kind",)


@admin.register(PayoutRequest)
class PayoutRequestAdmin(admin.ModelAdmin):
    list_display = ("host", "amount", "status", "requested_at", "resolved_at")
    list_filter = ("status",)


@admin.register(FlagSubmission)
class FlagSubmissionAdmin(admin.ModelAdmin):
    list_display = ("player", "challenge", "is_correct", "points_awarded", "submitted_at")
    list_filter = ("is_correct",)
