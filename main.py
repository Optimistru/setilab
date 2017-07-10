from bs4 import BeautifulSoup
import urllib3
import socket, threading

from HtmlParse import *
from Server import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 1911))
s.listen(10)

lock = threading.Lock()

while True:
    (client_sock, client_addr) = s.accept()
    Server(client_sock, client_addr).start()
