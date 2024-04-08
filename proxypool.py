import requests
from bs4 import BeautifulSoup
import random

class ProxyPool:
    def __init__(self):
        self.proxies = []
        self.test_url = 'https://httpbin.org/get'  # The url for checking the proxy

    def get_proxies(self):
        res = requests.get('https://www.free-proxy-list.net/')
        soup = BeautifulSoup(res.text, 'html.parser')
        for row in soup.select('#proxylisttable tbody tr'):
            proxy = {
                'ip':   row.select_one('td').text,
                'port': row.select_one('.hx').text
            }
            if self.check_proxy(proxy):  # check the proxy
                self.proxies.append(proxy)

    def check_proxy(self, proxy):
        '''
        Check the usability of the proxy
        '''
        try:
            res = requests.get(self.test_url, proxies={'http': f"http://{proxy['ip']}:{proxy['port']}"}, timeout=5)
            if res.status_code == 200:
                return True
        except:
            pass
        self.proxies.remove(proxy)
        return False

    def get_random_proxy(self):
        if not self.proxies:  # If the proxy pool is empty
            self.get_proxies()
        proxy = random.choice(self.proxies)
        if not self.check_proxy(proxy):  # If the proxy is invalid
            self.proxies.remove(proxy)
            return self.get_random_proxy()
        return proxy