#/usr/bin/python3

"""
Run Docker vault first:
  1. docker run --cap-add=IPC_LOCK -e 'VAULT_DEV_ROOT_TOKEN_ID=myroot' -e 'VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200' -p 8200:8200 vault
  2. export VAULT_ADDR and VAULT_TOKEN || overwrite them below
"""

import hvac
import os

config = {
  'vault_addr': os.environ['VAULT_ADDR'],
  'vault_token': os.environ['VAULT_TOKEN']
}

path_create = "pablo"
secret_name = "pablo_secret"
secret_value = "secret 123"

def vault_create_cli():
  cli = hvac.Client(
      url=config['vault_addr'],
      token=config['vault_token']
    )
  return cli

def vault_put(path, key, val):
  cli = vault_create_cli()
  resp = cli.secrets.kv.v2.create_or_update_secret(
    path=path,
    secret={key: val},
  )
  return resp


def vault_get(path, key):
  cli = vault_create_cli()
  resp = cli.secrets.kv.v2.read_secret_version(
    path=path
  )
  return resp['data']['data'][key]


# resp = vault_put(path='pablo2', k='environment', v='prod')
# print(resp)

resp2 = vault_get(path='pablo2')
print(resp2['data']['data'])