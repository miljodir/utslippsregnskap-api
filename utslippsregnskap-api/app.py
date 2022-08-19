import pandas as pd
from flask import Flask, jsonify, request

app = Flask("utslippsregnskap")
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)


df = pd.read_parquet("../data/utslippsdata_med_type.pq")
df = df.astype({"versjon": "category", "type": "category", "enhet": "category"})
nivaa_navn = df.loc[:, df.columns[df.columns.str.endswith("navn")]].drop_duplicates()


@app.after_request
def security_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers[
        "Strict-Transport-Security"
    ] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response


@app.get("/utslipp/jordbruk")
def utslipp_jordbruk():
    komponent_filter = request.args.get("komponenter")
    jordbruk = df.loc[
        (df.norskkilde_nivaa1_navn == "Jordbruk") & (df.versjon == "2019-11-01")
    ]
    if komponent_filter:
        komponent_filter = komponent_filter.split(',')
        jordbruk = jordbruk.loc[(jordbruk.komponent.isin(komponent_filter))]
    jordbruk = jordbruk.groupby(["aar", "versjon"], as_index=False, observed=True)

    return jordbruk.agg({"utslipp": sum}).to_dict(orient="list")


@app.get("/utslipp/jordbruk/nivaa3")
def utslipp_jordbruk_nivaa3():
    nivaa3 = (
        df.loc[
            (df.norskkilde_nivaa1_navn == "Jordbruk")
        ].norskkilde_nivaa3_navn.unique()
    ).to_list()
    return jsonify(dict({"nivaa3": nivaa3}))


@app.get("/utslipp/jordbruk/komponenter")
def utslipp_jordbruk_komponenter():
    komponenter = (
        df.loc[(df.norskkilde_nivaa1_navn == "Jordbruk")].komponent.unique()
    ).to_list()
    return jsonify(dict({"komponenter": komponenter}))


@app.get("/utslipp/nivaa")
def utslipp_nivaa_navn():
    tree = {}
    for r in nivaa_navn.to_dict(orient="records"):
        current_node = tree
        for column, value in r.items():
            if not isinstance(value, str):
                break
            if value not in current_node:
                current_node[value] = {}
            current_node = current_node[value]

    def pretty(tree):
        values = []
        for key, children in tree.items():
            if not children:
                values.append({"kategori": key})
            else:
                values.append({"kategori": key, "nivaa": pretty(children)})
        return values

    return jsonify(pretty(tree))


if __name__ == "__main__":
    app.run(debug=True)
