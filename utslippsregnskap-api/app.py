import os
import tempfile

import azure.identity
import azure.keyvault.secrets
import pyarrowfs_adlgen2
from flask import Flask
from flask_session import Session

from api import create_api
from data import DatalakeStorage
from login_api import create_login_api

app = Flask("utslippsregnskap")
with open("/dev/urandom", mode="rb") as urandom:
    secret_key = urandom.read(32)

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_TYPE="filesystem",
    SESSION_FILE_DIR=tempfile.mkdtemp(),
    SECRET_KEY=secret_key,
)

Session(app)

kv_name = os.environ["KV_NAME"]
file_location = os.environ["DATA_PATH"]
container, file_location = file_location.split("/")[0], "/".join(file_location.split("/")[1:])

storage_account = os.environ["STORAGE_ACCOUNT"]
credential = azure.identity.DefaultAzureCredential()

secrets_client = azure.keyvault.secrets.SecretClient(f"https://{kv_name}.vault.azure.net", credential)
filesystem = pyarrowfs_adlgen2.FilesystemHandler.from_account_name(storage_account, container, credential)
data_lake = DatalakeStorage(filesystem)
df = data_lake.load_parquet(file_location)

client_id = secrets_client.get_secret("client-id").value
tenant_id = secrets_client.get_secret("tenant-id").value
client_secret = secrets_client.get_secret("client-secret").value

app.register_blueprint(create_api(df, data_lake), url_prefix="/utslipp")
app.register_blueprint(create_login_api(tenant_id, client_id, client_secret))


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
