import webapp2
import os
import jinja2

from hw import cookie
from hw import formvalidation
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)



class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


class Blog(Handler):
	def render_front(self):
		blog_posts = db.GqlQuery("SELECT * FROM Blogs")
		self.render("allblogs.html", blog_posts=blog_posts)


	def get(self):
		self.render_front()

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")

		if subject and content:
			blog = Blogs(subject = subject, content = content)
			blog.put()
			self.redirect("/blog")
		else:
			self.redirect("/blog/newpost")



class Blogs(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)

class Users(db.Model):
	username = db.StringProperty(required = True)
	hash_pw = db.StringProperty(required = True)
	email = db.StringProperty(required = False)

class Newpost(Handler):
	def render_front(self):
		self.render("blog.html")

	def get(self):
		self.render_front()

class MainPage(Handler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		visits = self.request.cookies.get('visits', '0')
		if visits.isdigit():
			visits = int(visits) + 1
		else:
			visits = 0

		self.response.headers.add_header('Set-Cookie', 'visits=%s' % visits)

		self.write("You have been here %s times" % visits)

class Signup(Handler):
	def get(self):
		self.render_front()

	def render_front(self, username="", email="", error_msg=""):
		self.render("hw3signup.html", username=username, email=email, error_msg=error_msg)

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")

		valid_un = formvalidation.valid_username(username)
		valid_pwd = formvalidation.valid_password(password, verify)
		if email:
			valid_email = formvalidation.valid_email(email)		
		else:
			valid_email = ""


		c_user = self.request.cookies.get('username', '')
		c_hash_pw = self.request.cookies.get('hash_pw', '')
		
		if not c_user == '' and not c_hash_pw == '':
			self.redirect("/blog/login")
			return



		if(valid_un and valid_pwd and (valid_email or valid_email == "")):
			hash_pw = cookie.make_pw_hash(username, password)

			str_username = str(username)
			str_hash_pw = str(hash_pw)

			self.response.headers.add_header('Set-Cookie', 'username='+str_username+'; Path=/')
			self.response.headers.add_header('Set-Cookie', 'hash_pw='+str_hash_pw+'; Path=/')
			
			self.redirect("/blog/welcome")
		else:
			error_msg = "That was not a valid "
			if not valid_un:
				username = ""
				error_msg += "username "
			if not valid_pwd:
				error_msg += "password "
			if not valid_email:
				email = ""
				error_msg += "email"
			self.render_front(username, email, error_msg)


class Welcome(Handler):
	def get(self):
		c_user = self.request.cookies.get('username', '')
		if c_user == '':
			c_user = 'unknown user'

		self.render_front(c_user)

	def render_front(self, c_user=""):
		self.render("hw3welcome.html", c_user=c_user)



class Login(Handler):
	def get(self):
		c_user = self.request.cookies.get('username', '')
		already_user = ''
		if not c_user == '':
			already_user = 'You username is %s' % c_user 
		self.render_front(already_user=already_user)

	def render_front(self, error_msg="", already_user=""):
		self.render("hw3login.html", error_msg=error_msg, already_user=already_user)

	def post(self):
		username = self.request.get("username")
		c_user = self.request.cookies.get('username', '')
		password = self.request.get("password")
		c_hash_pw = self.request.cookies.get('hash_pw', '')
		if not c_hash_pw == '':
			pw_valid = cookie.valid_pwd(username, password, c_hash_pw)
		else:
			pw_valid = False

		if username == c_user and pw_valid:
			self.redirect("/blog/welcome")
			return
		else:
			self.render_front(error_msg='Could not login')
		

class Logout(Handler):
	def get(self):
		self.response.delete_cookie('username')
		self.response.delete_cookie('hash_pw')

		self.redirect("/blog/signup")

	


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog', Blog),
    ('/blog/newpost', Newpost),
    ('/blog/signup', Signup),
    ('/blog/welcome', Welcome),
    ('/blog/login', Login),
    ('/blog/logout', Logout)
], debug=True)