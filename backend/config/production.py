import os
import logging
import logging.config
import logging.handlers
from core.logger import setup_logging

log = logging.getLogger(__name__)

STATIC_FOLDERS = 'backend/static'

# Muffin
# ======

# PLUGINS = (
#     'muffin_peewee',
#     'muffin_session',
#     'muffin_debugtoolbar',
# )

# Plugin options
# ==============

# SESSION_SECRET = 'secretsecret'
#
# PEEWEE_MIGRATIONS_PATH = 'backend/migrations'
# PEEWEE_CONNECTION = os.environ.get('DATABASE_URL', 'sqlite:///backend.sqlite')
#
# DEBUGTOOLBAR_EXCLUDE = ['/static']
# DEBUGTOOLBAR_HOSTS = ['0.0.0.0/0']
# DEBUGTOOLBAR_INTERCEPT_REDIRECTS = False
# DEBUGTOOLBAR_ADDITIONAL_PANELS = [
#     'muffin_peewee',
#     'muffin_jinja2',
# ]

HOST = "0.0.0.0"
PORT = 9000

# message queue
RABBITMQ_USER = ''
RABBITMQ_PASSWORD = ''
RABBITMQ_HOST = ''
RABBITMQ_PORT = 5672
RABBITMQ_COMMAND_QUEUE = "vmmaster_commands"

# database
DATABASE = "postgresql://vmmaster:vmmaster@localhost/vmmaster_db"

# logging
LOG_TYPE = "plain"
LOG_LEVEL = "INFO"
LOGGING = setup_logging(log_type=LOG_TYPE, log_level=LOG_LEVEL)

SESSION_TIMEOUT = 60

# selenium
SELENIUM_PORT = 4455
VMMASTER_AGENT_PORT = 9000
