import time,random
from datetime import date

from login import Login


class Session:
    def __init__(self,log):
        self.start_time = time.time()
        self.date = str(date.today())
        self.end_time = None
        self.duration = "NULL"
        self.log = log
        self.session_id = self.__generate()
        self.insert()

    def __generate(self):
        data = self.log.cursor.execute("select sid from sessions ORDER BY sid ").fetchall()
        sess_id = data[len(data)-1][0]+1
        return sess_id

    def insert(self):
        query = "insert into sessions values (:sid, :cid, :date, :dur);"
        self.log.cursor.execute(query,{'sid': self.session_id,'cid':self.log.id,'date':self.date,'dur':self.duration})
        self.log.conn.commit()

    def end_session(self):
        self.end_time = time.time()
        self.duration = (self.end_time - self.start_time)//60.0
        query = "UPDATE sessions set duration = :dur where sid = :sid"
        self.log.cursor.execute(query,{'dur':self.duration,'sid':self.session_id})
        self.log.conn.commit()


class Movie:
    def __init__(self,log:Login):
        self.log = log
        self.start_time = None
        self.end_time = None
        self.duration = 0

    def search_movie(self):

        #         '''SELECT m.title, m.year, m.runtime ,count(m.title)
        # from movies m, moviePeople mp, casts c
        # where m.mid = c.mid AND
        # c.pid = mp.pid and
        # m.title like '%the%' COLLATE NOCASE or
        # mp.name like '%the%' COLLATE NOCASE or
        # c.role like '%the%' COLLATE NOCASE
        # GROUP by m.title
        # ORDER BY count(m.title) DESC'''
        keywords = input("Enter the keywords to search for: ").split()

        query = '''SELECT m.title, m.year, m.runtime ,count(m.title)
                   from movies m, moviePeople mp, casts c
                   where m.mid = c.mid AND
                   c.pid = mp.pid and'''
        for keyword in keywords:
            query += ''' m.title like '%''' + keyword + '''%' COLLATE NOCASE or'''
            query += ''' mp.name like '%''' + keyword + '''%' COLLATE NOCASE or'''
            query += ''' c.role like '%''' + keyword + '''%' COLLATE NOCASE'''
        query += ''' GROUP by m.title
                    ORDER BY count(m.title) DESC
                    LIMIT 5'''

        print(self.log.cursor.execute(query).fetchall())

class System:
    def __init__(self,log:Login):
        self.log = log
        self.session = None
        self.movies = []

    def start_session(self):
        self.session = Session(self.log)

    def search_movies(self):
        pass

    def end_session(self):
        # TODO: end movies
        self.session.end_session()


if __name__ == '__main__':
    l1 = Login("c100","cmput291","./mini-proj.db")
    l1.login()
    s1 = System(l1)
    s1.start_session()
    m = Movie(l1)
    m.search_movie()
    s1.end_session()
