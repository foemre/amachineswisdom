import requests
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputfile",
                    help="Name of the input file that stores links, one link per line", 
                    default="quotelinks.txt", 
                    type=str, 
                    action="store")
parser.add_argument("-o", "--outputfile",
                    help="Name of the file to store quotes", 
                    default="quotes.txt", 
                    type=str, 
                    action="store")
parser.add_argument("--maxlen",
                    dest="maxlen", 
                    default=1000, 
                    type=int, 
                    action="store",
                    help="Maximum length of the quotes stored")
parser.add_argument("--minlen",
                    dest="minlen", 
                    default=0, 
                    type=int, 
                    action="store",
                    help="Minimum length of the quotes stored")

args = parser.parse_args()

lines_seen = set() # holds lines already seen

with open(args.inputfile) as inputfile:
    links = inputfile.read().splitlines()
    
with open(args.outputfile, 'w+') as quotesfile:
    for link in links:
        quotes = list()
        page = requests.get(link)
        soup =  BeautifulSoup(page.content, 'html.parser')
        for item in soup.find_all('blockquote'):
            quotes.append(item.get_text().split('.')[0])
        for item in quotes:
            if item not in lines_seen: # not a duplicate
                try:
                    if len(item) <= args.maxlen and len(item) >= args.minlen:
                        quotesfile.write("%s\n" % item)
                        lines_seen.add(item)
                except UnicodeEncodeError:
                    pass # workaround for lines with non-unicode characters