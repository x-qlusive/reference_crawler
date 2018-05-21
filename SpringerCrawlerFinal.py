import urllib.request
import csv
import sys
import codecs
import unicodedata
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

memberlistreference=["Elstermann, M.", "Gniza, R.", "Krenn, F.", "Borgert, S.", "Obermeier, S.", "Oppl, S.", "Schmidt, W.", "Singer, R.", "Turetken, O.", "Meyer, N.", "Dirndofer, M.", "Kurz, M.", "Reiner, M.", "Kindermann, H.", "Fischer, H.", "Bastarz, F.", "Strecker, F.", "Cornerlia, Z.", "Witt, C.", "Stary, C.", "Fichtenbauer, C.", "Kramm, A.", "Fleischmann, A.", "M. Elstermann","R. Gniza","F. Krenn","S. Borgert","S. Oppl","W. Schmidt","R. Singer","O. Turetken","N. Meyer","M. Dirnhofer","M. Kurz","M. Reiner","H. Kindermann","H. Fischer","F. Bastarz","F. Strecker","C. Zehbold","C. Witt","C. Stary","C. Fichtenbauer","A. Kramm","A. Fleischmann"]
memberlistauthor=["Matthes Elstermann","Reinhard Gniza","Florian Krenn","Stephan Borgert","Stefan Oppl","Werner Schmidt","Robert Singer","Oktay Turetken","Nils Meyer","Max Dirnhofer","Matthias Kurz","Martin Reiner","Herbert Kindermann","Herbert Fischer","Fritz Bastarz","Florian Strecker","Cornelia Zehbold","Christoph Witt","Christian Stary","Christian Fichtenbauer","Anton Kramm","Albert Fleischmann"]

def unescape(s):
   s = s.replace("&lt;", "<")
   s = s.replace("&gt;", ">")
   # this has to be last:
   s = s.replace("&amp;", "&")
   s = s.replace("&amp", "&")
   return s

allauthorslist=[]

for url in urls:
    response = urllib.request.urlopen(url)
    html = response.read()
    #unicode.normalize excludes invalid characters like ANSI "/xa0"
    htmlStr = unicodedata.normalize("NFKD",html.decode('utf-8'))

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
        allauthor=[]
        htmlDoi=unescape(unicodedata.normalize("NFKD",urllib.request.urlopen(item).read().decode('utf-8')))
        authorcount=findall(regexAuthor, htmlDoi)
        #collects a list of all single authors
        for i in range (len(authorcount)):
            allauthor.append(authorcount[i])
            allauthorslist.append(allauthor[i])
        authors.append(allauthor)
        places.append(findall(regexPlace,htmlDoi))
    print(authors)
    print(places)
    paperAuthor=[]
    print(authors)
    for item in authors:
        paperAuthor.append(' and '.join(item))

    #get shortened names for communitycheck
    shortauthor=[]
    for author in allauthorslist:
        shortened=author.split()[0][0]
        last=author.split()[1]
        shortauthor.append(last+', '+shortened+'.')
        shortauthor.append(last+' '+shortened+'.')
        shortauthor.append(shortened+". "+last)

    #get the publishing places
    placeCount=0
    for item in places:
        allplace=[]
        for i in range (len(item)):
            allplace.append(item[i][0]+" "+item[i][1])
            print(allplace)
        place.append(' and '.join(allplace))
        #place.append(unescape(item[0][0]+" "+item[0][1]))
        placeCount+=1
    #get the references
    linkCount=0
    for link in completeLinks:
        htmlDoi=unescape(unicodedata.normalize("NFKD",urllib.request.urlopen(link).read().decode()))
        reference=findall(regexReference,htmlDoi)
        refcount=0
        author=[]
        titleReference=[]
        yearPublishing=[]
        for ref in reference:
            invalidflag=0
            communityflag=0
            memberreference=0
            memberauthor=0
            author.append(reference[refcount][0])
            titleReference.append(reference[refcount][1])
            yearPublishing.append(reference[refcount][3])
            try:
                if ((int(yearPublishing[refcount]) > yearnow) or (int(yearPublishing[refcount]) < 1900)):
                     invalidflag=1
            except ValueError:
                invalidflag =1

            for item in shortauthor:
                if author[refcount].find(str(item))!=(-1):
                    communityflag=1

            for item in allauthorslist:
                if author[refcount].find(str(item))!=(-1):
                    communityflag=1

            for item in memberlistauthor:
                if paperAuthor[linkCount].find(str(item))!=(-1):
                    memberauthor=1

            for item in memberlistreference:
                if author[refcount].find(str(item))!=(-1):
                    memberreference=1
            for i in range (len(authors[linkCount])):
                writedata=[authors[linkCount][i],place[linkCount],publicationTitle[linkCount],year[0],author[refcount]+" "+titleReference[refcount],yearPublishing[refcount],communityflag,memberreference, memberauthor,invalidflag]
                with open("SpringerReferences.csv","a",newline='', encoding="utf-8") as csv_file:
                    csvdata = csv.writer(csv_file)
                    csvdata.writerow(writedata)
            refcount+=1
        if not reference:
            communityflag=0
            invalidflag=0
            memberreference=0
            memberauthor=0
            author.append('no Author')
            titleReference.append("no Title")
            yearPublishing.append("no Date")
            try:
                if ((int(yearPublishing[refcount]) > yearnow) or (int(yearPublishing[refcount]) < 1900)):
                    invalidflag=1
            except ValueError:
                invalidflag =1

            for item in shortauthor:
                if author[refcount].find(str(item))!=(-1):
                    communityflag=1

            for item in memberlistauthor:
                if author[refcount].find(str(item))!=(-1):
                    memberauthor=1

            for item in memberlistreference:
                if author[refcount].find(str(item))!=(-1):
                    memberreference=1

            writedata=[paperAuthor[linkCount],place[linkCount],publicationTitle[linkCount],year[0],author[refcount]+" "+titleReference[refcount],yearPublishing[refcount],communityflag,memberreference, memberauthor,invalidflag]
            with open("SpringerReferences.csv","a",newline='',encoding="utf-8") as csv_file:
                csvdata = csv.writer(csv_file)
                csvdata.writerow(writedata)

            refcount+=1
        linkCount+=1
print(allauthorslist)
