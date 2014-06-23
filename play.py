import webapp2

form = """
<form method="post">
	What is your birthday?
	<br>

	<label>
		Month
		<input type="text" name="month" value="%(month)s">
	</label>
	<label>
		Day
		<input type="text" name="day" value="%(day)s">
	</label>
	<label>
		Year
		<input type="text" name="year" value="%(year)s">
	</label>
	<div style="color: red">%(error)s</div>
	<br>
	<br>

	<input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
	def write_form(self, error="", month="", day="", year=""):
		self.response.out.write(form % {"error": error,
										"month": month,
										"day": day,
										"year": year})

	def get(self):
		self.write_form()

	def post(self):
		user_month = self.request.get("month")
		user_day = self.request.get("day")
		user_year = self.request.get("year")

		month = user_month
		day = user_day
		year = user_year

		if not (year and day and month):
			self.write_form("Dude, not valid!!",
				user_month, user_day, user_year)
		else:
			self.redirect('/thanks')

class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Totally valid :)")

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/thanks', ThanksHandler)
], debug=True)