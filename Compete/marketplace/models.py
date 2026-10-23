from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Q


class HostedCTF(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_OPEN, "Open"),
        (STATUS_CLOSED, "Closed"),
    ]

    CATEGORY_CHOICES = [
        ("web", "Web"),
        ("crypto", "Crypto"),
        ("pwn", "Pwn"),
        ("rev", "Reverse"),
        ("forensics", "Forensics"),
        ("osint", "OSINT"),
        ("misc", "Misc"),
        ("mixed", "Mixed"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hosted_ctfs",
    )
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)
    summary = models.CharField(max_length=240)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="mixed")
    entry_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def is_accepting_entries(self):
        from django.utils import timezone

        if self.status != self.STATUS_OPEN:
            return False
        now = timezone.now()
        if self.starts_at and now < self.starts_at:
            return False
        if self.ends_at and now > self.ends_at:
            return False
        return True

    def is_accepting_solves(self):
        from django.utils import timezone

        if self.status != self.STATUS_OPEN:
            return False
        if self.ends_at and timezone.now() > self.ends_at:
            return False
        return True


class HostedChallenge(models.Model):
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]

    ctf = models.ForeignKey(HostedCTF, on_delete=models.CASCADE, related_name="challenges")
    title = models.CharField(max_length=140)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=HostedCTF.CATEGORY_CHOICES, default="misc")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="Easy")
    points = models.PositiveIntegerField(default=100)
    flag = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class CTFEntry(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_FAILED, "Failed"),
    ]

    ctf = models.ForeignKey(HostedCTF, on_delete=models.CASCADE, related_name="entries")
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ctf_entries",
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    gross_amount = models.DecimalField(max_digits=8, decimal_places=2)
    commission_percent = models.PositiveSmallIntegerField()
    commission_amount = models.DecimalField(max_digits=8, decimal_places=2)
    host_amount = models.DecimalField(max_digits=8, decimal_places=2)
    stripe_session_id = models.CharField(max_length=255, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["ctf", "player"], name="unique_ctf_entry"),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.player} → {self.ctf} ({self.status})"


class LedgerLine(models.Model):
    KIND_COMMISSION = "commission"
    KIND_HOST = "host_earning"
    KIND_PAYOUT = "host_payout"
    KIND_CHOICES = [
        (KIND_COMMISSION, "Platform commission"),
        (KIND_HOST, "Host earning"),
        (KIND_PAYOUT, "Host payout"),
    ]

    entry = models.ForeignKey(
        CTFEntry,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="ledger_lines",
    )
    ctf = models.ForeignKey(
        HostedCTF,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="ledger_lines",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="ledger_lines",
    )
    payout = models.ForeignKey(
        "PayoutRequest",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="ledger_lines",
    )
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    note = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["entry"],
                condition=Q(kind="commission"),
                name="one_commission_line_per_entry",
            ),
            models.UniqueConstraint(
                fields=["entry"],
                condition=Q(kind="host_earning"),
                name="one_host_line_per_entry",
            ),
        ]

    def __str__(self):
        return f"{self.kind} {self.amount}"


class PayoutRequest(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_REJECTED, "Rejected"),
    ]

    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payout_requests",
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    note = models.CharField(max_length=240, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-requested_at"]

    def __str__(self):
        return f"{self.host} {self.amount} ({self.status})"


class FlagSubmission(models.Model):
    challenge = models.ForeignKey(
        HostedChallenge,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="flag_submissions",
    )
    is_correct = models.BooleanField(default=False)
    points_awarded = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["challenge", "player"],
                condition=Q(is_correct=True),
                name="one_correct_solve_per_player",
            ),
        ]
        indexes = [
            models.Index(fields=["challenge", "player", "submitted_at"]),
        ]

    def __str__(self):
        return f"{self.player} {self.challenge} correct={self.is_correct}"
