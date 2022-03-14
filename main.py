from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys
from queue import Queue
import requests
import re
import os

DIRECTORY = "Links"
text_file = "Links/links_found.txt"
# Edit these urls to test links. If you wish to traverse websites IT TAKES A LONG TIME!
# Youtube doesn't seem to work however wikipedia links and reddit and so forth seem to do just fine
# *************************************************************************************
homepage = "https://en.wikipedia.org/wiki/Croissant"
target = "https://en.wikipedia.org/wiki/Adolf_Hitler"
# *************************************************************************************
queue = []
i = 1


def get_path():
    return "Links/links_found.txt"


# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)
        create_data_files(directory)


# Create queue and crawled files (if not created)
def create_data_files(project_name):
    os.path.join(project_name, 'links_found.txt')


def fetch_links(url):
    resp = requests.get(url)
    return resp.text


def write_to_file(path, data):
    with open(path, 'a', encoding="utf-8", errors='ignore') as file:
        file.write(data + '\n')


# Read the file and create a set.
def file_to_array(file_name, passed_queue):
    found = []
    with open(file_name, 'rt') as f:
        for line in f:
            if line.replace('\n', '').__contains__('mobile'):
                break
            if line.replace('\n', '').__contains__('toggle_view_mobile'):
                break
            found.append(line.replace('\n', ''))
    for a in found:
        if a in passed_queue:
            found.remove(a)
    return found


def add_to_queue(temp_links, queue_links):
    for a in temp_links:
        queue_links.append(a)
    return queue_links


def delete_file_contents(path):
    with open(path, 'w'):
        pass


# Get the sub domain name of the url
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''


def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-3] + '.' + results[-2] + '.' + results[-1]
    except:
        return ''


# Retrieve the links from the webpage and wrtie them to a file
def get_links(url, target_u, visited_sites):
    j = 0
    he2 = ''
    doc = fetch_links(url)
    soup = BeautifulSoup(doc, 'html.parser')
    for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
        he2 = link.get('href')
        write_to_file("Links/links_found.txt", he2)
    for link in soup.find_all('a', attrs={'href': re.compile("^/")}):
        he = "https://" + get_domain_name(url) + link.get('href')
        write_to_file("Links/links_found.txt", he)
        if he == target_u or he2 == target_u:
            print("**********************************************************")
            print("*************************The Path*************************")
            print("**********************************************************")
            for i in visited_sites:
                j = j + 1
                print(j, ": ", i)
            print("*********************************************")
            print("\n" + target_u)
            sys.exit(1)


# Create a queue of links to perform a bfs search and mark the path
def bfs(start_site, target_site):
    search = ''
    link_queue = []
    visited = []
    link_queue.append(start_site)
    for x in range(80):
        for y in range(len(link_queue)):
            search = link_queue.pop(0)
            visited.append(search)
            get_links(search, target_site, visited)
            temp_queue = file_to_array("Links/links_found.txt", visited)
            temp2_queue = link_queue
            link_queue = add_to_queue(temp_queue, temp2_queue)
            # for j in link_queue:
            #     if j == target_site:
            #         print("*********************************************")
            #         print("\nTarget: "+target_site)
            #
            #         sys.exit(1)
        if search == target_site:
            break


create_project_dir(DIRECTORY)
delete_file_contents(get_path())
bfs(homepage, target)
