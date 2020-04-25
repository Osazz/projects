import logging
import os
import sys
import sqlite3
from sqlite3 import Error
from configparser import ConfigParser

CURRENT_PATH = os.path.dirname(__file__)


class Logger(object):

    def __init__(self, name_file=None):
        self.name = name_file
        if not self.name:
            self.name = program_name()

        # create logger
        self.log = logging.getLogger(self.name)
        self.log.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.log.addHandler(ch)


class DatabaseUtil(object):
    def __init__(self, db_name=None):
        super().__init__()
        self.db_name = db_name
        if not self.db_name:
            self.db_name = os.path.join(CURRENT_PATH, Config().get_db_config().dbname)

        self.log = Logger('DatabaseUtil').log

    def do_db_transaction(self, method, *args, **kwargs):
        conn, cur = (None, None)
        try:
            conn = sqlite3.connect(self.db_name)
            cur = conn.cursor()
            return method(conn, cur, *args, **kwargs)
        except Error as e:
            self.log.error(e)
            raise SystemExit(2)
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


class Config(object):
    def __init__(self, database_conf=None):
        super().__init__()
        self.db_conf = database_conf

        if not self.db_conf:
            self.db_conf = self._get_conf()

        self.log = Logger('Config').log

    def get_db_config(self):
        parser = ConfigParser()
        if len(parser.read(self.db_conf)) == 0:
            msg = 'Failed to read config file %s' % self.db_conf
            self.log.error(msg)
            raise ValueError(msg)
        section = 'database'
        return DbConfig(
            _get(parser, section, 'db_name',),
        )

    def _get_conf(self):
        try:
            conf_file = os.path.join(CURRENT_PATH, 'variable.conf')
            os.chdir('/')
            return conf_file
        except OSError:
            msg = "No such directory at project root"
            self.log.error(msg)
            raise OSError(msg)


def _get(parser, section, option, required=True, default=None):
    if parser.has_option(section, option) or required:
        return parser.get(section, option).strip()
    return default


class DbConfig:
    def __init__(self, dbname):
        self.dbname = dbname


def program_name():
    return os.path.basename(sys.argv[0])
