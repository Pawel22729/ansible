#/usr/bin/python3

"""
Run Docker vault first:
  1. docker run --cap-add=IPC_LOCK -e 'VAULT_DEV_ROOT_TOKEN_ID=myroot' -e 'VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200' -p 8200:8200 vault
  2. export VAULT_ADDR and VAULT_TOKEN || overwrite them below

  Usaga:
    python3 vault.py --put --path 'pablo' --key 'pass' --value 'secretpass'
    python3 vault.py --get --path 'pablo' --key 'pass'
    python3 vault.py --patch --path 'pablo' --key 'pass' --value 'xxx'
"""

import hvac
import os
import argparse

config = {
  'vault_addr': os.environ['VAULT_ADDR'],
  'vault_token': os.environ['VAULT_TOKEN']
}

def vault_create_cli():
  try:
    cli = hvac.Client(
        url=config['vault_addr'],
        token=config['vault_token']
    )
    return cli
  except Exception as e:
    print("Vault client init failed with:", e)  

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
  return resp

def vault_patch(path, key, val):
  cli = vault_create_cli()
  resp = cli.secrets.kv.patch(
    path=path,
    secret={key: val}
  )
  return resp


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Vault argument parser')
  parser.add_argument('--put', action='store_true')
  parser.add_argument('--get', action='store_true')
  parser.add_argument('--patch', action='store_true')
  parser.add_argument('--path')
  parser.add_argument('--key')
  parser.add_argument('--value')
  parser.add_argument('--version', default=1)
  args = parser.parse_args()

  if args.put:
    resp = vault_put(
      path=args.path,
      key=args.key,
      val=args.value
    )
  elif args.get:
    resp = vault_get(
      path=args.path,
      key=args.key,
      version=args.version
    )
  elif args.patch:
    resp = vault_patch(
      path=args.path,
      key=args.key,
      val=args.value
    )

    print(resp)