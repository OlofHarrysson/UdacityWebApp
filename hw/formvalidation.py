import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
	return USER_RE.match(username)


def valid_password(password, verify):
	if (password == verify):
		return PASS_RE.match(password)
	return False

def valid_email(email):
	return EMAIL_RE.match(email)
