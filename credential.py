import os.path
from tools import *

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
	
	def getCount(self):
		return len(Credentials.credentials.keys())
	
	def load(self):
		if Credentials.credentials_loaded:
			print "Credentials have already been loaded!"
			return False
		
		cf = Credentials.credentials_file
		
		# if file already exists
		if createNewFile(cf) == None:
			
			# open file for reading
			f = open(cf, 'r')
			
			done = False
			
			# read line
			while not done:
				fcred = f.readline().split()
				
				if len(fcred) == 2:
					Credentials.credentials.update( {fcred[0] : fcred[1] })
				
				if not fcred:
					done = True
			
			f.close()
		
		# else file was created
		else:
			
			print "Created new credentials file."
	
	def save(self):
		
		cf = Credentials.credentials_file
		
		# if file doesnt exist, create it
		createNewFile(cf)

		# open file for writing
		f = open(cf, 'w')
		
		# write all credentials to file
		for cred in Credentials.credentials:
			try:
				f.write("%s %s\n" % (cred, Credentials.credentials[cred]) )
			except:
				pass
		
		f.close()
	
	def getAccount(self, ta):
		
		if len(ta) != 1:
			return None
		
		# check that target account is valid
		if type(ta) != dict:
			return None
		
		for k in self.credentials.keys():
			# if login name found
			if ta.keys()[0] == k:
				# if password matches
				if ta.values()[0] == self.credentials[k]:
					# return account name
					return k
		
		# nothing found
		return None
	
	def usernameExists(self, uname):
		return uname in self.credentials
		
	def addAccount(self, newaccount):
		if type(newaccount) == dict:
			self.credentials.update( newaccount)
			return True
		else:
			return False

if __name__ == "__main__":
	
	# save credentials to test file
	testpath = "./testcred/testcred.dat"
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
	

		
	
