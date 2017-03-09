import socket, threading
from array import array
from Controller import *

class Server(threading.Thread):
    #start work
    #help work
    #list work
    #info work
    #delete work
    #exit work
    welcome_message = 'Welcome to RSA - Robot of Sites Analysis\r\n' \
                      '-start: Login\r\n' \
                      '-help: Commands\r\n' \
                      '-list: List of analysed addresses\r\n' \
                      '-info #: Get info about site from list\r\n' \
                      '-delete #: Delete info about site from list\r\n' \
                      '-analysis "address": Start analysis of address\r\n' \
                      '-stop: Stop analysis\r\n' \
                      '-exit: Exit server\r\n'
    client_id = -1

    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        print("Connected by", address)

    def run(self):
        self.socket.recv(1024)
        # start_conv = bytes([255, 253, 34])
        # self.socket.send("/xff/xfd/x22".encode("utf-8"))
        self.socket.send(self.welcome_message.encode("utf-8"))

        while (True):
            # display welcome message
            data = self.socket.recv(1024).decode()  # wait for keypress + enter
            enter = self.socket.recv(1024).decode()
            print(data)

            if data == '\r\n':
                continue
# WITHOUT SIGN IN: BEGIN
            if data == 'start':
                data = 'Print login:\r\n'
                self.socket.send(data.encode("utf-8"))
                login = self.socket.recv(1024).decode()
                enter = self.socket.recv(1024).decode()

                data = 'Print password:\r\n'
                self.socket.send(data.encode("utf-8"))
                password = self.socket.recv(1024).decode().encode('utf-8')
                enter = self.socket.recv(1024).decode()

                self.client_id = BaseQueries.auth_check(login, password)
                if (self.client_id == -1):
                    data = 'Wrong login or pass, try again\r\n'
                    self.socket.send(data.encode("utf-8"))
                else:
                    data = 'Hello, %s\r\n' % login
                    self.socket.send(data.encode("utf-8"))

            elif data == 'help':
                data = self.welcome_message
                self.socket.send(data.encode("utf-8"))

            elif data == 'exit':
                break
# WITHOUT SIGN IN: END
#             elif (self.client_id == -1):  #if not sign in - continue
#                 data = 'Please sign in to continue\r\n'
#                 self.socket.send(data.encode("utf-8"))
#                 continue

            elif data == 'list':
                url_list = BaseQueries.get_list()
                url_str = ""
                for url in url_list:
                    url_str += "%d: %s\r\n" % (url[0], url[1])
                self.socket.send(url_str.encode("utf-8"))

            elif (str(data).split(' ')[0] == 'info' and len(str(data).split(' ')) > 1 and str(data).split(' ')[1].isdigit()):
                id = int(str(data).split(' ')[1])
                (keywords, tag_p, tag_hs) = BaseQueries.get_by_num(id)

                self.socket.send("KEYWORDS:\r\n".encode("utf-8"))
                keywords_str = ""
                if (len(keywords) == 0):
                    keywords_str = "NONE\r\n"
                for kw in keywords:
                    keywords_str += "%s\r\n" % (kw[1])
                self.socket.send(keywords_str.encode("utf-8"))

                self.socket.send("TAG P:\r\n".encode("utf-8"))
                ps_str = ""
                if (len(tag_p) == 0):
                    ps_str = "NONE\r\n"
                for p in tag_p:
                    ps_str += "%s\r\n%s\r\n\r\n" % (p[1], p[2])
                self.socket.send(ps_str.encode("utf-8"))

                self.socket.send("TAG H:\r\n".encode("utf-8"))
                hs_str = ""
                if (len(tag_hs) == 0):
                    hs_str = "NONE\r\n"
                for hs in tag_hs:
                    hs_str += "H%d:\r\n%s\r\n%s\r\n\r\n" % (hs[1], hs[2], hs[3])
                self.socket.send(hs_str.encode("utf-8"))

            elif (str(data).split(' ')[0] == 'delete' and len(str(data).split(' ')) > 1 and str(data).split(' ')[1].isdigit()):
                id = int(str(data).split(' ')[1])
                result = BaseQueries.del_by_num(id)
                if (result == 1):
                    self.socket.send("Delete successful\r\n".encode("utf-8"))
                else:
                    self.socket.send("An error occurred\r\n".encode("utf-8"))

            elif (str(data).split(' ')[0] == 'analysis' and len(str(data).split(' ')) > 1 and str(data).split(' ')[1] != None):
                http_address = str(str(data).split(' ')[1])
                #is http regexp
                result = Analysis.run(http_address)

            elif (str(data).split(' ')[0] == 'stop' and len(str(data).split(' ')) > 1 and str(data).split(' ')[1] != None):
                raise NotImplemented

            else:
                data = self.welcome_message
                self.socket.send(data.encode("utf-8"))

        self.socket.send("Exiting...".encode("utf-8"))
        # close connection
        self.socket.close()




