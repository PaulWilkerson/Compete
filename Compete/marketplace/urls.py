from django.urls import path

from . import views

urlpatterns = [
    path("", views.ctf_list, name="hosted_ctf_list"),
    path("new/", views.ctf_create, name="hosted_ctf_create"),
    path("mine/", views.my_ctfs, name="hosted_ctf_mine"),
    path("earnings/", views.earnings, name="hosted_ctf_earnings"),
    path("commissions/", views.commissions, name="hosted_ctf_commissions"),
    path("stripe/webhook/", views.stripe_webhook, name="hosted_ctf_stripe_webhook"),
    path("payouts/<int:payout_id>/resolve/", views.payout_mark_paid, name="hosted_ctf_payout_resolve"),
    path("<slug:slug>/", views.ctf_detail, name="hosted_ctf_detail"),
    path("<slug:slug>/edit/", views.ctf_edit, name="hosted_ctf_edit"),
    path("<slug:slug>/join/", views.ctf_join, name="hosted_ctf_join"),
    path("<slug:slug>/test-pay/", views.ctf_test_pay, name="hosted_ctf_test_pay"),
    path("<slug:slug>/entry/success/", views.entry_success, name="hosted_ctf_entry_success"),
    path("<slug:slug>/entry/cancel/", views.entry_cancel, name="hosted_ctf_entry_cancel"),
    path("<slug:slug>/scoreboard/", views.scoreboard, name="hosted_ctf_scoreboard"),
    path("<slug:slug>/challenges/new/", views.challenge_create, name="hosted_ctf_challenge_create"),
    path(
        "<slug:slug>/challenges/<int:challenge_id>/",
        views.challenge_detail,
        name="hosted_challenge_detail",
    ),
    path(
        "<slug:slug>/challenges/<int:challenge_id>/edit/",
        views.challenge_edit,
        name="hosted_ctf_challenge_edit",
    ),
    path(
        "<slug:slug>/challenges/<int:challenge_id>/delete/",
        views.challenge_delete,
        name="hosted_ctf_challenge_delete",
    ),
    path(
        "<slug:slug>/challenges/<int:challenge_id>/submit/",
        views.challenge_submit,
        name="hosted_ctf_submit",
    ),
]
