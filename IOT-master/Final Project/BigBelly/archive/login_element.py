import requests
from lxml import html
from xml.etree import ElementTree
from selenium import webdriver

USERNAME = "Jschneider"
PASSWORD = "downtownny"

LOGIN_URL = "https://clean.bigbelly.com/login.jsp"
URL = "https://clean.bigbelly.com/compactor-info.jsp?serial-number=2404069"

def main():
    session_requests = requests.session()

    # Get login csrf token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.content)
    #print tree.text
    authenticity_token = list(set(tree.xpath("//input[@name='destination']/@value")))[0]
    #print authenticity_token
    # Create payload
    payload = {
        "email": USERNAME, 
        "password": PASSWORD, 
        "destination": authenticity_token,
        "whichButton": ""
    }

    # Perform login
    POST_URL = "https://clean.bigbelly.com/api/login"
    result1 = session_requests.post(POST_URL, data = payload, headers = dict(referer = LOGIN_URL))
    #print result1.content
    # Scrape url

    browser = webdriver.Chrome()
    browser.get(POST_URL)
    html1 = browser.find_element_by_id('summary')
    print(html1)

    # result2 = session_requests.get(URL, headers = dict(referer = URL))
    # tree = html.fromstring(result2.content)
    # print result2.content
    # #print tree.text
    # #bucket_elems = ElementTree.Element("summary")
    # bucket_elems = tree.findall(".//table[@class='chart-sidebar']/tr")
    # bucket_names = [bucket_elem.text_content().replace("\n", "").strip() for bucket_elem in bucket_elems]
    # #print bucket_elems
    # #print bucket_names

if __name__ == '__main__':
    main()
