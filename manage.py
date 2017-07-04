# coding: utf-8

import threading
import logging
my_log = logging.getLogger("__threads__")


class MyThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(MyThread, self).__init__(group, target, name, args, kwargs, verbose)
        # import prctl
        self.the_name = getattr(target, "func_name", target.__name__) if target else self.__class__.__name__
        my_log.debug("{} start".format(self.the_name))
        # prctl.set_proctitle("{} with {}, {}".format(name, args, kwargs))

    def __del__(self, *args, **kwargs):
        my_log.debug("{} done".format(self.the_name))
        super(MyThread, self).__init__(self, *args, **kwargs)


threading.Thread = MyThread


from flask import Flask

from twisted.internet import reactor
from flask.ext.script import Manager

from core.config import setup_config, config
from core.utils.init import home_dir, useradd
from core.logger import setup_logging

setup_config('%s/config.py' % home_dir())

from core.utils import change_user_vmmaster

setup_logging(
    log_type=getattr(config, "LOG_TYPE", None),
    log_level=getattr(config, "LOG_LEVEL", None)
)
app = Flask(__name__)
manager = Manager(app)
log = logging.getLogger(__name__)


@manager.command
def runserver():
    """
    Run server
    """
    from vmmaster.server import VMMasterServer
    VMMasterServer(reactor, config.PORT).run()


@manager.command
def cleanup():
    """
    Run cleanup
    """
    from vmmaster import cleanup
    cleanup.run()


@manager.command
def init():
    """
    Initialize application
    """
    log.info('Initialize application')
    useradd()
    change_user_vmmaster()
    exit(0)


@manager.command
def migrations():
    """
    Database migrations
    """
    from migrations import migrations
    migrations.run(config.DATABASE)


@manager.command
def version():
    """
    Show application version
    """
    import versioneer

    versioneer.VCS = 'git'
    versioneer.versionfile_source = 'vmmaster/_version.py'
    versioneer.versionfile_build = 'vmmaster/_version.py'
    versioneer.tag_prefix = ''  # tags are like 0.1.0
    versioneer.parentdir_prefix = 'vmmaster-'  # dirname like 'myproject-0.1.0'

    return versioneer.get_version()


if __name__ == '__main__':
    manager.run()
