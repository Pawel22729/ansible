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

class LookupModule(LookupBase):

    def vault_create_cli(self):
        try:
            cli = hvac.Client(
                url=config['vault_addr'],
                token=config['vault_token']
            )
            return cli
        except Exception as e:
            print("Vault client init failed with:", e)  

    def vault_get(self, path, key, version=1):
        cli = self.vault_create_cli()
        resp = cli.secrets.kv.v2.read_secret_version(
            path=path,
            version=version
        )
        return resp

    def run(self, terms, variables=None, **kwargs):
        ret = []
        for term in terms:
            display.debug("Vault lookup term: %s" % term)
            try:
                resp = self.vault_get(path='pablo3', key=term)
                resp = to_text(resp)
                ret.append(resp)
            except AnsibleParserError:
                raise AnsibleError()

        return ret
