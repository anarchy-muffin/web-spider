import HTMLParser
import urllib2
import parser

#make class LinkParser that inherits methods from
#HTMLParser which is why its passed to LinkParser definition.

#This is a function that HTMLParser normally has
#but we add functionality to it.
def handle_starttag(self, tag, attrs):
        #looking for the beginning of a link
        # <a href="www.exampleurl.com"></a>
    if tag == 'a':
        for (key, value) in attrs:
            if key == 'href':
                #grabbing URL(s) and adding
                #base URL to it. For example:
                #www.example.com is the base and
                #newpage.html is the new URL (a relative URL)
                #
                #Combining a relative URL with the base HTML page
                #to create an absolute URL like: 
                #www.example.com/newpage.html
                newURL = parse.urljoin(self.baseUrl, value)
                #add it to collection of links:
                self.links = self.links + [newUrl]

#New function to get links that 
#spider() function will call
def get_links(self, url):
    self.links = []
    #Remember base URL which will be important
    #when creating absolute URLs
    self.baseUrl = url
    #use urlopen function from standard Python3 library
    response = urlopen(url)
    #Make sure you're looking @ HTML only!! 
    #(No CSS, JavaScript, etc...)
    if response.getheader('Content-Type')=='text/html':
        htmlBytes = response.read()
        #note that feed() handles strings well but not bytes
        #A change from Python2.x to 3.x
        htmlString = htmlBytes.decode("utf-8")
        self.feed(htmlString)
        return htmlString, self.links
    else:
            return "",[]

#This is the actual "spider" porton of the webspider (Hooray!)
#it takes a URL, a word to find, and a number of pages to search
#before giving up.
def spider(url, word, maxPages):
    pagesToVisit = [url]
    numberVisited = 0
    foundWord = False
    #above is the main loop creates a link parser and grabs all
    #links on the page, also searching through the page for the
    #desired quote or string, in getLinks function we return the page.
    #(helps with where to go next)
    while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
        numberVisited = numberVisited +1
        #Start from the beginning of our collection of pages
        url = pagesToVisit[1:]
        try :
            print (numberVisited, "Visiting: ", url) 
            parser = LinkParser()
            data, links = parser.getlinks(url)
            if data.find(word)>-1:
                foundWord = True
                #Adds pages we found to end of the collection
                #of pages to visit.
                pagesToVisit = pagesToVisit + links
                print ("**SUCCESS**")
        except:
                print ("**FAILED**")
    if foundWord:
        print "The word", word, "was found at:" , url
    else:
        print "Word not found."
