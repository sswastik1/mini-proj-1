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
    def __init__(self,log:Login,session:Session):
        self.log = log
        self.start_time = None
        self.end_time = None
        self.time_watched = 0
        self.session = session

    def end_movie(self):
        self.end_time = time.time()
        self.time_watched = (self.end_time-self.start_time)//60
        query_watch = "UPDATE watch set duration =:dur where sid = :sid and cid = :cid and duration = 'NULL'"
        self.log.cursor.execute(query_watch,{'dur':self.time_watched,'sid':self.session.session_id,'cid':self.log.id})
        self.log.conn.commit()

    def display_movies(self,data):
        if not data:
            print("No more choices. Try again! ")
            return 9
        print("|"+"-"*132+"|")
        print("| {:^58s} | {:^38s} | {:^28s} |".format("Title","Release Year", "Duration"))
        print("|"+"-"*132+"|")
        i = 1
        for row in data:
            print("| {:58s} | {:^38d} | {:^28d} |".format(str(i)+". "+row[0],row[1],row[2]))
            i += 1
        print("|"+"-"*132+"|")
        choice = int(input("Enter the number for the movie you would like to watch. \nOr enter 0 for more options : "))
        if choice != 0:
            return data[choice-1]
        return choice

    def search_movie(self):
        keywords = input("Enter the keywords to search for: ").split()

        query = '''SELECT m.title, m.year, m.runtime ,count(m.title), m.mid
                   from movies m, moviePeople mp, casts c
                   where m.mid = c.mid AND
                   c.pid = mp.pid and'''
        for i in range(len(keywords)):
            keyword = keywords[i]
            query += ''' m.title like '%''' + keyword + '''%' COLLATE NOCASE or'''
            query += ''' mp.name like '%''' + keyword + '''%' COLLATE NOCASE or'''
            query += ''' c.role like '%''' + keyword + '''%' COLLATE NOCASE '''
            if i+1 < len(keywords):
                query += "or "
        query += ''' GROUP by m.title
                    ORDER BY count(m.title) DESC'''

        data = self.log.cursor.execute(query).fetchall()
        if data:
            choice = 0
            end = 5
            while choice == 0:
                choice = self.display_movies(data[end-5:end])
                if choice == 0:
                    end += 5
            if choice == 9:
                return

            # Print cast members
            print("\nCast Members: ")
            query_cast = '''SELECT mp.name, mp.pid
                            from moviePeople mp, casts c, movies m
                            where m.mid = :mid and m.mid = c.mid and c.pid = mp.pid'''
            members = self.log.cursor.execute(query_cast,{'mid':choice[4]}).fetchall()
            for i in range(len(members)):
                print(str(i+1)+" "+members[i][0])

            # Print the number of customers that watched this movie
            query_watch = '''select count(*)
                             from watch 
                             WHERE watch.mid = :mid'''
            watched = self.log.cursor.execute(query_watch,{'mid':choice[4]}).fetchall()[0][0]
            print("\nNumber of people that watched "+choice[0]+" : "+str(watched))

            print("Options: ")
            print("1. Follow a cast member")
            print("2. Start watching movie")
            option_choice = int(input("Choice number: "))

            if option_choice == 1:
                member_number = int(input("Enter the member choice: ")) - 1
                query_follow = "insert into follows values (:cid, :pid);"
                self.log.cursor.execute(query_follow,{'cid':self.log.id,'pid':members[member_number][1]})
                self.log.conn.commit()

            elif option_choice == 2:
                if self.start_time is None:
                    self.start_time = time.time()
                    query_watch = "insert into watch values (:sid,:cid,:mid, 'NULL');"
                    self.log.cursor.execute(query_watch,{'sid':self.session.session_id,'cid':self.log.id,'mid':choice[4]})
                    self.log.conn.commit()
                    print("Movie Started!")
                else:
                    print("You cannot start another movie before ending the current movie")
                return
        else:
            print("No results found.")
            return


class System:
    def __init__(self,log:Login):
        self.log = log
        self.session = None
        self.movie = None

    def start_session(self):
        self.session = Session(self.log)

    def search_movies(self):
        if self.session is None:
            self.session = Session(self.log)
        self.movie = Movie(self.log,self.session)
        self.movie.search_movie()

    def end_movie(self):
        self.movie.end_movie()

    def end_session(self):
        self.movie.end_movie()
        self.session.end_session()


if __name__ == '__main__':
    l1 = Login("hrid","hridyansh","./mini-proj.db")
    l1.login()
    s1 = System(l1)
    s1.start_session()
    # time.sleep(60)
    s1.search_movies()
    # time.sleep(120)
    s1.end_session()
    s1.end_session()
