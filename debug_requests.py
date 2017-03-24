import logging
import contextlib

try:
    from http.client import HTTPConnection # py3
except ImportError:
    from httplib import HTTPConnection # py2

class DebugRequests:
    def debug_requests_on(self):
        '''Switches on logging of the requests module.'''
        HTTPConnection.debuglevel = 1

        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    def debug_requests_off(self):
        '''Switches off logging of the requests module, might be some side-effects'''
        HTTPConnection.debuglevel = 0

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.WARNING)
        root_logger.handlers = []
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.WARNING)
        requests_log.propagate = False

    def debug_requests(self):
        debug_requests_on()
        yield
        debug_requests_off()
