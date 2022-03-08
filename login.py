import sqlite3


class Login:
    def __init__(self,sid,pwd,database):
        self.id = sid
        self.pwd = pwd
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()
        self.cursor.execute(' PRAGMA foreign_keys=ON; ')
        self.conn.commit()
        self.login_type = ''
        self.success = 0
        self.name = ""

    def signup(self,name):
        query = "insert into customers values (:cid, :name, :pwd);"
        data = self.cursor.execute("select * from editors where eid = :cid",{'cid':self.id}).fetchall()
        if not data:
            try:
                self.cursor.execute(query,{'cid':self.id,'name':name,'pwd':self.pwd})
            except sqlite3.IntegrityError:
                print("User ID already taken. Try again")
                return 0

            # Continue if no error
            if self.cursor.rowcount == 1:
                self.conn.commit()
                self.login_type = 'c'
                return 1
            return 0
        else:
            print("User ID already taken. Try again")
            return 0

    def login(self):
        query_customer = "SELECT * FROM customers where cid= :cid"
        query_editor = "SELECT * FROM editors where eid = :cid"
        data = self.cursor.execute(query_customer,{'cid':self.id}).fetchall()
        self.login_type = 'c'

        # If the id is not in customer we query the editors database
        if not data:
            data = self.cursor.execute(query_editor,{'cid':self.id}).fetchall()
            self.login_type = 'e'
            if not data:
                print("User ID not found")
                self.login_type = ''
                self.success = 0
                return 0
        if data[0][2] == self.pwd:
            self.name = data[0][1]
            return 1
        else:
            print("Incorrect Password")
        return 0


if __name__ == '__main__':
    # Tests'
    from getpass import getpass
    userid = input("Enter id: ")
    pwd = getpass("Enter pwd: ")
    print(pwd)

    l1 = Login(userid,pwd,"./mini-proj.db")
    l1.signup("hridyansh")
    print(l1.login())