import hashlib
import hmac
import time
from decimal import Decimal, ROUND_HALF_UP

import requests
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .models import CTFEntry, LedgerLine, PayoutRequest


def commission_percent():
    try:
        raw = int(getattr(settings, "PLATFORM_COMMISSION_PERCENT", 15))
    except (TypeError, ValueError):
        raw = 15
    return max(0, min(raw, 50))


def split_fee(gross, percent=None):
    """Return (commission, host_net) in dollars. They always sum to gross."""
    amount = Decimal(gross).quantize(Decimal("0.01"))
    if amount < 0:
        raise ValueError("Entry fee cannot be negative.")
    rate_percent = commission_percent() if percent is None else int(percent)
    rate_percent = max(0, min(rate_percent, 50))
    rate = Decimal(rate_percent) / Decimal(100)
    commission = (amount * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if commission > amount:
        commission = amount
    host_net = (amount - commission).quantize(Decimal("0.01"))
    return commission, host_net


def quote_entry(ctf):
    gross = Decimal(ctf.entry_fee).quantize(Decimal("0.01"))
    percent = commission_percent()
    commission, host_net = split_fee(gross, percent)
    return {
        "gross": gross,
        "percent": percent,
        "commission": commission,
        "host_net": host_net,
    }


def mark_entry_paid(entry, session_id=""):
    """Record a paid entry once and write the commission + host ledger lines.

    The entry row is locked, so a webhook and the success page cannot double-pay.
    """
    with transaction.atomic():
        locked = CTFEntry.objects.select_for_update().get(pk=entry.pk)
        if locked.status == CTFEntry.STATUS_PAID:
            return locked
        locked.status = CTFEntry.STATUS_PAID
        locked.paid_at = timezone.now()
        if session_id:
            locked.stripe_session_id = session_id[:255]
        locked.save(update_fields=["status", "paid_at", "stripe_session_id"])

        if locked.gross_amount > 0:
            LedgerLine.objects.create(
                entry=locked,
                ctf=locked.ctf,
                user=None,
                kind=LedgerLine.KIND_COMMISSION,
                amount=locked.commission_amount,
                note=f"{locked.commission_percent}% commission on {locked.ctf.title}",
            )
            LedgerLine.objects.create(
                entry=locked,
                ctf=locked.ctf,
                user=locked.ctf.owner,
                kind=LedgerLine.KIND_HOST,
                amount=locked.host_amount,
                note=f"Entry fee from {locked.player.username}",
            )
        return locked


def stripe_configured():
    return bool(getattr(settings, "STRIPE_SECRET_KEY", ""))


def create_checkout_session(entry, success_url, cancel_url):
    amount_cents = int((entry.gross_amount * 100).to_integral_value())
    if amount_cents < 50:
        raise ValueError("Stripe requires a charge of at least $0.50.")
    data = {
        "mode": "payment",
        "success_url": success_url,
        "cancel_url": cancel_url,
        "client_reference_id": str(entry.pk),
        "metadata[entry_id]": str(entry.pk),
        "metadata[user_id]": str(entry.player_id),
        "metadata[ctf_id]": str(entry.ctf_id),
        "line_items[0][quantity]": 1,
        "line_items[0][price_data][currency]": "usd",
        "line_items[0][price_data][unit_amount]": amount_cents,
        "line_items[0][price_data][product_data][name]": f"CTF entry: {entry.ctf.title}"[:120],
        "line_items[0][price_data][product_data][description]": (
            f"Includes a {entry.commission_percent}% Compete platform commission."
        )[:500],
    }
    response = requests.post(
        "https://api.stripe.com/v1/checkout/sessions",
        data=data,
        auth=(settings.STRIPE_SECRET_KEY, ""),
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    entry.stripe_session_id = payload.get("id", "")[:255]
    entry.save(update_fields=["stripe_session_id"])
    return payload["url"]


def retrieve_checkout_session(session_id):
    response = requests.get(
        f"https://api.stripe.com/v1/checkout/sessions/{session_id}",
        auth=(settings.STRIPE_SECRET_KEY, ""),
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def verify_stripe_signature(payload, header, secret, tolerance=300):
    if not header or not secret:
        return False
    parts = {}
    for item in header.split(","):
        key, _, value = item.partition("=")
        parts.setdefault(key, []).append(value)
    timestamps = parts.get("t") or []
    signatures = parts.get("v1") or []
    if not timestamps or not signatures:
        return False
    try:
        timestamp = int(timestamps[0])
    except ValueError:
        return False
    if abs(time.time() - timestamp) > tolerance:
        return False
    signed = f"{timestamps[0]}.".encode("utf-8") + payload
    expected = hmac.new(secret.encode("utf-8"), signed, hashlib.sha256).hexdigest()
    return any(hmac.compare_digest(expected, signature) for signature in signatures)


def session_confirms_entry(session, entry):
    metadata = session.get("metadata") or {}
    return (
        session.get("payment_status") == "paid"
        and str(metadata.get("entry_id")) == str(entry.pk)
        and str(metadata.get("user_id")) == str(entry.player_id)
        and str(metadata.get("ctf_id")) == str(entry.ctf_id)
    )


def host_earned(user):
    from django.db.models import Sum

    total = LedgerLine.objects.filter(user=user, kind=LedgerLine.KIND_HOST).aggregate(
        total=Sum("amount")
    )["total"]
    return total or Decimal("0.00")


def host_reserved(user):
    """Pending and paid payouts reduce what the host can request next."""
    from django.db.models import Sum

    total = PayoutRequest.objects.filter(
        host=user,
        status__in=[PayoutRequest.STATUS_PENDING, PayoutRequest.STATUS_PAID],
    ).aggregate(total=Sum("amount"))["total"]
    return total or Decimal("0.00")


def host_available(user):
    available = (host_earned(user) - host_reserved(user)).quantize(Decimal("0.01"))
    if available < 0:
        return Decimal("0.00")
    return available


def platform_commission_total():
    from django.db.models import Sum

    total = LedgerLine.objects.filter(kind=LedgerLine.KIND_COMMISSION).aggregate(
        total=Sum("amount")
    )["total"]
    return total or Decimal("0.00")
