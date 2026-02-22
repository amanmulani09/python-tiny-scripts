import requests
from bs4 import BeautifulSoup
import csv

URL = "https://news.ycombinator.com/"


def get_page_data(url:str):
    
    try:
        respnose = requests.get(url)
        respnose.raise_for_status
        
        # parse html
        
        soup = BeautifulSoup(respnose.text,"html.parser")
        
        # find headline elements 
        
        headlines = soup.find_all("span",class_="titleline")
        
        # extract data 
        data = []
        for index, item in enumerate(headlines,start=1):
            title = item.get_text()
            data.append([index,title])
            
        # save to csv
        
        with open("headlines.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["No","Headline"])
            writer.writerows(data)
        print("headlines saves to csv successfullly ")
        
    except requests.exceptions.RequestException as e:
        print("error fetching website",e)
    
    except Exception as e:
        print("Something went wrong:",e)

get_page_data(URL)