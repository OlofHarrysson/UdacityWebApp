import webapp2
from hw import rot13
from hw import formvalidation
from hw import blog

# form ='''
# <form method="post">
# 	<h1>Encrypt text with rot13</h1>
# 	<textarea name="text" style="width: 450px; height: 150px">%s</textarea>
# 	<br>
# 	<input type="submit">
# </form>
# '''

form = '''
<h1>Signup</h1>
<br>
<form method="post">
	<label>
		Username <input type="text" name="username"> %(name)s
	</label>
	<br>
	<label>
		Password <input type="password" name="password"> %(pass)s
	</label>
	<br>
	<label>
		Verify Password <input type="password" name="verify">
	</label>
	<br>
	<label>
		Email <input type="text" name="email"> %(email)s
	</label>
	<br>
	<input type="submit">

'''



class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Velkommen!')


class Encrypter(webapp2.RequestHandler):
	def write_form(self, text=""):
		self.response.out.write(form % text)

	def get(self):
		self.write_form()

	def post(self):
		self.write_form(rot13.encrypt_text(self.request.get("text")))


class Signup(webapp2.RequestHandler):
	def get(self):
		self.write_form()

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")

		valid_un = formvalidation.valid_username(username)
		valid_pwd = formvalidation.valid_password(password, verify)
		valid_email = formvalidation.valid_email(email)

		if(valid_un and valid_pwd and valid_email):
			URL = '?q=' + username
			self.redirect('/welcome'+ URL)
		else:
			if (valid_un):
				valid_un = ""
			else:
				valid_un = "invalid"
			if (valid_pwd):
				valid_pwd = ""
			else:
				valid_pwd = "invalid"
			if (valid_email):
				valid_email = ""
			else:
				valid_email = "invalid"
			

			self.response.out.write(form % {"name": valid_un,
											"pass": valid_pwd,
											"email": valid_email})

	def write_form(self):
		self.response.out.write(form % {"name": "",
										"pass": "",
										"email": ""})


class Welcome(webapp2.RequestHandler):
	def get(self):
		username = self.request.get('q')
		self.response.out.write('Welcome ' + username)



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/encrypter', Encrypter),
    ('/signup', Signup),
    ('/welcome', Welcome),
], debug=True)
