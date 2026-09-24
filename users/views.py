from urllib.parse import urlencode
import secrets
from urllib.request import Request as UrlRequest, urlopen
import json

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from coffee.models import Reservation
from .forms import AvatarForm
from .models import UserProfile


def google_login(request):
    if not settings.GOOGLE_CLIENT_ID:
        return render(request, "users/google_setup.html", status=503)
    request.session["login_next"] = request.GET.get("next") or "/account/"
    request.session["google_oauth_state"] = secrets.token_urlsafe(32)
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "online",
        "prompt": "select_account",
        "state": request.session["google_oauth_state"],
    }
    return redirect("https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params))


def google_callback(request):
    code = request.GET.get("code")
    if request.GET.get("error"):
        return redirect("coffee:home")
    state = request.GET.get("state")
    expected_state = request.session.pop("google_oauth_state", None)
    if not code or not state or state != expected_state:
        return render(request, "users/google_error.html", {"message": "Invalid Google sign-in state. Please try again."}, status=400)

    token_body = urlencode({
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }).encode()

    try:
        token_request = UrlRequest(
            "https://oauth2.googleapis.com/token",
            data=token_body,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urlopen(token_request, timeout=10) as response:
            token_data = json.loads(response.read().decode("utf-8"))

        raw_id_token = token_data.get("id_token")
        if not raw_id_token:
            raise ValueError("Google did not return an ID token.")

        identity = id_token.verify_oauth2_token(
            raw_id_token, google_requests.Request(), settings.GOOGLE_CLIENT_ID
        )
        email = identity.get("email")
        if not email or not identity.get("sub"):
            raise ValueError("Google account information is incomplete.")
        if not identity.get("email_verified", False):
            raise ValueError("The Google email address is not verified.")

        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            base = (email.split("@")[0] or "google_user")[:120]
            username, counter = base, 1
            while User.objects.filter(username=username).exists():
                counter += 1
                suffix = f"_{counter}"
                username = f"{base[:120-len(suffix)]}{suffix}"
            user = User.objects.create(
                username=username,
                email=email,
                first_name=identity.get("given_name", ""),
                last_name=identity.get("family_name", ""),
            )
            user.set_unusable_password()
            user.save(update_fields=["password"])

        profile, _ = UserProfile.objects.get_or_create(user=user)
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect(request.session.pop("login_next", "/account/"))
    except Exception as exc:
        return render(request, "users/google_error.html", {"message": str(exc)}, status=400)


@require_http_methods(["GET"])
def account_status(request):
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False})
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return JsonResponse({
        "authenticated": True,
        "name": request.user.get_full_name() or request.user.username,
        "email": request.user.email,
        "avatar": profile.avatar.url if profile.avatar else "",
        "account_url": "/account/",
        "logout_url": "/logout/",
    })


def account(request):
    if not request.user.is_authenticated:
        request.session["login_next"] = "/account/"
        return redirect("users:google_login")
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    reservations = Reservation.objects.filter(user=request.user).order_by("-date", "-time")
    return render(request, "users/account.html", {
        "profile": profile,
        "reservations": reservations,
        "avatar_form": AvatarForm(instance=profile),
    })


@require_http_methods(["POST"])
def upload_avatar(request):
    if not request.user.is_authenticated:
        return redirect("users:google_login")
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    form = AvatarForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
        form.save()
    return redirect("users:account")


@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return redirect("coffee:home")
