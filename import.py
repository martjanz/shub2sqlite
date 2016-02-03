import sys, getopt
import os.path
import sqlite3, json
import requests
import config # config file
from scrapinghub import Connection
		
""" Scrapinghub2Sqlite

1. Create sqlite database (if not exists yet, obviously)
	a. Create tables
2. get all projects from scrapinghub
3. check for new projects (not stored yet in local db)
4. for each project
	a. insert (only new) project data in shub_projects
	a. get new jobs (not stored yet in local db)
		i. insert job info in shub_jobs 
		ii. for each job
			I. insert items in shub_items
"""

def getJobItems(job_id):
	url = 'https://storage.scrapinghub.com/items/' + job_id \
		+ '?format=json&meta=_key&meta=_ts&apikey=' + config.apikey
	print url
	res = requests.get(url)

	return res.json()

def getJobs(db, jobs):
	for job in jobs:
		cursor = db.cursor()
		cursor.execute('''SELECT *
							FROM shub_jobs
							WHERE shub_id = ?''',\
			(job.id,))

		# insert jobs if not exists
		if len(cursor.fetchall()) == 0:
			print "Guardando job " + job.id + "..."
			
			jsonString = json.dumps(job.info)

			db.execute('''INSERT INTO shub_jobs (shub_id, raw_json)
							VALUES (?, ?)''',\
				[job.id, jsonString])

			for item in getJobItems(job.id):
				jsonString = json.dumps(item)

				# insert items
				db.execute('''INSERT INTO shub_items (shub_job_id, raw_json)
									VALUES (?, ?)''', [job.id, jsonString])
		cursor.close()
		db.commit()

def main(argv):
	getDeleted = False

	opts, args = getopt.getopt(argv, "d", ["deleted"])

	for opt, arg in opts:
		if opt in ("-d", "--deleted"):
			getDeleted = True

	# create schema if db not exists
	if not os.path.isfile(config.database):
		createSchema = True
	else:
		createSchema = False

	connection = Connection(config.apikey)

	# connect to database
	db = sqlite3.connect(config.database)
	cursor = db.cursor()
	
	if createSchema:	
		# open schema definition file
		file = open("schema.sql", 'r')
		for line in file.readlines():
			cursor.execute(line)
		db.commit()

	# get projects
	project_ids = connection.project_ids()

	for project_id in project_ids:
		project = connection[project_id]
		
		cursor.execute('''SELECT *
			FROM shub_projects
			WHERE shub_id = ?''', (project.id,))

		# insert if not exist
		if len(cursor.fetchall()) == 0:
			print "Guardando proyecto " + str(project.id) + "..."
			db.execute('''INSERT INTO shub_projects (shub_id)
							VALUES (?)''',\
				[project.id])

		# get finished jobs
		getJobs(db, project.jobs(state='finished'))

		# get deleted jobs
		if getDeleted:
			getJobs(db, project.jobs(state='deleted'))

	db.close()

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))