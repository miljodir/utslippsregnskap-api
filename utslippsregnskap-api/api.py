import time
from flask import jsonify, request, session, make_response, url_for
from flask.blueprints import Blueprint

import data


def create_api(df):

    nivaa_navn = df.loc[:, df.columns[df.columns.str.endswith("navn")]].drop_duplicates()

    api = Blueprint("api", __name__)

    @api.before_request
    def check_logged_in():
        if "user" not in session:
            resp = make_response({"message": "Unauthorized"}, 401)
            resp.headers["Location"] = url_for("login-api.login", _external=True)
            return resp
        else:
            user_exp = session.get("user")["exp"]
            if time.time() >= user_exp:
                session.clear()
                resp = make_response({"message": "Session expired"}, 401)
                resp.headers["Location"] = url_for("login-api.login", _external=True)
                return resp

    @api.get("/jordbruk")
    def utslipp_jordbruk():
        komponent_filter = request.args.get("komponenter")
        nivaa_filter = request.args.get("nivaa")
        jordbruk = df.loc[(df.norskkilde_nivaa1_navn == "Jordbruk") & (df.versjon == "2019-11-01")]
        if komponent_filter:
            komponent_filter = komponent_filter.split(",")
            jordbruk = jordbruk.loc[(jordbruk.komponent.isin(komponent_filter))]
        if nivaa_filter:
            nivaa_filter = nivaa_filter.split(",")
            jordbruk = jordbruk.loc[(jordbruk.norskkilde_nivaa3_navn.isin(nivaa_filter))]
        jordbruk = jordbruk.groupby(["aar", "versjon"], as_index=False, observed=True)

        return jordbruk.agg({"utslipp": sum}).to_dict(orient="list")

    @api.get("/jordbruk/nivaa3")
    def utslipp_jordbruk_nivaa3():
        nivaa3 = (df.loc[(df.norskkilde_nivaa1_navn == "Jordbruk")].norskkilde_nivaa3_navn.unique()).to_list()
        return jsonify(dict({"nivaa3": nivaa3}))

    @api.get("/jordbruk/komponenter")
    def utslipp_jordbruk_komponenter():
        komponenter = (df.loc[(df.norskkilde_nivaa1_navn == "Jordbruk")].komponent.unique()).to_list()
        return jsonify(dict({"komponenter": komponenter}))

    @api.get("/nivaa")
    def utslipp_nivaa_navn():
        records = nivaa_navn.to_dict(orient="records")
        tree = data.to_tree(records.values())
        pretty_tree = data.pretty_tree(tree, "kategori", "nivaa")
        return jsonify(pretty_tree)

    return api
