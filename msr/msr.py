import os
import sys
from time import time
from collections import defaultdict
import requests
import config as conf
import re
from urllib.request import urlopen

arguments = sys.argv

if len(arguments) < 2:
    print("You must include a subcommand.")
    sys.exit()

subcommand = arguments[1]

if subcommand.lower() == 'version':
    print(conf.version)
    sys.exit()

if subcommand.lower() == 'register':
    if not len(arguments) == 3:
        sys.exit()
    url = arguments[2]
    try:
        validating = requests.get(url)
        with open('registry.txt', 'a') as registry:
            registry.write(url + '\n')
    except:
        print("Not a valid url")
    sys.exit()

if subcommand.lower() == 'measure':
    print("Website \t\t\t\t Size")
    dict = defaultdict(int)
    with open('registry.txt', 'r') as registry:
        urls = registry.readlines()
        for u in urls:
            try:
                response = requests.get(u, verify=False, timeout=None)
                # https://stackoverflow.com/questions/24688479/size-of-raw-response-in-bytes/24688721
                dict[u] = len(response.content)
                # HANNAH THIS DOESN'T WORK YET
            except:
                print(f"{u} could not be reached.")
    print("Website \t\t\t\t\t Size")
    for site in dict.keys():
        print(f"{site} \t\t {dict[site]}")
    sys.exit()

if subcommand.lower() == 'race':
    dict = defaultdict(list)
    with open('registry.txt', 'r') as registry:
        urls = registry.readlines()
        for u in urls:
            # https://regexr.com/3au3g
            domain = re.search(r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]", u)
            if domain is None:
                print("Error has occurred with url " + u)
            else:
                # https://stackoverflow.com/questions/52761225/how-to-find-load-time-of-the-website-using-python-or-javascript
                start_time = time()
                stream = urlopen(u)
                stream.read()
                end_time = time()
                stream.close()
                dict[domain.group()].append(end_time - start_time)
    print("Domain \t\t\t\t Average Load Time \t\t Number of Sites Considered")
    for domain in dict.keys():
        total_time = 0
        number = len(dict[domain])
        for timing in dict[domain]:
            total_time += timing
        avg = total_time/number
        print(f"{domain}\t\t{avg}\t\t{number}")
    sys.exit()
