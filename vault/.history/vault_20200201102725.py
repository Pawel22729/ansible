#/usr/bin/python3

import hvac
import os

config = {
  'vault_addr': os.environ['VAULT_ADDR'],
  'vault_token': env.['VAULT_TOKE']
}

path_create = "pablo"
secret_create = "pablo secret"

cli = hvac.Client(
  url=config['vault_addr'],
  token=config['vault_token']
)
cli.secrets.kv.v2.create_or_update_secret(
    path=path_create,
    secret=dict(pssst='this is secret'),
)
