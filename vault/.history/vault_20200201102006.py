#/usr/bin/python3

import hvac
import os

cli = hvac.Client()

config = {
  'vault_addr': os.environ['VAULT_ADDR'],
  'vault_token': env.['VAULT_TOKE']
}

cli.secrets.kv.v2.create_or_update_secret(
    path='hvac',
    secret=dict(pssst='this is secret'),
)
