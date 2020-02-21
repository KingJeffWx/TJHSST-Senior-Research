
import urllib
from bs4 import BeautifulSoup




def scrape_budgets():
    #start = time.time()
    url_id = 101
    table_rows = []
    while url_id <= 5401:
        
        current_url = "http://www.the-numbers.com/movie/budgets/all/" + str(url_id)
        content = urllib.request.urlopen(current_url).read()

        
        soup = BeautifulSoup(content, "html5lib")
        for node in soup.findAll('td'):
            table_rows.append(''.join(node.findAll(text=True)))
            
        url_id += 100
    i = 0
    while i < len(table_rows):
        movie_budgets[i] = [table_rows[i+1], table_rows[i+2], table_rows[i+3], table_rows[i+4], table_rows[i+5]]
        # for each: release date, movie title, budget, domestic, worldwide
        i += 6
    #done = time.time()
    #elapsed = done - start
    #print(elapsed)
    
scrape_budgets()
