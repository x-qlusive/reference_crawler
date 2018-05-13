import urllib.request
import requests
from urllib.request import Request
import urllib
import csv
import sys
import codecs
from re import findall
import re
from bs4 import BeautifulSoup

url2015 ="https://dl.acm.org/citation.cfm?id=2723839&preflayout=flat"
url2016 ="https://dl.acm.org/citation.cfm?id=2882879&preflayout=flat"
url2017 ="https://dl.acm.org/citation.cfm?id=3040565&preflayout=flat"
url2018 ="https://dl.acm.org/citation.cfm?id=3178248&preflayout=flat"

#avoids crawl security from ACM Digital Library
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

#appends attribute to redirected doi link to make it readable for the crawler
def doirewriter(doi):
    parse=requests.get(doi, allow_redirects=False)
    url = re.search("href=\"(.*)\"", parse.text).group(1) + "&preflayout=flat"
    return url

#replaces all the HTML character entities with utf-8
def unescape(s):
    s=BeautifulSoup(s, "lxml")
    return s

regexDOI= "doi&gt\;\<a href=\"(.*)\" title"
regexYear="\> (\d\d\d\d) Proceeding"

#author in part 1 and place in part 2
regexAuthor="Page\">(.*?)<.*?<small>(.*?)<"
# author and puplication in place 1 and year in place 2
regexReference="""(\d|\d\d)\n.*?<div>\n(<a.href=.*?>|.*?)(.*?)(\d\d\d\d|<\/div>)"""

opener=AppURLopener()
response = opener.open(url2015)
html = response.read()
htmlStr = html.decode()
htmlStr=unescape(htmlStr)
#get the DOI links of the different papers per conference
doilinks = findall(regexDOI, str(htmlStr))
completeLinks=[]
for item in doilinks:
    completeLinks.append(doirewriter(item))

#get the year of the conference
year=findall(regexYear, str(htmlStr))
htmlarticleauthor=[]
htmlreferencesdata=[]
htmlreferences=[]
for item in completeLinks:
    htmlDoi=unescape(opener.open(item).read().decode())
    htmlauthors=re.search(r"Full.Text:(.*?)Bibliometrics:", str(htmlDoi), re.DOTALL).group(1)
    htmlarticleauthor.append(re.findall("(Authors:|Author:)(.*?)Published.by", htmlauthors, re.DOTALL))
    htmlreferences.append(re.findall("REFERENCES(.*)CITED", str(htmlDoi), re.DOTALL))
    #print(htmlreferences)
    #htmlreferences=re.search(r"REFERENCES(.*)CITED", str(htmlDoi), re.DOTALL).group(1)
authors=[]
authorcount=0
#get the authors of the articles
for item in htmlarticleauthor:
    authors.append(re.findall(regexAuthor,str(item),re.DOTALL))
#    print("Article No.: "+str(authorcount+1))
#    for i in range (len(authors[authorcount])):
#        print("Author: "+authors[authorcount][i][0]+" Place: "+authors[authorcount][i][1])
    authorcount+=1
references=[]
referencecount=0
#get the authors and titles and the year of the publication
for item in htmlreferences:
    references.append(re.findall(regexReference, str(item[0]), re.DOTALL))
    #print("Reference No.: " + str(referencecount+1))
    #print(references)
    #print("Authors and Title: "+references[referencecount][0][2])
    #print("Year: "+references[referencecount][0][3 ])
    referencecount+=1
linkcount=0
referencecount=0
for link in completeLinks:
    print(str(linkcount+1))
    #print(references)
    for reference in references[linkcount]:
        print(str(referencecount+1))
        for i in range(len(authors[linkcount])):
            print(authors[linkcount][i][0] +" "+authors[linkcount][i][1])
            print(reference[2])
            print(reference[3])
        referencecount+=1
    referencecount=0
    linkcount+=1


"""

#get the references
linkCount=0
for link in completeLinks:
    print('start')
    htmlDoi=urllib.request.urlopen(link).read().decode()
    reference=findall(regexReference,htmlDoi)
    refcount=0
    author=[]
    titleReference=[]
    yearPublishing=[]
    for ref in reference:
        author.append(reference[refcount][0])
        titleReference.append(reference[refcount][1])
        yearPublishing.append(reference[refcount][3])
        writedata=[paperAuthor[linkCount],place[linkCount],year[0],author[refcount],titleReference[refcount],yearPublishing[refcount]]
        with open("references.csv","a",newline='', encoding="utf-8") as csv_file:
            csvdata = csv.writer(csv_file)
            csvdata.writerow(writedata)
        refcount+=1
    if not reference:
        author.append('no Author')
        titleReference.append("no Title")
        yearPublishing.append("no Date")
        writedata=[paperAuthor[linkCount],place[linkCount],year[0],author[refcount],titleReference[refcount],yearPublishing[refcount]]
        with open("references.csv","a",newline='') as csv_file:
            csvdata = csv.writer(csv_file)
            csvdata.writerow(writedata)
    linkCount+=1
"""
