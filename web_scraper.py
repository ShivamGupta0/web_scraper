"""
web_scraper with main assignment as well as bonus tasks
"""
import requests
from bs4 import BeautifulSoup
import os
import urllib.request
def month_number(month):
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    return months.index(month) + 1
def month_name (number):
    if number == 1:
        return "january"
    elif number == 2:
        return "february"
    elif number == 3:
        return "march"
    elif number == 4:
        return "april"
    elif number == 5:
        return "may"
    elif number == 6:
        return "june"
    elif number == 7:
        return "july"
    elif number == 8:
        return "august"
    elif number == 9:
        return "september"
    elif number == 10:
        return "october"
    elif number == 11:
        return "november"
    elif number == 12:
        return "december"
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
def download(url,name,author):
    urllib.request.urlretrieve(url, str(name)+"-"+str(author)+".png")

def comic_opener(URL,destination,author):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'}
    r = requests.get(URL,headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.findAll('div', attrs = {'class':'small-3 medium-3 large-3 columns'})
    urls=[]
    for row in table:
        new_url=row.a['href']
        urls.append(new_url)
    for url in urls:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'}
        r = requests.get('http://explosm.net'+str(url),headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        table = soup.find('div', attrs = {'id':'comic-wrap'})
        img=table.img['src']
        Table=soup.find('div',attrs={'id':'comic-author'})
        name=Table.br.previous_sibling
        print('downloading comic dated '+name[1:]+' by '+author)
        download('http:'+img,name[1:],author)
def random_comic(URL):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'}
    r = requests.get(URL,headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    table=soup.find('div',attrs={'class':'rcg-panels'})
    urls=[]
    row=table.findAll('img')
    for Table in row :
        urls.append(str(Table)[17:68])
    for i in range(len(urls)):
        print('downloading random comic frame '+str(i+1))
        download(urls[i],'frame'+str(i+1),'')
def latest_comic(URL,n):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'}
    r = requests.get(URL,headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.findAll('div', attrs = {'class':'small-3 medium-3 large-3 columns'})
    urls=[]
    for row in table:
        new_url=row.a['href']
        urls.append(new_url)
        if len(urls)==int(n):
            break
    for url in urls:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'}
        r = requests.get('http://explosm.net'+str(url),headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        table = soup.find('div', attrs = {'id':'comic-wrap'})
        img=table.img['src']
        Table=soup.find('div',attrs={'id':'comic-author'})
        name=Table.br.previous_sibling
        Name=Table.br.next_sibling
        print('downloading comic dated '+name[1:]+' by '+str(Name[1:]))
        Sname=(str(Name[1:]).split())[1]
        download('http:'+img,name[1:],Sname)   
f=open('input.txt','r')
lines=f.readlines()
f.close()
if lines[0]=='Random':
    createFolder('./random/')
    os.chdir('./random/')
    random_comic('http://explosm.net/rcg')
elif (lines[0].split())[0]=='latest':
    createFolder('./latest/')
    os.chdir('./latest/')
    n=lines[0].split()[1]
    latest_comic('http://explosm.net/comics/archive',n)    
else:
    start=lines[0].split()
    end=lines[1].split()
    authors=lines[2].split()
    Smonth=start[0]
    Syear=start[1]
    Emonth=end[0]
    Eyear=end[1]
    if Syear==Eyear:
        createFolder('./'+Syear+'/')
        for month in range(month_number(Smonth),month_number(Emonth)+1):
            os.chdir('./'+Syear+'/')
            createFolder('./'+(str(month_name(month)))+'/')
            os.chdir('./'+(str(month_name(month)))+'/')
            for author in authors:
                comic_opener("http://explosm.net/comics/archive/"+str(Syear)+"/"+str(month)+"/"+str(author),os.getcwd(),author)
            os.chdir("..")
        os.chdir("..")
    else:    
        createFolder('./'+Syear+'/')
        os.chdir('./'+Syear+'/')
        for month in range(month_number(Smonth),13):
            createFolder('./'+(str(month_name(month)))+'/')
            os.chdir('./'+(str(month_name(month)))+'/')
            for author in authors:
                comic_opener("http://explosm.net/comics/archive/"+str(Syear)+"/"+str(month)+"/"+str(author),os.getcwd(),author)
            os.chdir("..")
        os.chdir("..")
        createFolder('./'+Eyear+'/')
        os.chdir('./'+Eyear+'/')
        for month in range(1,month_number(Emonth)+1):
            createFolder('./'+(str(month_name(month)))+'/')
            os.chdir('./'+(str(month_name(month)))+'/')
            for author in authors:
                comic_opener("http://explosm.net/comics/archive/"+str(Eyear)+"/"+str(month)+"/"+str(author),os.getcwd(),author)
            os.chdir("..")
        os.chdir("..")
        for year in range(int(Syear)+1,int(Eyear)):
            createFolder('./'+str(year)+'/')
            os.chdir('./'+str(year)+'/')
            for month in range(1,13):
                createFolder('./'+(str(month_name(month)))+'/')
                os.chdir('./'+(str(month_name(month)))+'/')
                for author in authors:
                    comic_opener("http://explosm.net/comics/archive/"+str(year)+"/"+str(month)+"/"+str(author),os.getcwd(),author)
                os.chdir("..")
            os.chdir("..")
                 
    
 


        
    
