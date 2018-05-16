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
yearnow=2018
urls=[url2015, url2016, url2017, url2018]
#authors of the previous conferences from 2009 to 2014 from SpringerCrawlerRebuild
allauthorslist =['Lutz Heuser', 'Hagen Buchwald', 'Christian Fichtenbauer', 'Werner Schmidt', 'Christian Stary', 'Robert Singer', 'Erwin Zinser', 'Erwin Aitenbichler', 'Stephan Borgert', 'Albert Fleischmann', 'Anton Kramm', 'Gabriele Konjack', 'Hagen Buchwald', 'Christian Stary', 'Ayelt Komus', 'Erwin Aitenbichler', 'Stephan Borgert', 'Max Mühlhäuser', 'Oliver Kopp', 'Lasse Engler', 'Tammo van Lessen', 'Frank Leymann', 'Jörg Nitzsche', 'Matthias Kurz', 'Albert Fleischmann', 'Nils Meyer', 'Thomas Feiner', 'Markus Radmayr', 'Dominik Blei', 'Albert Fleischmann', 'Konrad Walser', 'Marc Schaffroth', 'Alexander Sellner', 'Erwin Zinser', 'Jörg Rodenhagen', 'Florian Strecker', 'Stephan H. Sneed', 'Peter Kesch', 'Yuliya Stavenko', 'Alexander Gromoff', 'Thomas J. Olbrich', 'Albert Fleischmann', 'Robert Singer', 'Erwin Zinser', 'Christian Stary', 'Stefan Oppl', 'Johannes Kröckel', 'Bernd Hilgarth', 'Gregor Back', 'Klaus Daniel', 'Matthias Neubauer', 'Christian Stary', 'Christian Herrmann', 'Matthias Kurz', 'David Bonaldi', 'Alexandra Totter', 'Eva Pinter', 'Fritz Bastarz', 'Patrick Halek', 'Stefan Reinheimer', 'Hans-Günter Lindner', 'Matthias Kurz', 'Thomas Schaller', 'Dominik Reichelt', 'Michael Ferschl', 'Andreas Hufgard', 'Eduard Gerhardt', 'Nils Meyer', 'Markus Radmayr', 'Richard Heininger', 'Thomas Rothschädl', 'Albert Fleischmann', 'Stephan Borgert', 'Joachim Steinmetz', 'Max Mühlhäuser', 'Shinji Nakamura', 'Toshihiro Tan', 'Takeshi Hirayama', 'Hiroyuki Kawai', 'Shota Komiyama', 'Sadao Hosaka', 'Minoru Nakamura', 'Katsuhiro Yuki', 'Egon Börger', 'Thomas Rothschädl', 'Alexander Lawall', 'Thomas Schaller', 'Dominik Reichelt', 'Martina Augl', 'Matthias Neubauer', 'Albert Fleischmann', 'Robert Gottanka', 'Nils Meyer', 'Matthias Lohrmann', 'Manfred Reichert', 'Matthias Kurz', 'Gunnar Billing', 'Karl Hettling', 'Holger von Jouanne-Diedrich', 'Dominik Wachholder', 'Stefan Oppl', 'Clemens Krauthausen', 'Harald Müller', 'James E. Weber', 'Werner Schmidt', 'Paula S. Weber', 'Albert Fleischmann', 'Werner Schmidt', 'Christian Stary', 'Thomas J. Olbrich', 'Norbert Kaiser', 'Matthes Elstermann', 'Detlef Seese', 'Stefan Obermeier', 'Thomas Keller', 'Uwe Brunner', 'Katharina Schiefer', 'Edith Stary', 'Norbert Graef', 'Nils Tölle', 'Oliver Schöll', 'Detlef Seese', 'Stephan Sneed', 'Hessah AlSalamah', 'Alex Gray', 'David Morrey', 'Florian Strecker', 'Robert Singer', 'Matthias Teller', 'Matthias Kurz', 'Sebastian Huber', 'Bernd Hilgarth', 'Richard Heininger', 'Georg Weichhart', 'Fritz Bastarz', 'Patrick Halek', 'Ricarda Vierlinger', 'Max Dirndorfer', 'Barbara Handy', 'Josef Schneeberger', 'Herbert Fischer', 'Uwe V. Riss', 'Doris Weitlaner', 'Jens Kolb', 'Manfred Reichert', 'Barbara Weber', 'Clemens Krauthausen', 'Alexander Lawall', 'Thomas Schaller', 'Dominik Reichelt', 'Oktay Turetken', 'Onur Demirors', 'Doris Weitlaner', 'Annemarie Guettinger', 'Markus Kohlbacher', 'Kai Michael Höver', 'Stephan Borgert', 'Max Mühlhäuser', 'Matthes Elstermann', 'Zhili Zhao', 'Adrian Paschke', 'Matthias Kurz', 'Albert Fleischmann', 'Matthias Lederer', 'Sebastian Huber', 'Michael Götzfried', 'Michael Guppenberger', 'Maximilian Reiter', 'Frank Plechinger', 'Cornelia Zehbold', 'Werner Schmidt', 'Albert Fleischmann', 'Barbara Handy', 'Max Dirndorfer', 'Josef Schneeberger', 'Herbert Fischer', 'Jürgen Hirsch', 'Torsten Greiner', 'Sebastian Huber', 'Adrian Hauptmann', 'Matthias Lederer', 'Matthias Kurz', 'Max Dirndorfer', 'Herbert Fischer', 'Stephan Sneed', 'Udo Kannengiesser', 'Harald Müller', 'Georg Weichhart', 'Dominik Wachholder', 'Stephan Borgert', 'Max Mühlhäuser', 'Kai Michael Höver', 'Max Mühlhäuser', 'Başak Çakar', 'Onur Demirörs', 'Patrick Garon', 'Arnd Neumann', 'Frank Bensberg', 'Alexander Lawall', 'Thomas Schaller', 'Dominik Reichelt', 'Anton Ivaschenko', 'Matthias Kurz', 'Matthias Lederer', 'Davut Çulha', 'Ali Doğru', 'Vadim Agievich', 'Kirill Skripkin', 'Udo Kannengiesser', 'Stephan Borgert', 'Max Mühlhäuser', 'Thomas Müllerleile', 'Volker Nissen', 'Stefan Oppl', 'Thomas Rothschädl', 'Boris Sobočan', 'Nils Meyer', 'Christoph Fleischmann', 'Udo Kannengiesser', 'Alexandra Totter', 'David Bonaldi', 'Murat Salmanoğlu', 'Onur Demirörs', 'Oktay Türetken', 'Matthias Lederer', 'Matthias Kurz', 'Ulricke Lembcke', 'Christoph Fleischmann', 'Gerhard Stein', 'Andreas Fink', 'Simon Vogt', 'Matthes Elstermann', 'Jivka Ovtcharova', 'Matthes Elstermann', 'Jivka Ovtcharova', 'Eray Uluhan', 'Mehmet N. Aydin', 'Ramtin Mesbahipour', 'André Nursinski', 'Michael Spiller', 'Christoph Piller', 'DI Walter Wölfel', 'Kai Michael Höver', 'Max Mühlhäuser', 'Georg Weichhart', 'Johanna Pirker', 'Christian Gütl', 'Christian Stary']
#memberlist to compare with publishing authors
memberlistreference=["Elstermann, M.", "Gniza, R.", "Krenn, F.", "Borgert, S.", "Obermeier, S.", "Oppl, S.", "Schmidt, W.", "Singer, R.", "Turetken, O.", "Meyer, N.", "Dirndofer, M.", "Kurz, M.", "Reiner, M.", "Kindermann, H.", "Fischer, H.", "Bastarz, F.", "Strecker, F.", "Cornerlia, Z.", "Witt, C.", "Stary, C.", "Fichtenbauer, C.", "Kramm, A.", "Fleischmann, A."]
#memberlist to comapre with referenced authors
memberlistauthor=["Matthes Elstermann","Reinhard Gniza","Florian Krenn","Stephan Borgert","Stefan Oppl","Werner Schmidt","Robert Singer","Oktay Turetken","Nils Meyer","Max Dirnhofer","Matthias Kurz","Martin Reiner","Herbert Kindermann","Herbert Fischer","Fritz Bastarz","Florian Strecker","Cornelia Zehbold","Christoph Witt","Christian Stary","Christian Fichtenbauer","Anton Kramm","Albert Fleischmann"]


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

for url in urls:
    opener=AppURLopener()
    response = opener.open(url)
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
    title=[]
    for item in completeLinks:
        htmlDoi=unescape(opener.open(item).read().decode())
        htmlauthors=re.search(r"Full.Text:(.*?)Bibliometrics:", str(htmlDoi).replace("&amp;","&"), re.DOTALL).group(1)
        htmlarticleauthor.append(re.findall("(Authors:|Author:)(.*?)Published.by", htmlauthors, re.DOTALL))
        htmlreferences.append(re.findall("REFERENCES(.*)CITED", str(htmlDoi).replace("&amp;","&"), re.DOTALL))
        title.append(re.findall("<title>(.*)<\/title>", str(htmlDoi).replace("&amp;","&")))
        #print(htmlreferences)
        #htmlreferences=re.search(r"REFERENCES(.*)CITED", str(htmlDoi), re.DOTALL).group(1)
    authors=[]
    authorcount=0
    print(title)
    #get the authors of the articles
    for item in htmlarticleauthor:
        authors.append(re.findall(regexAuthor,str(item),re.DOTALL))
        authorcount+=1
    references=[]
    referencecount=0
    authorcount=0

    for author in authors:
        allauthorslist.append(authors[authorcount][0][0])
        authorcount+=1

    #get shortened names for communitycheck
    shortauthor=[]
    for author in allauthorslist:
        shortened=author.split()[0][0]
        last=author.split()[1]
        shortauthor.append(last+', '+shortened+'.')
        shortauthor.append(last+' '+shortened+'.')


    #for i in range (len(authors[authorcount])):
     #   authorscommunity.append(authors[authorcount[i][0]])
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
        memberflag=0
        communityflag=0
        invalidflag=0
        print("Article No.: "+str(linkcount+1))
        #print(references)
        for reference in references[linkcount]:
            print(str(referencecount+1))
            for i in range(len(authors[linkcount])):
                communityflag=0
                memberreference=0
                memberauthor=0
                invalidflag = 0
                try:
                     if ((int(reference[3]) > yearnow) or (int(reference[3])) < 1900):
                         invalidflag=1
                except ValueError:
                    invalidflag =1

                for item in shortauthor:
                    if reference[2].find(str(item))!=(-1):
                        communityflag=1

                for item in memberlistauthor:
                   if authors[linkcount][i][1].find(str(item))!=(-1):
                        memberauthor=1

                for item in memberlistreference:
                    if reference[2].find(str(item))!=(-1):
                        memberreference=1

                writedata=[authors[linkcount][i][0], authors[linkcount][i][1],title[linkcount][0],year[0],reference[2], reference[3], communityflag, memberreference, memberauthor, invalidflag]
                with open("ACMreferences.csv","a",newline='', encoding="utf-8") as csv_file:
                   csvdata = csv.writer(csv_file)
                   csvdata.writerow(writedata)
                #print(authors[linkcount][i][0] +" "+authors[linkcount][i][1])
                #print(reference[2])
                #print(reference[3])
                #print(invalidflag)
            referencecount+=1
        referencecount=0
        linkcount+=1
print(allauthorslist)
