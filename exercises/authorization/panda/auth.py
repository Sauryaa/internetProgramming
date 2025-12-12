#!/usr/bin/env python3
"""
PandAuth authentication

@author:
@version: 2025.12
"""

import datetime
import json

import requests
from flask import Blueprint, current_app, redirect, request, url_for
from flask_login import login_required, login_user, logout_user

from . import client, db, login_manager
from .models import User

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.get("/login")
def login():
    """Log in"""

    google_provider_cfg = current_app.config["GOOGLE_CONFIG"]
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for("auth.callback", _external=True, _scheme="https"),
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@auth.route("/login/callback")
def callback():
    """Google callback"""

    code = request.args.get("code")
    if not code:
        return redirect(url_for("main.index"))

    google_provider_cfg = current_app.config["GOOGLE_CONFIG"]
    try:
        token_endpoint = google_provider_cfg["token_endpoint"]
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(client.client_id, current_app.config["GOOGLE_CLIENT_SECRET"]),
            timeout=5,
        )
        client.parse_request_body_response(json.dumps(token_response.json()))

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body, timeout=5).json()
    except requests.RequestException:
        return redirect(url_for("main.index"))

    unique_id = userinfo_response.get("sub")
    users_email = userinfo_response.get("email")
    picture = userinfo_response.get("picture")
    users_name = userinfo_response.get("given_name", userinfo_response.get("name", ""))

    user = db.session.query(User).filter_by(id=unique_id).first()
    if not user:
        user = User(
            id=unique_id,
            email=users_email,
            name=users_name,
            picture=picture,
            registered=datetime.datetime.now(),
        )
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for("main.index"))


@auth.route("/logout")
@login_required
def logout():
    """Log out"""
    logout_user()
    return redirect(url_for("main.index"))


@login_manager.user_loader
def load_user(user_id):
    """User loader"""
    return db.session.query(User).filter_by(id=user_id).first()
