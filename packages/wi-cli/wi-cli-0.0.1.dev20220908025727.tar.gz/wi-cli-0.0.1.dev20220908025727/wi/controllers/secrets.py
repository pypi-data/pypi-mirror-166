import os
from cement import Controller, ex
from time import strftime
from tinydb import Query

class Secrets(Controller):
    class Meta:
        label = 'secrets'
        stacked_type = 'nested'
        stacked_on = 'base'

    def list_secrets(self):
        return self.app.db.search(Query().directory == os.getcwd())

    @ex(help='list secrets')
    def list(self):
        data = {}
        data['secrets'] = self.list_secrets()
        self.app.render(data, 'secrets/list.jinja2')
        
    @ex(help='add a secret',
        arguments=[
            ( 
                ['secret'], {'help': 'secret key and value in the format FOO=BAR', 'action': 'store' },
            )
        ],
    )
    def add(self):
        secret = self.app.pargs.secret
        now = strftime("%Y-%m-%d %H:%M:%S")
        directory = os.getcwd()

        self.app.log.info('creating secret')

        secret = secret.split("=")
        key = secret[0]
        value = secret[1]

        secret = {
            'timestamp': now,
            'key': key,
            'value': value,
            'directory': directory
        }

        self.app.db.insert(secret)

    @ex(help='delete a secret',
        arguments=[
            ( 
                ['secret_id'], {'help': 'secret id to delete', 'action': 'store' },
            )
        ],
    )
    def delete(self):
        id = int(self.app.pargs.secret_id)
        self.app.log.info('deleting secret id: %s' % id)
        self.app.db.remove(doc_ids=[id])
