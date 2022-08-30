import os
import time
import uuid
import msal
from flask import session, redirect, url_for, request
from flask.blueprints import Blueprint


def create_login_api(tenant_id, client_id, client_secret):
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    auth = msal.ConfidentialClientApplication(client_id, client_secret, authority)

    login_api = Blueprint("login-api", __name__)

    @login_api.get("/login")
    def login():
        if "user" in session:
            user_exp = session.get("user")["exp"]
            if time.time() < user_exp:
                return redirect("/")
        if "state" not in session:
            session["state"] = str(uuid.uuid4())
        auth_url = auth.get_authorization_request_url(
            scopes=[], state=session["state"], redirect_uri=url_for("login-api.logged_in", _external=True)
        )
        return redirect(auth_url)

    @login_api.get("/logged-in")
    def logged_in():
        if request.args.get("state") != session["state"]:
            return redirect("/")
        if request.args.get("error"):
            raise RuntimeError("Got error from Microsoft")
        code = request.args.get("code")
        if code:
            result = auth.acquire_token_by_authorization_code(
                code=code, scopes=[], redirect_uri=url_for("login-api.logged_in", _external=True)
            )
            if "error" in result:
                raise RuntimeError(
                    f"Got error when acquiring token from MS {result.get('error')} {result.get('error_description')}"
                )
            session["user"] = result["id_token_claims"]
            return redirect("/")
        else:
            raise RuntimeError("Got no code when redirected from MS")

    @login_api.get("/logout")
    def logout():
        session.clear()
        return redirect(
            f'{authority}/oauth2/v2.0/logout?post_logout_redirect_uri={url_for("static", _external=True, filename="index.html")}'
        )

    return login_api
