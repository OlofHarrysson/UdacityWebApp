import string
import hashlib
import random

def make_salt():
	return ''.join(random.choice(string.letters) for x in xrange(5))


def make_pw_hash(name, pw, salt = None):
	if not salt:
		salt = make_salt()
	hash_pw = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s|%s' % (hash_pw, salt)

def valid_pwd(name, pw, hash_pw):
	salt = hash_pw.split('|')[1]
	return hash_pw == make_pw_hash(name, pw, salt)


