import hmac
import json
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Count, Max, Q, Sum
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import ChallengeForm, CompetitionForm, FlagSubmitForm, PayoutForm
from .models import CTFEntry, FlagSubmission, HostedCTF, HostedChallenge, LedgerLine, PayoutRequest
from .services import (
    commission_percent,
    create_checkout_session,
    host_available,
    host_earned,
    mark_entry_paid,
    platform_commission_total,
    quote_entry,
    retrieve_checkout_session,
    session_confirms_entry,
    stripe_configured,
    verify_stripe_signature,
)


def _unique_slug(title):
    base = (slugify(title) or "ctf")[:140]
    slug = base
    number = 2
    while HostedCTF.objects.filter(slug=slug).exists():
        suffix = f"-{number}"
        slug = f"{base[:160 - len(suffix)]}{suffix}"
        number += 1
    return slug


def _paid_entry(ctf, user):
    if not user.is_authenticated:
        return None
    return CTFEntry.objects.filter(
        ctf=ctf,
        player=user,
        status=CTFEntry.STATUS_PAID,
    ).first()


def _can_view_challenge_body(ctf, user):
    if not user.is_authenticated:
        return False
    if ctf.owner_id == user.id:
        return True
    return _paid_entry(ctf, user) is not None


def ctf_list(request):
    status = request.GET.get("status", "open")
    if status not in (HostedCTF.STATUS_OPEN, HostedCTF.STATUS_CLOSED, "all"):
        status = HostedCTF.STATUS_OPEN
    queryset = HostedCTF.objects.exclude(status=HostedCTF.STATUS_DRAFT).select_related("owner")
    if status != "all":
        queryset = queryset.filter(status=status)
    query = (request.GET.get("q") or "").strip()
    if query:
        queryset = queryset.filter(Q(title__icontains=query) | Q(summary__icontains=query))
    competitions = queryset.annotate(
        challenge_count=Count("challenges", distinct=True),
        player_count=Count(
            "entries",
            filter=Q(entries__status=CTFEntry.STATUS_PAID),
            distinct=True,
        ),
    )
    return render(
        request,
        "marketplace/ctf_list.html",
        {
            "competitions": competitions,
            "status": status,
            "query": query,
            "commission_percent": commission_percent(),
        },
    )


def ctf_detail(request, slug):
    ctf = get_object_or_404(
        HostedCTF.objects.select_related("owner"),
        slug=slug,
    )
    if ctf.status == HostedCTF.STATUS_DRAFT and not (
        request.user.is_authenticated and request.user.id == ctf.owner_id
    ):
        return HttpResponseForbidden("This competition is still a draft.")

    entry = None
    if request.user.is_authenticated:
        entry = CTFEntry.objects.filter(ctf=ctf, player=request.user).first()
    can_play = _can_view_challenge_body(ctf, request.user)
    challenges = list(ctf.challenges.all())
    solved_ids = set()
    if request.user.is_authenticated and can_play:
        solved_ids = set(
            FlagSubmission.objects.filter(
                challenge__ctf=ctf,
                player=request.user,
                is_correct=True,
            ).values_list("challenge_id", flat=True)
        )
    quote = quote_entry(ctf)
    return render(
        request,
        "marketplace/ctf_detail.html",
        {
            "ctf": ctf,
            "challenges": challenges,
            "solved_ids": solved_ids,
            "entry": entry,
            "can_play": can_play,
            "is_owner": request.user.is_authenticated and request.user.id == ctf.owner_id,
            "quote": quote,
            "stripe_ready": stripe_configured(),
            "test_payments": settings.DEBUG and not stripe_configured(),
            "player_count": ctf.entries.filter(status=CTFEntry.STATUS_PAID).count(),
        },
    )


@login_required
def ctf_create(request):
    if request.method == "POST":
        form = CompetitionForm(request.POST)
        if form.is_valid():
            ctf = form.save(commit=False)
            ctf.owner = request.user
            ctf.slug = _unique_slug(ctf.title)
            ctf.status = HostedCTF.STATUS_DRAFT
            ctf.save()
            messages.success(request, "Competition saved as a draft. Add challenges, then open it.")
            return redirect("hosted_ctf_challenge_create", slug=ctf.slug)
    else:
        form = CompetitionForm()
    return render(
        request,
        "marketplace/ctf_form.html",
        {
            "form": form,
            "commission_percent": commission_percent(),
            "mode": "create",
        },
    )


@login_required
def ctf_edit(request, slug):
    ctf = get_object_or_404(HostedCTF, slug=slug, owner=request.user)
    if request.method == "POST":
        form = CompetitionForm(request.POST, instance=ctf)
        if form.is_valid():
            form.save()
            messages.success(request, "Competition updated.")
            return redirect("hosted_ctf_detail", slug=ctf.slug)
    else:
        form = CompetitionForm(instance=ctf)
    return render(
        request,
        "marketplace/ctf_form.html",
        {
            "form": form,
            "ctf": ctf,
            "commission_percent": commission_percent(),
            "mode": "edit",
        },
    )


@login_required
def my_ctfs(request):
    competitions = (
        HostedCTF.objects.filter(owner=request.user)
        .annotate(
            challenge_count=Count("challenges", distinct=True),
            player_count=Count(
                "entries",
                filter=Q(entries__status=CTFEntry.STATUS_PAID),
                distinct=True,
            ),
            gross=Sum("entries__gross_amount", filter=Q(entries__status=CTFEntry.STATUS_PAID)),
            net=Sum("entries__host_amount", filter=Q(entries__status=CTFEntry.STATUS_PAID)),
        )
        .order_by("-created_at")
    )
    return render(
        request,
        "marketplace/my_ctfs.html",
        {
            "competitions": competitions,
            "available": host_available(request.user),
        },
    )


@login_required
@require_POST
def ctf_join(request, slug):
    ctf = get_object_or_404(HostedCTF, slug=slug)
    if ctf.owner_id == request.user.id:
        messages.info(request, "You host this competition, so you already have access. No entry fee.")
        return redirect("hosted_ctf_detail", slug=ctf.slug)
    if not ctf.is_accepting_entries():
        messages.error(request, "This competition is not accepting entries right now.")
        return redirect("hosted_ctf_detail", slug=ctf.slug)

    existing = CTFEntry.objects.filter(ctf=ctf, player=request.user).first()
    if existing and existing.status == CTFEntry.STATUS_PAID:
        messages.info(request, "You already entered this competition.")
        return redirect("hosted_ctf_detail", slug=ctf.slug)

    quote = quote_entry(ctf)
    if existing:
        entry = existing
        entry.gross_amount = quote["gross"]
        entry.commission_percent = quote["percent"]
        entry.commission_amount = quote["commission"]
        entry.host_amount = quote["host_net"]
        entry.status = CTFEntry.STATUS_PENDING
        entry.save()
    else:
        entry = CTFEntry.objects.create(
            ctf=ctf,
            player=request.user,
            status=CTFEntry.STATUS_PENDING,
            gross_amount=quote["gross"],
            commission_percent=quote["percent"],
            commission_amount=quote["commission"],
            host_amount=quote["host_net"],
        )

    if quote["gross"] == 0:
        mark_entry_paid(entry)
        messages.success(request, "You're in. This competition is free.")
        return redirect("hosted_ctf_detail", slug=ctf.slug)

    if stripe_configured():
        success = request.build_absolute_uri(
            reverse("hosted_ctf_entry_success", args=[ctf.slug])
        )
        cancel = request.build_absolute_uri(
            reverse("hosted_ctf_entry_cancel", args=[ctf.slug])
        )
        try:
            url = create_checkout_session(
                entry,
                success_url=success + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=cancel,
            )
        except Exception:
            messages.error(request, "Could not start checkout. Try again in a moment.")
            return redirect("hosted_ctf_detail", slug=ctf.slug)
        return redirect(url)

    if settings.DEBUG:
        messages.warning(
            request,
            "Stripe is not configured. Use the test payment button to simulate a paid entry.",
        )
        return redirect("hosted_ctf_detail", slug=ctf.slug)

    entry.status = CTFEntry.STATUS_FAILED
    entry.save(update_fields=["status"])
    messages.error(
        request,
        "Paid entries are not available until Stripe is configured on the server.",
    )
    return redirect("hosted_ctf_detail", slug=ctf.slug)


@login_required
@require_POST
def ctf_test_pay(request, slug):
    if not settings.DEBUG or stripe_configured():
        return HttpResponseForbidden("Test payments are disabled.")
    ctf = get_object_or_404(HostedCTF, slug=slug)
    entry = get_object_or_404(
        CTFEntry,
        ctf=ctf,
        player=request.user,
        status=CTFEntry.STATUS_PENDING,
    )
    mark_entry_paid(entry, session_id="debug-test")
    messages.success(request, "Test payment recorded. The host balance and platform commission were updated.")
    return redirect("hosted_ctf_detail", slug=ctf.slug)


@login_required
def entry_success(request, slug):
    ctf = get_object_or_404(HostedCTF, slug=slug)
    entry = get_object_or_404(CTFEntry, ctf=ctf, player=request.user)
    if entry.status != CTFEntry.STATUS_PAID:
        session_id = request.GET.get("session_id", "")
        if not session_id or not stripe_configured():
            messages.error(request, "Payment was not confirmed.")
            return redirect("hosted_ctf_detail", slug=ctf.slug)
        try:
            session = retrieve_checkout_session(session_id)
        except Exception:
            messages.error(request, "Could not confirm the payment with Stripe.")
            return redirect("hosted_ctf_detail", slug=ctf.slug)
        if not session_confirms_entry(session, entry):
            messages.error(request, "That payment does not match this entry.")
            return redirect("hosted_ctf_detail", slug=ctf.slug)
        mark_entry_paid(entry, session_id=session.get("id", session_id))
    messages.success(request, "Payment received. You can start the challenges.")
    return redirect("hosted_ctf_detail", slug=ctf.slug)


@login_required
def entry_cancel(request, slug):
    messages.info(request, "Checkout cancelled. You have not been charged.")
    return redirect("hosted_ctf_detail", slug=slug)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", "")
    payload = request.body
    if not verify_stripe_signature(payload, request.headers.get("Stripe-Signature", ""), secret):
        return HttpResponse(status=400)
    try:
        event = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return HttpResponse(status=400)
    if event.get("type") in ("checkout.session.completed", "checkout.session.async_payment_succeeded"):
        session = event.get("data", {}).get("object", {})
        metadata = session.get("metadata") or {}
        entry_id = metadata.get("entry_id")
        if entry_id and session.get("payment_status") == "paid":
            entry = CTFEntry.objects.filter(pk=entry_id).first()
            if entry and session_confirms_entry(session, entry):
                mark_entry_paid(entry, session_id=session.get("id", ""))
    return HttpResponse(status=200)


@login_required
def challenge_create(request, slug):
    ctf = get_object_or_404(HostedCTF, slug=slug, owner=request.user)
    if request.method == "POST":
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.ctf = ctf
            challenge.save()
            messages.success(request, "Challenge added.")
            return redirect("hosted_ctf_detail", slug=ctf.slug)
    else:
        form = ChallengeForm()
    return render(
        request,
        "marketplace/challenge_form.html",
        {"form": form, "ctf": ctf, "mode": "create"},
    )


@login_required
def challenge_edit(request, slug, challenge_id):
    ctf = get_object_or_404(HostedCTF, slug=slug, owner=request.user)
    challenge = get_object_or_404(HostedChallenge, pk=challenge_id, ctf=ctf)
    if request.method == "POST":
        form = ChallengeForm(request.POST, instance=challenge)
        if form.is_valid():
            form.save()
            messages.success(request, "Challenge updated.")
            return redirect("hosted_ctf_detail", slug=ctf.slug)
    else:
        form = ChallengeForm(instance=challenge)
    return render(
        request,
        "marketplace/challenge_form.html",
        {"form": form, "ctf": ctf, "challenge": challenge, "mode": "edit"},
    )


@login_required
@require_POST
def challenge_delete(request, slug, challenge_id):
    ctf = get_object_or_404(HostedCTF, slug=slug, owner=request.user)
    challenge = get_object_or_404(HostedChallenge, pk=challenge_id, ctf=ctf)
    if ctf.status == HostedCTF.STATUS_OPEN and ctf.challenges.count() <= 1:
        messages.error(request, "An open competition needs at least one challenge.")
        return redirect("hosted_ctf_detail", slug=ctf.slug)
    challenge.delete()
    messages.success(request, "Challenge removed.")
    return redirect("hosted_ctf_detail", slug=ctf.slug)


def challenge_detail(request, slug, challenge_id):
    ctf = get_object_or_404(HostedCTF.objects.select_related("owner"), slug=slug)
    if ctf.status == HostedCTF.STATUS_DRAFT and not (
        request.user.is_authenticated and request.user.id == ctf.owner_id
    ):
        return HttpResponseForbidden("This competition is still a draft.")
    challenge = get_object_or_404(HostedChallenge, pk=challenge_id, ctf=ctf)
    can_play = _can_view_challenge_body(ctf, request.user)
    solved = False
    if request.user.is_authenticated:
        solved = FlagSubmission.objects.filter(
            challenge=challenge,
            player=request.user,
            is_correct=True,
        ).exists()
    return render(
        request,
        "marketplace/challenge_detail.html",
        {
            "ctf": ctf,
            "challenge": challenge,
            "can_play": can_play,
            "is_owner": request.user.is_authenticated and request.user.id == ctf.owner_id,
            "solved": solved,
            "form": FlagSubmitForm(),
        },
    )


@login_required
@require_POST
def challenge_submit(request, slug, challenge_id):
    ctf = get_object_or_404(HostedCTF, slug=slug)
    challenge = get_object_or_404(HostedChallenge, pk=challenge_id, ctf=ctf)
    if ctf.owner_id == request.user.id:
        messages.error(request, "Hosts don't score their own flags.")
        return redirect("hosted_challenge_detail", slug=slug, challenge_id=challenge.id)
    if not _paid_entry(ctf, request.user):
        messages.error(request, "Enter the competition before submitting a flag.")
        return redirect("hosted_ctf_detail", slug=slug)
    if not ctf.is_accepting_solves():
        messages.error(request, "This competition is closed to new solves.")
        return redirect("hosted_challenge_detail", slug=slug, challenge_id=challenge.id)

    form = FlagSubmitForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Enter a flag.")
        return redirect("hosted_challenge_detail", slug=slug, challenge_id=challenge.id)

    window_start = timezone.now() - timedelta(minutes=10)
    wrong_recent = FlagSubmission.objects.filter(
        challenge=challenge,
        player=request.user,
        is_correct=False,
        submitted_at__gte=window_start,
    ).count()
    if wrong_recent >= 15:
        messages.error(request, "Too many wrong attempts. Wait a few minutes and try again.")
        return redirect("hosted_challenge_detail", slug=slug, challenge_id=challenge.id)

    submitted = form.cleaned_data["flag"]
    expected = challenge.flag.strip()
    correct = hmac.compare_digest(submitted.encode("utf-8"), expected.encode("utf-8"))

    try:
        with transaction.atomic():
            already = FlagSubmission.objects.select_for_update().filter(
                challenge=challenge,
                player=request.user,
                is_correct=True,
            ).exists()
            if already:
                messages.info(request, "You already solved this challenge.")
                return redirect("hosted_challenge_detail", slug=slug, challenge_id=challenge.id)
            FlagSubmission.objects.create(
                challenge=challenge,
                player=request.user,
                is_correct=correct,
                points_awarded=challenge.points if correct else 0,
            )
    except IntegrityError:
        messages.info(request, "You already solved this challenge.")
        return redirect("hosted_challenge_detail", slug=slug, challenge_id=challenge.id)

    if correct:
        messages.success(request, f"Correct. {challenge.points} points.")
    else:
        messages.error(request, "Incorrect flag.")
    return redirect("hosted_challenge_detail", slug=slug, challenge_id=challenge.id)


def scoreboard(request, slug):
    ctf = get_object_or_404(HostedCTF, slug=slug)
    if ctf.status == HostedCTF.STATUS_DRAFT and not (
        request.user.is_authenticated and request.user.id == ctf.owner_id
    ):
        return HttpResponseForbidden("This competition is still a draft.")

    totals = {
        row["player_id"]: row
        for row in FlagSubmission.objects.filter(challenge__ctf=ctf, is_correct=True)
        .values("player_id")
        .annotate(
            points=Sum("points_awarded"),
            solves=Count("id"),
            last_solve=Max("submitted_at"),
        )
    }
    entries = (
        CTFEntry.objects.filter(ctf=ctf, status=CTFEntry.STATUS_PAID)
        .select_related("player")
        .order_by("player__username")
    )
    ranked = []
    for entry in entries:
        stats = totals.get(entry.player_id, {})
        ranked.append(
            {
                "username": entry.player.username,
                "points": stats.get("points") or 0,
                "solves": stats.get("solves") or 0,
                "last_solve": stats.get("last_solve"),
            }
        )
    ranked.sort(key=lambda row: (-row["points"], row["last_solve"] or timezone.now(), row["username"]))
    for index, row in enumerate(ranked, start=1):
        row["rank"] = index
    return render(
        request,
        "marketplace/scoreboard.html",
        {"ctf": ctf, "board": ranked},
    )


@login_required
def earnings(request):
    lines = (
        LedgerLine.objects.filter(user=request.user, kind=LedgerLine.KIND_HOST)
        .select_related("ctf", "entry", "entry__player")
        .order_by("-created_at")[:50]
    )
    payouts = PayoutRequest.objects.filter(host=request.user)[:20]
    commission_taken = (
        LedgerLine.objects.filter(
            kind=LedgerLine.KIND_COMMISSION,
            ctf__owner=request.user,
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )
    if request.method == "POST":
        form = PayoutForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            with transaction.atomic():
                available = host_available(request.user)
                if amount > available:
                    form.add_error("amount", f"You can request up to ${available}.")
                else:
                    PayoutRequest.objects.create(
                        host=request.user,
                        amount=amount,
                        note=form.cleaned_data.get("note") or "",
                    )
                    messages.success(request, "Payout requested. Compete will pay this out off-platform.")
                    return redirect("hosted_ctf_earnings")
    else:
        form = PayoutForm()
    return render(
        request,
        "marketplace/earnings.html",
        {
            "lines": lines,
            "payouts": payouts,
            "earned": host_earned(request.user),
            "available": host_available(request.user),
            "commission_taken": commission_taken,
            "form": form,
            "commission_percent": commission_percent(),
        },
    )


@login_required
def commissions(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Staff only.")
    recent = (
        CTFEntry.objects.filter(status=CTFEntry.STATUS_PAID, gross_amount__gt=0)
        .select_related("ctf", "ctf__owner", "player")
        .order_by("-paid_at")[:100]
    )
    totals = CTFEntry.objects.filter(status=CTFEntry.STATUS_PAID).aggregate(
        gross=Sum("gross_amount"),
        host=Sum("host_amount"),
    )
    pending_payouts = PayoutRequest.objects.filter(status=PayoutRequest.STATUS_PENDING).select_related(
        "host"
    )
    return render(
        request,
        "marketplace/commissions.html",
        {
            "commission_total": platform_commission_total(),
            "gross_total": totals["gross"] or 0,
            "host_total": totals["host"] or 0,
            "recent": recent,
            "pending_payouts": pending_payouts,
            "commission_percent": commission_percent(),
        },
    )


@login_required
@require_POST
def payout_mark_paid(request, payout_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Staff only.")
    payout = get_object_or_404(PayoutRequest, pk=payout_id, status=PayoutRequest.STATUS_PENDING)
    action = request.POST.get("action")
    if action == "reject":
        payout.status = PayoutRequest.STATUS_REJECTED
        payout.resolved_at = timezone.now()
        payout.save(update_fields=["status", "resolved_at"])
        messages.success(request, "Payout rejected. The balance is available to the host again.")
        return redirect("hosted_ctf_commissions")
    with transaction.atomic():
        payout.status = PayoutRequest.STATUS_PAID
        payout.resolved_at = timezone.now()
        payout.save(update_fields=["status", "resolved_at"])
        LedgerLine.objects.create(
            user=payout.host,
            kind=LedgerLine.KIND_PAYOUT,
            amount=payout.amount,
            payout=payout,
            note="Payout marked paid by staff",
        )
    messages.success(request, "Payout marked paid.")
    return redirect("hosted_ctf_commissions")
