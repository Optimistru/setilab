from HtmlParse import *
from Connection import *
import hashlib

class BaseQueries:

    @classmethod
    def auth_check(self, login, password):
        (conn, dbc) = Connection.connection()
        passw = hashlib.md5(password).hexdigest()
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
    def get_by_num(self, page_id):
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
    def del_by_num(self, page_id):
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
        analyse = HtmlParse(http_address)
        if (self.is_running):
            analyse.get_keywords()
        if (self.is_running):
            analyse.get_tag_hs()
        if (self.is_running):
            analyse.get_tag_p()
        self.is_running = True

    @classmethod
    def stop(self, page_id):
        self.is_running = False