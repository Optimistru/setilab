from mysql.connector import MySQLConnection
from python_mysql_dbconfig import read_db_config

from Connection import *
from bs4 import BeautifulSoup
import urllib3

import datetime


class HtmlParse:
    url = ""
    page_id = -1  #id of current page in mysql database
    def __init__(self, page_url):
        (conn, dbc) = self.get_connection()
        #if already has this url - delete
        dbc.execute("INSERT INTO `pages`(`url`, `date`) VALUES ('"+page_url+"',"
                    "'"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"')")
        conn.commit()
        conn.close()
        self.page_id = dbc.lastrowid
        self.url = page_url

    def get_connection(self):  #get mysql connection
        return Connection.connection()

    def get_escape(self, st):  #get string escapes of slashes etc
        if (st):
            return st.replace("&", "&amp;").replace('\\', '\\\\').replace(')','\)').replace('(','\(').\
                replace('\"','\\\"').replace('\'','\\\'')

    def get_soup(self, page_url = None):  #do you wanna some tasty html soup?? :)
        if (self.page_id == -1):
            return
        if (page_url == None):
            page_url = self.url
        if (page_url == ""):
            raise NameError('Empty url')
        http = urllib3.PoolManager()
        page = http.request('get', page_url).data
        soup = BeautifulSoup(page, 'html.parser')
        soup.prettify()
        return soup

    def get_tag_p(self, page_url = None):  #get info about <p>
        if (self.page_id == -1):
            return
        if (page_url == None):
            page_url = self.url
        if (page_url == ""):
            raise NameError('Empty url')

        soup = self.get_soup(page_url)
        (conn, dbc) = self.get_connection()

        for ps in soup.findAll('p'):
            attr_str = self.get_escape(str(ps.attrs))
            content_str = self.get_escape(str(ps.contents[0]))
            if (content_str == ""):
                continue
            dbc.execute(
                 "INSERT INTO `tag_p`(`attr`, `value`, `pages_id`) VALUES ('" + attr_str + "',"
                                      "'" + str(content_str) + "','" + str(self.page_id) + "')")
        conn.commit()
        conn.close()

    def get_tag_hs(self, page_url = None):  #get info about <h1> - <h6>
        if (self.page_id == -1):
            return
        if (page_url == None):
            page_url = self.url
        if (page_url == ""):
            raise NameError('Empty url')

        soup = self.get_soup(page_url)
        (conn, dbc) = self.get_connection()

        for i in range(1, 7):
            for hs in soup.findAll("h%d" % i):
                attr_str = self.get_escape(str(hs.attrs))
                content_str = self.get_escape(str(hs.contents[0]))
                dbc.execute("INSERT INTO `tag_hs`(`h_num`, `attr`, `value`, `pages_id`) VALUES ('" + str(i) + "',"
                            "'" + attr_str + "','" + content_str + "','" + str(self.page_id) + "')")
        conn.commit()
        conn.close()

    def get_keywords(self, page_url = None):  #get info about <head> keywords
        if (self.page_id == -1):
            return
        if (page_url == None):
            page_url = self.url
        if (page_url == ""):
            raise NameError('Empty url')

        soup = self.get_soup(page_url)
        (conn, dbc) = self.get_connection()

        keywords = soup.find('meta', attrs={'name':'keywords'})

        words_arr = []
        if (keywords != None):
            words_arr = keywords['content'].split(', ')

        for kw in words_arr:
            keyword_str = self.get_escape(str(kw))
            dbc.execute("INSERT INTO `keywords`(`keyword`, `pages_id`) VALUES ('"+ keyword_str +"',"
                        "'" + str(self.page_id) + "')")
        conn.commit()
        conn.close()
