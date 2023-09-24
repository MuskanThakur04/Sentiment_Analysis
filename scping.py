import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

os.chdir(r'C:\Users\Satvinder Singh\Documents\Intrnshala_Assignment\Textual_Analysis')
def scrape(url_id, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    Title_name = soup.select("h1.entry-title")
    P = soup.find(class_="td-post-content tagdiv-type")
    print(url, url_id)
    with open('text_Files\\'f'{url_id}'+'.txt', "w", encoding="utf-8") as f:

        for title in Title_name:
            t = title.get_text()
            f.writelines(t)
            for par in P:
                p = par.get_text()
                print(p)
                f.writelines(p)
    f.close


def main():
    df = pd.read_excel('Input.xlsx')

    for i in range(0, 113):
        a = df["URL_ID"][i]
        b = df["URL"][i]
        scrape(a, b)


main()
