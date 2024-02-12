import requests # for sending HTTP requests
import time
from fake_useragent import UserAgent # for generating a random user agent

from stem import Signal # for renewing the IP address, Tor
from stem.control import Controller # for renewing the IP address, Tor

def switchIP(): 
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        time.sleep(10)

def get_ip(session):
    response = session.get('http://icanhazip.com')
    return response.text.strip()

headers = {"User_Agent":UserAgent().random} # for generating a random user agent

session = requests.session() 
session.proxies = {} 
session.proxies['http'] = 'socks5://localhost:9150' #9150 for browser; 9050 for TOR service
session.proxies['https'] = 'socks5://localhost:9150' #9150 for browser; 9050 for TOR service

print(get_ip(session))
switchIP()  # Switch the IP

print(get_ip(session))  # This should print a different IP address