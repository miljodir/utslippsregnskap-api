from flask import g, jsonify, request
from flask.blueprints import Blueprint

import data

api = Blueprint("api", __name__)


@api.get("/jordbruk")
def utslipp_jordbruk():
    komponent_filter = request.args.get("komponenter")
    nivaa_filter = request.args.get("nivaa")
    jordbruk = g.df.loc[(g.df.norskkilde_nivaa1_navn == "Jordbruk") & (g.df.versjon == "2019-11-01")]
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
    nivaa3 = (g.df.loc[(g.df.norskkilde_nivaa1_navn == "Jordbruk")].norskkilde_nivaa3_navn.unique()).to_list()
    return jsonify(dict({"nivaa3": nivaa3}))


@api.get("/jordbruk/komponenter")
def utslipp_jordbruk_komponenter():
    komponenter = (g.df.loc[(g.df.norskkilde_nivaa1_navn == "Jordbruk")].komponent.unique()).to_list()
    return jsonify(dict({"komponenter": komponenter}))


@api.get("/nivaa")
def utslipp_nivaa_navn():
    records = g.nivaa_navn.to_dict(orient="records")
    tree = data.to_tree(records.values())
    pretty_tree = data.pretty_tree(tree, "kategori", "nivaa")
    return jsonify(pretty_tree)
