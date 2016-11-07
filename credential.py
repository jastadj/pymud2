import os.path

# credentials object stored in server

class Credentials(object):
	
	credentials = {}
	
	credentials_loaded = False
	
	credentials_file = "./data/credentials.dat"
	
	def __init__(self, altfile = None):
		
		# alternate credentials file provided
		
		if altfile != None:
			if Credentials.credentials_file != altfile:
				Credentials.credentials_loaded = False
			Credentials.credentials_file = altfile
	
	def load(self):
		if Credentials.credentials_loaded:
			print "Credentials have already been loaded!"
			return False
		
		cpath = Credentials.credentials_file
		
		# if credentials file exists
		if os.path.isfile(cpath):
			
			# open file for reading
			rfile = open(cpath, 'r')
			
			done = False
			
			# read line
			while not done:
				fcred = rfile.readline().split()
				
				if len(fcred) == 2:
					Credentials.credentials.update( {fcred[0] : fcred[1] })
				
				if not fcred:
					done = True
			
			rfile.close()
		
		# else file doesnt exist, create new one
		else:
			
			# if directory doesnt exist, create one
			cdir = os.path.dirname(cpath)
			print "cdir=" + cdir
			if cdir != ".":
				try:
					os.path.stat(cdir)
				except:
					os.mkdir(cdir)
			
			# create new file
			try:
				newfile = open(cpath, 'w')
			except:
				print "Unable find or create credential file!"
				return False
			
			newfile.close()
			
			print "Created new credentials file."
	
	def save(self):
		
		cpath = Credentials.credentials_file

		# if directory doesnt exist, create one
		cdir = os.path.dirname(cpath)
		if not os.path.isdir(cdir) and cdir != "":
			os.mkdir(cdir)

		# open file for writing
		rfile = open(cpath, 'w')
		
		# write all credentials to file
		for cred in Credentials.credentials:
			try:
				rfile.write("%s %s\n" % (cred, Credentials.credentials[cred]) )
			except:
				pass
		
		rfile.close()

if __name__ == "__main__":
	
	# save credentials to test file
	testpath = "testcred.dat"
	testcred = Credentials(testpath)
	newcreds = {"john":"postal", "mel":"melly", "alyssa":"monkey"}
	Credentials.credentials = newcreds
	testcred.save()
	print "Saved %d credentials:" % len(Credentials.credentials.keys())
	for cred in Credentials.credentials:
		print cred + ":" + Credentials.credentials[cred]
	
	# erase and load credentials from testfile
	Credentials.credentials = {}
	testcred.load()
	print "Loaded %d credentials" % len(Credentials.credentials.keys())
	db = Credentials.credentials
	for cred in db:
		print cred + ":" + db[cred]
	
	print "\n"
	
	# save credentials to testfile with directory
	testpath = "./testcred/anotherdir/testcred2.dat"
	testcred = Credentials(testpath)
	Credentials.credentials = newcreds
	testcred.save()
	print "Saved %d credentials:" % len(Credentials.credentials.keys())
	for cred in Credentials.credentials:
		print cred + ":" + Credentials.credentials[cred]	
	
	# erase and load credentials from testfile
	Credentials.credentials = {}
	testcred.load()
	print "Loaded %d credentials" % len(Credentials.credentials.keys())
	db = Credentials.credentials
	for cred in db:
		print cred + ":" + db[cred]
		
