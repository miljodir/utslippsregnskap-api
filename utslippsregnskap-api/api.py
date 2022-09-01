import time
from flask import jsonify, request, session, make_response, url_for
from flask.blueprints import Blueprint

import data


def create_api(df, storage: data.DatalakeStorage):
    nivå_navn = df.loc[:, df.columns[df.columns.str.endswith("nivå")]].drop_duplicates()
    jordbruk_navn = '7-Jordbruk'

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
        nivå_filter = request.args.get("nivaa")
        jordbruk = df.loc[(df.kategori_nivå1 == jordbruk_navn) & (df.versjon == "2019-11-01")]
        if komponent_filter:
            komponent_filter = komponent_filter.split(",")
            jordbruk = jordbruk.loc[(jordbruk.komponent.isin(komponent_filter))]
        if nivå_filter:
            nivå_filter = nivå_filter.split(",")
            jordbruk = jordbruk.loc[(jordbruk.kategori_nivå3.isin(nivå_filter))]
        jordbruk = jordbruk.groupby(["år", "versjon"], as_index=False, observed=True)

        return jordbruk.agg({"utslipp": sum}).rename(
            columns={'år': 'aar'}
        ).to_dict(orient="list")

    @api.get("/jordbruk/nivaa3")
    def utslipp_jordbruk_nivaa3():
        nivå3 = (df.loc[(df.kategori_nivå1 == jordbruk_navn)].kategori_nivå3.unique()).to_list()
        return jsonify(dict({"nivaa3": nivå3}))

    @api.get("/jordbruk/komponenter")
    def utslipp_jordbruk_komponenter():
        komponenter = (df.loc[(df.kategori_nivå1 == jordbruk_navn)].komponent.unique()).to_list()
        return jsonify(dict({"komponenter": komponenter}))

    @api.get("/nivaa")
    def utslipp_nivaa_navn():
        records = nivå_navn.to_dict(orient="records")
        tree = data.to_tree(records.values())
        pretty_tree = data.pretty_tree(tree, "kategori", "nivaa")
        return jsonify(pretty_tree)

    @api.post("/upload/<file_name>/<int:sheet_number>")
    def store_excel_as_pq(file_name: str, sheet_number: int = 0):
        # sjekk at bruker har lov
        df = data.excel_to_df(request.files['file'], sheet_number)
        storage.save_parquet(file_name.replace('.xlsx', '.pq'), df)
        return {}

    return api
