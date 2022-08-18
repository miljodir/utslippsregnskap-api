from flask import Flask
import pandas as pd

app = Flask("utslippsregnskap")
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)


df = pd.read_parquet("../data/utslippsdata_med_type.pq")
df = df.astype({"versjon": "category", "type": "category", "enhet": "category"})


@app.after_request
def security_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response


@app.get("/utslipp/jordbruk")
def utslipp_jordbruk():
    next_df = (
        df.loc[(df.norskkilde_nivaa1_navn == "Jordbruk") & (df.versjon == "2019-11-01") & (df.type == "POP")]
        .groupby(["aar", "versjon"], as_index=False, observed=True)
        .agg({"utslipp": sum})
        .to_dict(orient="list")
    )
    return next_df

if __name__ == '__main__':
    app.run(debug=True)