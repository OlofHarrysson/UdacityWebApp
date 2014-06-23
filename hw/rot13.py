import cgi


def escape_html(s):
	return cgi.escape(s, quote = True)

def encrypt_text(text):
	

	new_string = ""

	for s in text:
		c = ord(s)
		if(c > 64 and c <= 90):
			c += 13
			if(c > 90):
				c -= 26
			s = chr(c)
		elif(c > 96 and c <= 122):
			c += 13
			if(c > 122):
				c -= 26
			s = chr(c)

		new_string += s

	escaped_html = escape_html(new_string)

	return escaped_html