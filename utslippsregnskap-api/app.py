from flask import Flask
import pandas as pd

app = Flask('utslippsregnskap')

df = pd.read_parquet('../data/utslippsdata_med_type.pq')
df = df.astype(
    {'versjon': 'category', 'type': 'category', 'enhet': 'category'}
)

@app.after_request
def allow_cors(response):
    print('response', response)
    response.headers.access_control_allow_origin = '*'

@app.get("/utslipp/jordbruk")
def utslipp_jordbruk():
    next_df = df.loc[
        (df.norskkilde_nivaa1_navn == 'Jordbruk') &
        (df.versjon == '2019-11-01') &
        (df.type == 'POP')
    ].groupby(
        ['aar', 'versjon'],
        as_index=False,
        observed=True
    ).agg({ 'utslipp': sum }).to_dict()
    return next_df

