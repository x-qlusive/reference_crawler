import urllib.request
import csv
import sys
import codecs
from re import findall
import re
url2009 = "https://link.springer.com/book/10.1007/978-3-642-15915-2"
url2010 = "https://link.springer.com/book/10.1007/978-3-642-23135-3"
url2011 ="https://link.springer.com/book/10.1007/978-3-642-23471-2"
url2012 ="https://link.springer.com/book/10.1007/978-3-642-29133-3"
url20122="https://link.springer.com/book/10.1007/978-3-642-29294-1"
url2013 ="https://link.springer.com/book/10.1007/978-3-642-36754-0"
url2014 ="https://link.springer.com/book/10.1007/978-3-319-06065-1"
url20142="https://link.springer.com/book/10.1007/978-3-319-06191-7"

#set this variable to the actual year to filter invalid years
yearnow=2018
urls=[url2009, url2010, url2011, url2012, url20122, url2013, url2014, url20142]
regexDOI= "gtm-chapter-link\" href=\"(.*?)\">"
regexYear="ConferenceAcronymAndYear\">S-BPM ONE (\d\d\d\d)"
regexTitle="title>(.*?) [|]"
regexAuthor="authors-affiliations__name\">(.*?)<"
regexPlace="affiliation__item\"><.*?affiliation__.*?>(.*?)<.*?affiliation__.*?>(.*?)<"
regexReference="CitationContent.*?>(.*?):.(.*?)([.(]|, <|, v|<s).*?(\d\d\d\d)"
regexPublicationTitle=r"div class=\"content-type-list__title\">.*?href=\".*?\">(.*?)<\/a"
addurl="https://link.springer.com"

def unescape(s):
   s = s.replace("&lt;", "<")
   s = s.replace("&gt;", ">")
   # this has to be last:
   s = s.replace("&amp;", "&")
   return s

authorscommunity=[]

for url in urls:
    response = urllib.request.urlopen(url)
    html = response.read()
    htmlStr = html.decode()

    #get the DOI links of the different papers per conference
    doilinks = findall(regexDOI, htmlStr)
    publicationTitle=re.findall(regexPublicationTitle,htmlStr,re.DOTALL)

    completeLinks=[]
    for item in doilinks:
        completeLinks.append(addurl+item)

    #get the year of the conference
    year=findall(regexYear, htmlStr)

    #get the title of the conference
    title=findall(regexTitle, htmlStr)
    print(title)

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
        memberflag=0
        communityflag=0
        htmlDoi=urllib.request.urlopen(link).read().decode()
        reference=findall(regexReference,htmlDoi)
        refcount=0
        author=[]
        titleReference=[]
        yearPublishing=[]
        for ref in reference:
            invalidflag=0
            author.append(reference[refcount][0])
            titleReference.append(reference[refcount][1])
            yearPublishing.append(reference[refcount][3])
            try:
                if ((int(yearPublishing[refcount]) > yearnow) or (int(yearPublishing[refcount]) < 1900)):
                     invalidflag=1
            except ValueError:
                invalidflag =1
            writedata=[paperAuthor[linkCount],place[linkCount],publicationTitle[linkCount],year[0],author[refcount]+" "+titleReference[refcount],yearPublishing[refcount],communityflag,memberflag,invalidflag]
            with open("SpringerReferences.csv","a",newline='', encoding="utf-8") as csv_file:
                csvdata = csv.writer(csv_file)
                csvdata.writerow(writedata)
            refcount+=1
        if not reference:
            invalidflag=0
            author.append('no Author')
            titleReference.append("no Title")
            yearPublishing.append("no Date")
            try:
                if ((int(yearPublishing[refcount]) > yearnow) or (int(yearPublishing[refcount]) < 1900)):
                    invalidflag=1
            except ValueError:
                invalidflag =1
            writedata=[paperAuthor[linkCount],place[linkCount],year[0],publicationTitle[linkCount],author[refcount]+" "+titleReference[refcount],yearPublishing[refcount],communityflag,memberflag,invalidflag]
            with open("SpringerReferences.csv","a",newline='') as csv_file:
                csvdata = csv.writer(csv_file)
                csvdata.writerow(writedata)
            refcount+=1
        linkCount+=1
