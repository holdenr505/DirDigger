import requests
import threading
import argparse
import sys
import re
from math import ceil

parser = argparse.ArgumentParser()
parser.add_argument('threads', type=int,
                    help='Number of threads to spawn. Max is 64')
parser.add_argument('file', help='Name of wordlist file')
parser.add_argument('url', help='Url to brute force')
parser.add_argument('-e', '--extensions', nargs='+', default=[], help='File extensions to use during scan')
arguments = parser.parse_args()

urlregex = re.compile('https?://(?:www\\.)?[a-zA-Z0-9./]+')

if arguments.threads < 0 or arguments.threads > 64:
    print('Invalid number of threads, range is 0 to 64. Exiting with status code 1...')
    sys.exit(1)
if not urlregex.match(arguments.url):
    print('You entered an invalid or improperly formatted url. Exiting with status code 2...')
    sys.exit(2)

def createListFromFile(file):
    with open(file, mode='r') as listfile:
        wordlist = []

        try:
            for line in listfile.readlines():
                wordlist.append(line)
        except:
            print("An error occured while reading the file. Exiting with status code 3...")
            sys.exit(3)
    return wordlist

def divideList(list, numlists):
    wrapperlist = []
    listSize = len(list)
    step = ceil(listSize / (numlists + 1))

    for x in range(0, listSize, step):
        wrapperlist.append(list[x:x+step])

    return wrapperlist

def checkListings(baseurl, list, extensions):
    for listing in list:
        urls = []
        combinedurl = baseurl + '/' + listing[:len(listing) - 1]
        #strip newline characters
        urls.append(combinedurl)

        for extension in extensions:
            urls.append(combinedurl + extension)

        for url in urls:
            response = requests.get(url)

            if response.status_code != 404:
                print('{} found: status code {}' .format(url,
                response.status_code))
            else:
                print('{} not found' .format(url))

def main():
    wordlist = createListFromFile(arguments.file)
    if arguments.threads > 0:
        threads = []
        sublists = divideList(wordlist, arguments.threads)

        for list in sublists[1:]:
            threads.append(threading.Thread(target=checkListings, args=(arguments.url, list, arguments.extensions)))

        for thread in threads:
            thread.start()

        checkListings(arguments.url, sublists[0], arguments.extensions)

        #ensure termination of threads
        for thread in threads:
            thread.join()
    else:
        checkListings(arguments.url, wordlist, arguments.extensions)

main()