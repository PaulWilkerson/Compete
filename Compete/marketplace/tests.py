import hashlib
import hmac
import json
import time
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import CTFEntry, FlagSubmission, HostedCTF, LedgerLine, PayoutRequest
from .services import mark_entry_paid, split_fee, verify_stripe_signature


def _open_ctf(owner, fee="0.00", title="Midnight Range"):
    ctf = HostedCTF.objects.create(
        owner=owner,
        title=title,
        slug=title.lower().replace(" ", "-"),
        summary="A short hosted event.",
        description="Find the flags.",
        entry_fee=Decimal(fee),
        status=HostedCTF.STATUS_OPEN,
    )
    ctf.challenges.create(
        title="Warmup",
        description="The flag is hidden in this sentence: flag{warmup}.",
        category="misc",
        difficulty="Easy",
        points=100,
        flag="flag{warmup}",
    )
    return ctf


@override_settings(SECURE_SSL_REDIRECT=False)
class SplitFeeTests(TestCase):
    def test_fifteen_percent_of_ten_dollars(self):
        commission, host_net = split_fee(Decimal("10.00"), 15)
        self.assertEqual(commission, Decimal("1.50"))
        self.assertEqual(host_net, Decimal("8.50"))
        self.assertEqual(commission + host_net, Decimal("10.00"))

    def test_rounding_never_exceeds_gross(self):
        commission, host_net = split_fee(Decimal("0.10"), 15)
        self.assertEqual(commission + host_net, Decimal("0.10"))
        self.assertGreaterEqual(host_net, Decimal("0.00"))

    def test_zero_fee(self):
        self.assertEqual(split_fee(Decimal("0.00"), 15), (Decimal("0.00"), Decimal("0.00")))

    def test_webhook_signature(self):
        payload = b'{"id":"evt_1"}'
        secret = "whsec_test"
        timestamp = str(int(time.time()))
        signed = f"{timestamp}.".encode() + payload
        signature = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
        header = f"t={timestamp},v1={signature}"
        self.assertTrue(verify_stripe_signature(payload, header, secret))
        self.assertFalse(verify_stripe_signature(payload, header, "other"))
        self.assertFalse(verify_stripe_signature(b"tampered", header, secret))


@override_settings(
    SECURE_SSL_REDIRECT=False,
    SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False,
    PLATFORM_COMMISSION_PERCENT=15,
    DEBUG=True,
    STRIPE_SECRET_KEY="",
    STRIPE_WEBHOOK_SECRET="whsec_test",
)
class HostedCompetitionTests(TestCase):
    def setUp(self):
        self.host = User.objects.create_user("host", "host@example.com", "host-pass-123")
        self.player = User.objects.create_user("player", "player@example.com", "player-pass-123")
        self.staff = User.objects.create_user(
            "staff",
            "staff@example.com",
            "staff-pass-123",
            is_staff=True,
        )
        self.client = Client()

    def test_free_entry_and_solve_are_scoped_to_the_competition(self):
        ctf = _open_ctf(self.host)
        self.client.login(username="player", password="player-pass-123")
        detail = self.client.get(reverse("hosted_challenge_detail", args=[ctf.slug, ctf.challenges.first().id]))
        self.assertNotContains(detail, "flag{warmup}")
        join = self.client.post(reverse("hosted_ctf_join", args=[ctf.slug]))
        self.assertEqual(join.status_code, 302)
        entry = CTFEntry.objects.get(player=self.player, ctf=ctf)
        self.assertEqual(entry.status, CTFEntry.STATUS_PAID)
        self.assertEqual(entry.gross_amount, Decimal("0.00"))
        self.assertFalse(LedgerLine.objects.exists())

        opened = self.client.get(reverse("hosted_challenge_detail", args=[ctf.slug, ctf.challenges.first().id]))
        self.assertContains(opened, "flag{warmup}")
        wrong = self.client.post(
            reverse("hosted_ctf_submit", args=[ctf.slug, ctf.challenges.first().id]),
            {"flag": "nope"},
        )
        self.assertEqual(wrong.status_code, 302)
        self.assertFalse(FlagSubmission.objects.get().is_correct)
        right = self.client.post(
            reverse("hosted_ctf_submit", args=[ctf.slug, ctf.challenges.first().id]),
            {"flag": "flag{warmup}"},
        )
        self.assertEqual(right.status_code, 302)
        self.assertEqual(FlagSubmission.objects.filter(is_correct=True).count(), 1)
        again = self.client.post(
            reverse("hosted_ctf_submit", args=[ctf.slug, ctf.challenges.first().id]),
            {"flag": "flag{warmup}"},
        )
        self.assertEqual(again.status_code, 302)
        self.assertEqual(FlagSubmission.objects.filter(is_correct=True).count(), 1)

        board = self.client.get(reverse("hosted_ctf_scoreboard", args=[ctf.slug]))
        self.assertContains(board, "player")
        self.assertContains(board, "100")

    def test_paid_entry_splits_commission_and_is_idempotent(self):
        ctf = _open_ctf(self.host, fee="10.00", title="Paid Cup")
        self.client.login(username="player", password="player-pass-123")
        self.client.post(reverse("hosted_ctf_join", args=[ctf.slug]))
        entry = CTFEntry.objects.get()
        self.assertEqual(entry.status, CTFEntry.STATUS_PENDING)
        self.assertEqual(entry.commission_amount, Decimal("1.50"))
        self.assertEqual(entry.host_amount, Decimal("8.50"))

        blocked = self.client.get(reverse("hosted_challenge_detail", args=[ctf.slug, ctf.challenges.first().id]))
        self.assertNotContains(blocked, "hidden in this sentence")

        paid = self.client.post(reverse("hosted_ctf_test_pay", args=[ctf.slug]))
        self.assertEqual(paid.status_code, 302)
        mark_entry_paid(entry, session_id="again")
        entry.refresh_from_db()
        self.assertEqual(entry.status, CTFEntry.STATUS_PAID)
        self.assertEqual(
            LedgerLine.objects.get(kind=LedgerLine.KIND_COMMISSION).amount,
            Decimal("1.50"),
        )
        self.assertEqual(
            LedgerLine.objects.get(kind=LedgerLine.KIND_HOST).amount,
            Decimal("8.50"),
        )
        self.assertEqual(LedgerLine.objects.filter(kind=LedgerLine.KIND_COMMISSION).count(), 1)

        self.client.login(username="host", password="host-pass-123")
        earnings = self.client.get(reverse("hosted_ctf_earnings"))
        self.assertContains(earnings, "8.50")
        self.client.post(reverse("hosted_ctf_earnings"), {"amount": "8.50", "note": "bank"})
        self.assertEqual(PayoutRequest.objects.get().amount, Decimal("8.50"))
        too_much = self.client.post(reverse("hosted_ctf_earnings"), {"amount": "1.00", "note": ""})
        self.assertEqual(too_much.status_code, 200)
        self.assertEqual(PayoutRequest.objects.count(), 1)

        self.client.login(username="player", password="player-pass-123")
        denied = self.client.get(reverse("hosted_ctf_commissions"))
        self.assertEqual(denied.status_code, 403)
        self.client.login(username="staff", password="staff-pass-123")
        page = self.client.get(reverse("hosted_ctf_commissions"))
        self.assertContains(page, "1.50")
        resolve = self.client.post(
            reverse("hosted_ctf_payout_resolve", args=[PayoutRequest.objects.get().id]),
            {"action": "pay"},
        )
        self.assertEqual(resolve.status_code, 302)
        self.assertEqual(PayoutRequest.objects.get().status, PayoutRequest.STATUS_PAID)

    def test_host_does_not_pay_to_enter_own_event(self):
        ctf = _open_ctf(self.host, fee="10.00", title="Own Event")
        self.client.login(username="host", password="host-pass-123")
        self.client.post(reverse("hosted_ctf_join", args=[ctf.slug]))
        self.assertFalse(CTFEntry.objects.exists())

    def test_webhook_marks_pending_entry_paid(self):
        ctf = _open_ctf(self.host, fee="20.00", title="Webhook Cup")
        commission, host_net = split_fee(Decimal("20.00"), 15)
        entry = CTFEntry.objects.create(
            ctf=ctf,
            player=self.player,
            gross_amount=Decimal("20.00"),
            commission_percent=15,
            commission_amount=commission,
            host_amount=host_net,
        )
        payload = json.dumps(
            {
                "type": "checkout.session.completed",
                "data": {
                    "object": {
                        "id": "cs_test_123",
                        "payment_status": "paid",
                        "metadata": {
                            "entry_id": str(entry.pk),
                            "user_id": str(self.player.id),
                            "ctf_id": str(ctf.id),
                        },
                    }
                },
            }
        ).encode()
        timestamp = str(int(time.time()))
        signature = hmac.new(
            b"whsec_test",
            f"{timestamp}.".encode() + payload,
            hashlib.sha256,
        ).hexdigest()
        response = self.client.post(
            reverse("hosted_ctf_stripe_webhook"),
            data=payload,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=f"t={timestamp},v1={signature}",
        )
        self.assertEqual(response.status_code, 200)
        entry.refresh_from_db()
        self.assertEqual(entry.status, CTFEntry.STATUS_PAID)
        self.assertEqual(LedgerLine.objects.filter(kind=LedgerLine.KIND_COMMISSION).count(), 1)

    def test_drafts_are_hidden_and_open_requires_a_challenge(self):
        self.client.login(username="host", password="host-pass-123")
        created = self.client.post(
            reverse("hosted_ctf_create"),
            {
                "title": "Unreleased",
                "summary": "Not yet",
                "description": "Draft body",
                "category": "web",
                "entry_fee": "5.00",
                "status": "draft",
            },
        )
        self.assertEqual(created.status_code, 302)
        ctf = HostedCTF.objects.get(title="Unreleased")
        self.assertEqual(ctf.status, HostedCTF.STATUS_DRAFT)
        self.client.logout()
        hidden = self.client.get(reverse("hosted_ctf_detail", args=[ctf.slug]))
        self.assertEqual(hidden.status_code, 403)
        listing = self.client.get(reverse("hosted_ctf_list"))
        self.assertNotContains(listing, "Unreleased")

        self.client.login(username="host", password="host-pass-123")
        opened = self.client.post(
            reverse("hosted_ctf_edit", args=[ctf.slug]),
            {
                "title": "Unreleased",
                "summary": "Not yet",
                "description": "Draft body",
                "category": "web",
                "entry_fee": "5.00",
                "status": "open",
            },
        )
        self.assertEqual(opened.status_code, 200)
        ctf.refresh_from_db()
        self.assertEqual(ctf.status, HostedCTF.STATUS_DRAFT)

    def test_aggregator_home_lists_open_competitions(self):
        ctf = _open_ctf(self.host, title="Visible Cup")
        ctf.created_at = timezone.now()
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Visible Cup")
        self.assertContains(response, "Hosted competitions")
