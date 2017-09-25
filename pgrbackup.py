#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2017 Igor Riđanović, www.hdhead.com

#---- User Configuration ----

# Number of minutes between backups
interval   = 720

# Delete backups older than maxDays
maxDays    = 30

# Resolve Postgres database name and user name, default database name is provided
dbName     = 'Database_Name'
dbUser     = 'postgres'

# Database server IP address unless this script is running on the same server
dbHost     = '127.0.0.1'

# Installed Postgres version
pgVersion = '9.2'

#---- End of User configuration ----

import os
import sys
import getpass
import time
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT

sleeptime = interval * 60
version = 1.0
currentUser = getpass.getuser()

# Determine the host operating system and set OS specific variables
hostOS = sys.platform

if hostOS == 'win32':
	eol = '\r\n'
	dumpTool = 'C:\\"Program Files"\\PostgreSQL\\%s\\bin\\pg_dump.exe' %pgVersion
	destPath = os.path.join('C:\Users', currentUser, 'Documents\ResolveProjectBackup')

elif hostOS == 'darwin':
	eol = '\n'
	dumpTool = '/Library/PostgresSQL/%s/bin/pg_dump' %pgVersion
	destPath   = os.path.join('Users', currentUser, 'Documents/ResolveProjectBackup')

# We assume Linux host unless Windows or OS X.
else:
	eol = '\n'
	dumpTool = '/usr/bin/pg_dump'
	destPath = os.path.join('/home', currentUser, 'Documents/ResolveProjectBackup')

def wincompliance(ts):
	"""remove space and colons from timestamp for Windows compliance"""
	noSpace = 'T'.join(ts.split())
	noColon = '-'.join(noSpace.split(':'))
	return noColon

# Verify if destination path is valid. Create destination directory if missing.
if not os.path.isdir(destPath):
	os.makedirs(destPath)

# Create log file if missing
logName = 'ResolveBackupLog.txt'
logPath = os.path.join(destPath, logName)
if not os.path.isfile(logPath):
	logfile = open(logPath, 'w')
	logfile.write('Resolve Postgres Database Backup Tool V%s.' %version)
	logfile.write(eol)
	logfile.close()

# Infinite backup loop
while True:

	# Form pg_dump argument string and create backup
	timeStamp = str(datetime.now())[:-7]
	backupName = 'Resolve_%s_PostgresDump_%s' % (dbName, wincompliance(timeStamp))
	savePath = os.path.join(destPath, backupName + '.sqlc')
	command = '%s -U %s -h %s -F c -f %s %s' % (dumpTool, dbUser, dbHost, savePath, dbName)
	process = Popen(command, universal_newlines=True, stdout=PIPE, stderr=STDOUT, shell=True)
        stdout, stderr = process.communicate()
        print stdout
        print stderr
        print backupName + ' saved'

	# Write a log entry
	logfile = open(logPath, 'a')
	logfile.write('Created %s.sqlc'%backupName)
	logfile.write(eol)
	logfile.close()
	
	# Remove old backups
	now = time.time()
	for filename in os.listdir(destPath):
		if filename.endswith('sqlc') == True:
			deleteFile = os.path.join(destPath, filename)
			timeStamp  = os.stat(deleteFile).st_mtime
			if maxDays + 1< (now - timeStamp) / 86400: # x/86400 converts seconds to days
				os.remove(deleteFile)

        print 'sleeping...'
	time.sleep(sleeptime)



