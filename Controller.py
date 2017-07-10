from HtmlParse import *
from Connection import *
import hashlib

class BaseQueries:

    @classmethod
    def auth_check(self, login, password): #authorization check
        (conn, dbc) = Connection.connection()
        passw = hashlib.md5(password.encode("utf-8")).hexdigest()
        dbc.execute("SELECT id FROM `users` WHERE login = '" + login + "'"
                    " AND password = '" + passw + "'")
        data = dbc.fetchone()
        conn.commit()
        conn.close()
        if (data != None):
            return data[0]
        else:
            return -1

    @classmethod
    def get_list(self):
        (conn, dbc) = Connection.connection()
        dbc.execute("SELECT id, url FROM `pages` ")
        data = dbc.fetchall()
        conn.close()
        return data

    @classmethod
    def get_by_num(self, page_id): #get all info by number in sites list
        (conn, dbc) = Connection.connection()
        dbc.execute("SELECT * FROM `keywords` WHERE pages_id = '%d'" % page_id)
        keywords = list(dbc.fetchall())

        dbc.execute("SELECT * FROM `tag_p` WHERE pages_id = '%d'" % page_id)
        tag_p = list(dbc.fetchall())

        dbc.execute("SELECT * FROM `tag_hs` WHERE pages_id = '%d'" % page_id)
        tag_hs = list(dbc.fetchall())

        conn.close()
        return (keywords, tag_p, tag_hs)

    @classmethod
    def del_by_num(self, page_id): #delete all info by number in sites list (another tables DELETE CASCADE)
        (conn, dbc) = Connection.connection()
        try:
            dbc.execute("DELETE FROM `pages` WHERE id = '%d'" % page_id)
            conn.commit()
        except Error as error:
            print(error)
            return 0
        finally:
            dbc.close()
            conn.close()

        return 1


class Analysis:

    is_running = True

    @classmethod
    def run(self, http_address):
        self.is_running = True
        analyse = HtmlParse(http_address)
        if (self.is_running):
            analyse.get_keywords()
        else:
            return 0
        if (self.is_running):
            analyse.get_tag_hs()
        else:
            return 0
        if (self.is_running):
            analyse.get_tag_p()
        else:
            return 0
        return 1

    @classmethod
    def stop(self):
        self.is_running = False