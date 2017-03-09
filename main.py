from bs4 import BeautifulSoup
import urllib3
import socket, threading

from HtmlParse import *
from Server import *

# http = urllib3.PoolManager()
# page = http.request('get', 'http://www.radunia.ru/oplata').data
# markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
# soup = BeautifulSoup(page, 'html.parser')
#
# soup.prettify()
#
#
# htmlp = HtmlParse("rassudariki.ru")
# htmlp.get_keywords()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 1911))
s.listen(10)

lock = threading.Lock()

while True:
    (client_sock, client_addr) = s.accept()
    Server(client_sock, client_addr).start()
