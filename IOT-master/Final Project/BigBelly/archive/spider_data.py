import re
import mechanize

username = "username"
password = "password"
success_verification_text = "Log Out"

br = mechanize.Browser()
response = br.open("https://account.dyn.com/")


#select the login form
for form1 in br.forms():
    form = form1
    break;

br.select_form(nr=0)
print form
form["username"] = username
form["password"] = password

response = br.submit()


if success_verification_text in response.read():
    print "SUCCESS"
else:
    print "FAILED"