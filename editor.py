import os
import sys
from datetime import datetime
from random import randint
from collections import Counter
from database import DB
from login import login

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




	def Update()
	print('''Please select a term from the following:
		  1.) Monthly
		  2.) Annual
		  3.) All-time Report''')
	term = input()
	if lower(term) == monthly:
		till = "-30 days"
	if else lower(term) == "monthly":
		till = "-365 days"
	
	db.c.execute('''
				SELECT (*)
				FROM movies m, sessions s, customers cm 
				WHERE date(s.sdate) >= date('now', till)

				INTERSECT

				SELECT m1.mid, m2.mid, COUNT(customers)
				FROM movies m1, movies m2, customers cm, watch w
				WHERE cm.cid = w.cid and w.mid = m1.mid 
					and w.mid = m2.mid and m1.mid != m2.mid  
				ORDER BY DESC	
				''')
	final = db.c.fetchall()
	
	db.c.execute('''
				SELECT recommended
				FROM recommendations
				''')
	reccomended = db.c.fetchall()
	indicator = NO		
	for j in (0, range(final)):
		for i in (0,range(reccomended)):
			if final[j] in reccomended[i] and final[j] in reccomended[i]:
				indicator = YES




