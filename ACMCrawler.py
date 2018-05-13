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
testurl ="https://doi.org/10.1145/2723839.2723840"

#avoids crawl security from ACM Digital Library
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

#appends attribute to redirected doi link to make it readable for the crawler
def doirewriter(doi):
    parse=requests.get(testurl, allow_redirects=False)
    url = re.search("href=\"(.*)\"", parse.text).group(1) + "&preflayout=flat"
    return url

#replaces all the HTML character entities with utf-8
def unescape(s):
    s=BeautifulSoup(s, "lxml")
    return s

regexDOI= "doi&gt\;\<a href=\"(.*)\" title"
regexYear="\> (\d\d\d\d) Proceeding"

# regexTitle="title>(.*?) [|]" keine Konferenztitel seit 2015
regexAuthor="<a href=\"author_page.*>(.*)<" #author musst start at index 2 to not input the conference authors
regexPlace="affiliation__item\"><.*?affiliation__.*?>(.*?)<.*?affiliation__.*?>(.*?)<"
regexReference="CitationContent.*?>(.*?):.(.*?)([.(]|, <|, v|<s).*?(\d\d\d\d)"
addurl="https://link.springer.com"

opener=AppURLopener()
testurl2=doirewriter(testurl) #testdata
response = opener.open(testurl2)
html = response.read()
htmlStr = html.decode()

htmlStr=unescape(htmlStr)

authorFiltered = re.search(r"REFERENCES(.*)CITED", str(htmlStr), re.DOTALL).group(1)

print(authorFiltered)
"""
response = urllib.request.urlopen(urlConference)

#get the DOI links of the different papers per conference
doilinks = findall(regexDOI, htmlStr)
completeLinks=[]
for item in doilinks:
    completeLinks.append(addurl+item)

#get the year of the conference
year=findall(regexYear, htmlStr)

#get the title of the conference
title=findall(regexTitle, htmlStr)

#get the authors of the papers
authors=[]
place=[]
places=[]
for item in completeLinks:
    htmlDoi=urllib.request.urlopen(item).read().decode()
    if len(findall(regexAuthor, htmlDoi)) == 1:
        authors.append(findall(regexAuthor, htmlDoi)[0])
    if len(findall(regexAuthor, htmlDoi)) >1:
        authors.append(findall(regexAuthor, htmlDoi)[0]+' and '+findall(regexAuthor, htmlDoi)[1])
    places.append(findall(regexPlace,htmlDoi))
paperAuthor=[]
for item in authors:
    paperAuthor.append(item)
#get the publishing places
placeCount=0
for item in places:
    place.append(unescape(item[0][0]+" "+item[0][1]))
    placeCount+=1
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
