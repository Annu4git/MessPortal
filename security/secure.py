import bcrypt
password = b"super secret password"
# Hash a password for the first time, with a randomly-generated salt

st = bcrypt.gensalt()
print st

hashed = bcrypt.hashpw(password, st)
# Check that an unhashed password matches one that has previously been
# hashed
if bcrypt.checkpw(password, hashed):
	print("It Matches!")
else:
	print("It Does not Match :(")

print "==============================================="

static_salt="#ANTS@!%"
password = "t@sahu"
dynamic_salt = "$2b$12$nhEvMgLphpBOEVB6KNn7Lu"
salted_password = static_salt + password
hashed = bcrypt.hashpw(salted_password, dynamic_salt)
print "hash is : ", hashed