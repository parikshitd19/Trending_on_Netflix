import requests
from bs4 import BeautifulSoup

class BSoup():
    """
    Fetch and the Beautiful Soup Object of a given URL
    """
    def __init__(self,url:str):
        self.url = url

        self.page = requests.get(url)
        
        if self.page.status_code != 200:
            raise Exception(self.page)
            
        self.soup = BeautifulSoup(self.page.text, 'html.parser')
    
    def get_soup_obj(self):
        return self.soup
