
import os
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from cement.utils import fs
from tinydb import TinyDB
from .core.exc import WiError
from .controllers.base import Base
from .controllers.secrets import Secrets



# configuration defaults
CONFIG = init_defaults('wi')
CONFIG['wi']['db_file'] = '~/.wi/db.json'
CONFIG['wi']['foo'] = 'bar'

def extend_tinydb(app):
    db_file = app.config.get('wi', 'db_file')
    
    # ensure that we expand the full path
    db_file = fs.abspath(db_file)
    app.log.info('tinydb database file is: %s' % db_file)
    
    # ensure our parent directory exists
    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    app.extend('db', TinyDB(db_file))


class Wi(App):
    """Wi primary application."""

    class Meta:
        label = 'wi'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            Secrets
        ]

        # register hooks
        hooks = [
            ('post_setup', extend_tinydb),
        ]


class WiTest(TestApp,Wi):
    """A sub-class of Wi that is better suited for testing."""

    class Meta:
        label = 'wi'


def main():
    with Wi() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except WiError as e:
            print('WiError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
