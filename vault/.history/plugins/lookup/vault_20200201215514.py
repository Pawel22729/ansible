#!/usr/bin/python3

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from ansible.module_utils._text import to_text
import hvac
import os

display = Display()

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

def vault_get(path, key, version=1):
  cli = vault_create_cli()
  resp = cli.secrets.kv.v2.read_secret_version(
    path=path,
    version=version
  )
  return resp

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        ret = []
        for term in terms:
            display.debug("Vault lookup term: %s" % term)
            try:
                resp = vault_get(path='pablo3', key=term)
                resp = 
                ret.append('XXX')
            except AnsibleParserError:
                raise AnsibleError()

        return ret
