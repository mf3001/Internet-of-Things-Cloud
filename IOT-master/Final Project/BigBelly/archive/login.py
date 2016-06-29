import urllib, urllib2, cookielib

username = 'Jschneider'
password = 'downtownny'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'email' : username, 'password' : password})
opener.open('https://clean.bigbelly.com/api/login', login_data)
resp = opener.open('https://clean.bigbelly.com/compactor-info.jsp?serial-number=2404069')
print resp.read()