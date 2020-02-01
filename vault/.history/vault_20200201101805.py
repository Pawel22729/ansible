#/usr/bin/python3

import hvac
cli = hvac.Client()

config = {
  'vault_addr': env.VAULT_ADDR,
  'vault_token': env.VAULT_TOKEN
}

cli.secrets.kv.v2.create_or_update_secret(
    path='hvac',
    secret=dict(pssst='this is secret'),
)
