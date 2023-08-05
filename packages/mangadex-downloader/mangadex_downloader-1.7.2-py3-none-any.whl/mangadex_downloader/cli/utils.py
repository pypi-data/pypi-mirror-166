import logging
import signal
import sys

from .. import __version__, __repository__
from ..update import architecture, executable
from ..network import Net
from ..downloader import _cleanup_jobs
from ..errors import MangaDexException, NotLoggedIn

log = logging.getLogger(__name__)

# Will be used in main() and get_args()
sys_argv = sys.argv[1:]

def setup_logging(name_module, verbose=False):
    log = logging.getLogger(name_module)
    handler = logging.StreamHandler()
    fmt = logging.Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(fmt)
    log.addHandler(handler)
    if verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    return log

def setup_proxy(proxy=None, from_env=False):
    if proxy and from_env:
        raise MangaDexException("--proxy and --proxy-env cannot be together")

    if from_env:
        log.debug("Using proxy from environments")

    if proxy:
        log.debug('Setting up proxy from --proxy option')
        Net.set_proxy(proxy)

def setup_network(args):
    # Build proxy
    setup_proxy(args.proxy, args.proxy_env)

    # Setup delay requests (if set)
    Net.set_delay(args.delay_requests)

    if args.dns_over_https:
        Net.set_doh(args.dns_over_https)
    
    if args.timeout:
        Net.set_timeout(args.timeout)

def _keyboard_interrupt_handler(*args):
    print("Cleaning up...")
    # Downloader are not cleaned up
    for job in _cleanup_jobs:
        job()

    # Unfinished jobs in pdf converting
    from ..format.pdf import _cleanup_jobs as pdf_cleanup

    for job in pdf_cleanup:
        job()

    # Logging out
    try:
        Net.mangadex.logout()
    except NotLoggedIn:
        pass

    print("Action interrupted by user", file=sys.stdout)
    sys.exit(0)

def register_keyboardinterrupt_handler():
    # CTRL+C is pressed
    signal.signal(signal.SIGINT, _keyboard_interrupt_handler)

    # CTRL+D (in Unix) is pressed or taskkill without force (in Windows)
    signal.signal(signal.SIGTERM, _keyboard_interrupt_handler)

def close_network_object():
    log.info("Cleaning up...")
    log.debug("Closing netwok object")
    Net.close()

class Paginator:
    def __init__(self, limit=10):
        self._pages = {}
        self._size = 0
        self._pos = 0
        self._item_pos = 1
        self.limit = limit

    def add_page(self, *data):
        items = []
        for item in data:
            items.append({
                "pos": self._item_pos,
                "item": item
            })
            self._item_pos += 1

        if not items:
            return

        self._pages[self._size] = items

        self._size += 1
        
    def next(self):
        self._pos += 1
    
    def previous(self):
        if (self._pos - 1) < 0:
            raise IndexError

        self._pos -= 1

    def print(self):
        page = self._pages[self._pos]
        for item in page:
            print(f"({item['pos']}). {item['item']}")

def print_version_info():
    bundled_executable = 'yes' if executable else 'no'

    print(f"mangadex-downloader v{__version__} ({__repository__})")
    print("Python: {0[0]}.{0[1]}.{0[2]}".format(sys.version_info))
    print(f"arch: {architecture}")
    print(f"bundled executable: {bundled_executable}")

def dynamic_bars(length):
    if isinstance(length, str):
        length = len(length)

    bar = ""
    for _ in range(length):
        bar += "="
    
    return bar

def get_key_value(text, sep='='):
    splitted = text.split(sep, maxsplit=1)
    key = splitted[0]
    value = "".join(splitted[1:])
    return key, value

def split_comma_separated(text, single_value_to_list=False):
    if ',' not in text:
        return [text] if single_value_to_list else  text
    
    return [i.strip() for i in text.split(',')]
    
