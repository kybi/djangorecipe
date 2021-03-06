import os
import sys
import gevent.socket
import redis.connection
from ws4redis.uwsgi_runserver import uWSGIWebsocketServer


def main(settings_file, logfile=None):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_file)
    if logfile:
        import datetime

        class logger(object):
            def __init__(self, logfile):
                self.logfile = logfile

            def write(self, data):
                self.log(data)

            def writeline(self, data):
                self.log(data)

            def log(self, msg):
                line = '%s - %s\n' % (
                    datetime.datetime.now().strftime('%Y%m%d %H:%M:%S'), msg)
                fp = open(self.logfile, 'a')
                try:
                    fp.write(line)
                finally:
                    fp.close()
        sys.stdout = sys.stderr = logger(logfile)

    redis.connection.socket = gevent.socket
    return uWSGIWebsocketServer()
