
import os
from cement import Controller, ex, shell
from cement.utils.version import get_version_banner
from ..core.version import get_version

from tinydb import Query

VERSION_BANNER = """
Wi will allow storing and using a set of environment variables based on current directory %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'Wi will allow storing and using a set of environment variables based on current directory'

        # text displayed at the bottom of --help output
        epilog = 'Usage: wi command1 --foo bar'

        # controller level arguments. ex: 'wi --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()


    @ex(
        help='example sub command1',

        # sub-command level arguments. ex: 'wi command1 --foo bar'
        arguments=[
            ### add a sample foo option under subcommand namespace
            ( [ '-f', '--foo' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store',
                'dest' : 'foo' } ),
        ],
    )
    def command1(self):
        """Example sub-command."""

        data = {
            'foo' : 'bar',
        }

        ### do something with arguments
        if self.app.pargs.foo is not None:
            data['foo'] = self.app.pargs.foo

        self.app.render(data, 'command1.jinja2')


    @ex(
        help="Run a command with the environment variables set for the current directory",
        arguments=[
            ( ['command'], {'help': 'Command to be run', 'action': 'store', 'nargs': '*'})
        ]
    )
    def run(self):
        secrets = self.app.db.search(Query().directory == os.getcwd())
        command = self.app.pargs.command

        for secret in secrets:
            env_var = f"{secret['key']}={secret['value']}"
            command.insert(0, env_var)

        code = shell.cmd(' '.join(command), capture=False)
