#/usr/bin/python3

import hvac
cli = hvac.Client()

cli.secrets.kv.v2.create_or_update_secret(
    path='hvac',
    secret=dict(pssst='this is secret'),
)
