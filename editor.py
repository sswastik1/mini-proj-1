from random import randint

sid = randint()
sid_array = []

class Editor:
	def __init__(self, eid, pwd)
		self.eid = 
		self.pwd = 

	def AddMovie():
	while True:
		m_mid = input("Please type the unique movie id   ")
		db.c.execute("SELECT COUNT(*) FROM movies WHERE mid=:m_mid")
		count = db.c.fetchall()
		if count = 0:
			break

	m_title = input("Please type the movie title   ")
	m_year = input("Please type the year of realease   ")
	m_runtime = input("Please type the runtime   ")
	
	movie_to_add = [
						(m_mid, m_title, m_year, m_runtime)
					]		
	db.c.execute("INSERT INTO movies VALUES (?,?,?,?)", movie_to_add)
	
	while True:
		c_pid = input("Please enter the id of the cast member you want to enter  ")
		db.c.execute("SELECT COUNT(*) FROM movies WHERE mid=:m_mid")
		count = db.c.fetchall()
		if count == 0:
			conformation = input("Do you want to give this id a new role?  ")
			
			if conformation == Yes:
				c_pid = input("Please enter the id of the cast member you want to enter  ")
				mp_name = input("Please type in the name of the new cast member  ")
				mp_birthYear = input("Please type in the birth year of the new cast member  ")
				cast_to_add = [
								(c_pid, mp_name, mp_birthYear)	
								]
				db.c.execute("INSERT INTO moviePeople VALUES (?,?,?)", cast_to_add)

		else:
			db.c.execute('''SELECT mp.name mp.birthYear
							FROM casts c, moviePeople mp
							WHERE c.pid=:c_pid and c.pid = mp.pid 
							''')
			casts_members = db.c.fetchall()
			print(casts_members[0] + " | " + casts_members[1])
			break







