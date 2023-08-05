# noinspection PyUnresolvedReferences
from mixlab import runSh, PortForward_wrapper
# noinspection PyUnresolvedReferences
from IPython.display import clear_output
from urllib.parse import urlparse
from omnitools import abs_dir
from ..utils import runShell
import urllib.request
import random
import os


def startFileServer(port, cd="/"):
    try:
        urllib.request.urlopen("http://localhost:{}".format(port))
        return False
    except:
        runShell("python3.7 -m http.server {}".format(port), cd=cd)
        return True


def startWRCS(port, sc_port):
    t = open(os.path.join(abs_dir(__file__), "wrcs.py"), "rb").read().decode()
    t = t.replace("'<port>'", str(port)).replace("'<sc_port>'", str(sc_port))
    open("wrcs.py", "wb").write(t.encode())
    runShell("python3.7 wrcs.py")


def penetrateIntranet(name, port):
    PORT_FORWARD = "argotunnel"
    TOKEN = ""
    USE_FREE_TOKEN = True
    REGION = "JP"
    Server = PortForward_wrapper(
        PORT_FORWARD,
        TOKEN,
        USE_FREE_TOKEN,
        [[name, port, 'http']],
        REGION.lower(),
        ["", random.randint(5000, 10000)]
    )
    data = Server.start(name, displayB=False, v=False)
    return urlparse(data['url'])._replace(scheme='https').geturl()

