#/usr/bin/python3

"""
Run Docker vault first:
  1. docker run --cap-add=IPC_LOCK -e 'VAULT_DEV_ROOT_TOKEN_ID=myroot' -e 'VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200' -p 8200:8200 vault
  2. export VAULT_ADDR and VAULT_TOKEN || overwrite them below
"""

import hvac
import os
import argparse

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


def vault_get(path, key, version=1):
  cli = vault_create_cli()
  resp = cli.secrets.kv.v2.read_secret_version(
    path=path,
    version=version
  )
  return resp['data']['data'][key]

def vault_patch(path, key, val):
  cli = vault_create_cli()
  resp = cli.secrets.kv.patch(
    path=path,
    secret={key: val}
  )
  return resp


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Vault argument parser')
  parser.add_argument('--put', name='vault_put')
  parser.add_argument('--get', name='vault_get')
  parser.add_argument('--path', name='secret_path')
  parser.add_argument('--key', name='vault_key')
  parser.add_argument('--value', name='vault_value')
  parser.add_argument('--version', name='secret_version', default=1)
  args = parser.parse_args()

  if args.vault_put and not args.vault_get:
    resp = vault_put(
      path=args.secret_path,
      key=args.args.key,
      val=args.vault_value
    )
  elif args.vault_get and not vault_put:
    resp = vault_get(
      path=args.path,
      key=args.key,
      version=args.secret_version
    )  
# resp = vault_put(path='pablo2', k='environment', v='prod')
# print(resp)

#resp2 = vault_get(path='pablo2', key='environment', version=5)
#print(resp2)
 
#resp3 = vault_patch(path='pablo2', key='environment', val='new_prod')
#print(resp3)