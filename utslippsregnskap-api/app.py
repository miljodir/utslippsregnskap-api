import os
import pyarrowfs_adlgen2
import pandas as pd
import azure.identity
import azure.keyvault.secrets
from flask import Flask, g

from api import api

app = Flask("utslippsregnskap")
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
app.register_blueprint(api, url_prefix="/utslipp")


kv_name = os.environ['KV_NAME']
file_location = os.environ['DATA_PATH']
storage_account = os.environ['STORAGE_ACCOUNT']
credential = azure.identity.DefaultAzureCredential()

secrets_client = azure.keyvault.secrets.SecretClient(f'https://{kv_name}.vault.azure.net', credential)
filesystem = pyarrowfs_adlgen2.AccountHandler.from_account_name(storage_account, credential).to_fs()

client_id = secrets_client.get_secret('client-id').value
tenant_id = secrets_client.get_secret('tenant-id').value
client_secret = secrets_client.get_secret('client-secret').value

df = pd.read_parquet(file_location, filesystem=filesystem)
df = df.astype({"versjon": "category", "type": "category", "enhet": "category"})
nivaa_navn = df.loc[:, df.columns[df.columns.str.endswith("navn")]].drop_duplicates()


@app.before_request
def set_df_on_request_context():
    g.df = df
    g.nivaa_navn = nivaa_navn

@app.after_request
def security_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    # response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response


if __name__ == "__main__":
    app.run(debug=True)
