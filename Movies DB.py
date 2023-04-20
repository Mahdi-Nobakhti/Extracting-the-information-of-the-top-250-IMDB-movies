import sqlite3
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect("Imdb Movies.db")
curs = conn.cursor()
curs.execute("CREATE TABLE  IF NOT EXISTS movies(name string, year int, score real, voters int, genre string, director string, budget string, language string, rank int, country string,currency string)")
curs.execute("CREATE TABLE  IF NOT EXISTS cooperation(actor string, director string, movie_name string)")

def insert(name,year,imdb,votes,janr,kargardan,budg,lang,rank,country,currenc):
    curs.execute("INSERT INTO movies(name , year , score , voters , genre , director , budget , language , rank , country ,currency ) VALUES(?, ?, ?, ?,?,?,?,?,?,?,?)",[name,year,imdb,votes,janr,kargardan,budg,lang,rank,country,currenc])
    conn.commit()
    print("Added!!!")

x=0
for i in range(250):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    url = "https://www.imdb.com/chart/top/?sort=rk,asc&mode=simple&page=1"
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all('td',attrs=({'class':'titleColumn'}))

    url2="https://www.imdb.com"+table[x].a['href']
    response2 = requests.get(url2,headers=headers)
    soup2 = BeautifulSoup(response2.content, "html.parser")
    name = soup2.find('div',attrs=({'class':'sc-5be2ae66-1 dRYQIl'})).h1.text
    year = soup2.find('div',attrs=({'class':'sc-5be2ae66-2 jaKsxz'})).a.text
    rate = soup2.find('span',attrs=({'class':'sc-7ab21ed2-1 eUYAaq'})).text
    voters = soup2.find('div',attrs=({'class':'sc-7ab21ed2-3 iDwwZL'})).text
    genre = soup2.find('span',attrs=({'class':'ipc-chip__text'})).text
    director = soup2.find('div',attrs=({'class':'ipc-metadata-list-item__content-container'})).text
    budget = soup2.find('ul',attrs=({'class':'ipc-metadata-list ipc-metadata-list--dividers-none ipc-metadata-list--compact sc-6d4f3f8c-0 VdkJY ipc-metadata-list--base'})).li.div.label.text
    country = soup2.find_all('ul',attrs=({'class':'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base'}))
    rank=soup2.find('a',attrs=({'class':'ipc-link ipc-link--base ipc-link--inherit-color top-rated-link'})).text

    lst = [name, int(year), rate, voters, genre, director, budget, country[6].li.text, int(rank.split("#")[1]), country[4].text, str(budget)[0]]

    insert(name, int(year), rate, voters, genre, director, budget, country[6].li.text, int(rank.split("#")[1]), country[4].text, str(budget)[0])
    print("added!")
    x+=1
   