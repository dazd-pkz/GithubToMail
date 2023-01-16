import re
import json
import sys
from requests import get
from requests.auth import HTTPBasicAuth
from pystyle import *
import getpass
import os

os.system("title GTM - Github to Mail ^| By Fascicule")

def Clear():
    command = 'clear'
    if os.name in ('nt', 'dos'): 
        command = 'cls'
    os.system(command)

banner = """
   ██████╗████████╗███╗   ███╗
  ██╔════╝╚══██╔══╝████╗ ████║
  ██║  ███╗  ██║   ██╔████╔██║
  ██║   ██║  ██║   ██║╚██╔╝██║
  ╚██████╔╝  ██║   ██║ ╚═╝ ██║
   ╚═════╝   ╚═╝   ╚═╝     ╚═╝
         Github to Mail
         
"""

print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))

try:
    username = input("   > Enter username : ")
    Clear()
    print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))
    print("   > Loading...")
    targetOrganization = targetRepo = targetUser = False
    jsonOutput = {}
    response = get('https://api.github.com/users/%s/repos?per_page=100&sort=pushed' % username, auth=HTTPBasicAuth(username, '')).text
    repos = re.findall(r'"full_name":"%s/(.*?)",.*?"fork":(.*?),' % username, response)
    nonForkedRepos = []
    for repo in repos:
        if repo[1] == 'false':
            nonForkedRepos.append(repo[0])
    response = get('https://github.com/%s/%s/commits?author=%s' % (username, nonForkedRepos[0], username), auth=HTTPBasicAuth(username, '')).text
    latestCommit = re.search(r'href="/%s/%s/commit/(.*?)"' % (username, nonForkedRepos[0]), response)
    if latestCommit:
        latestCommit = latestCommit.group(1)
    commitDetails = get('https://github.com/%s/%s/commit/%s.patch' % (username, nonForkedRepos[0], latestCommit), auth=HTTPBasicAuth(username, '')).text
    email = re.search(r'<(.*)>', commitDetails)
    if email:
        email = email.group(1)
    Clear()
    print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))
    print(Colors.yellow + '   > Username : ' + Colors.white + str(nonForkedRepos[1]))
    print(Colors.yellow + '   > Commit ID : ' + Colors.white + latestCommit)
    print(Colors.yellow + '   > Repo JSON : ' + Colors.white + str(nonForkedRepos))
    print(Colors.yellow + '   > Repository : ' + Colors.white + str(nonForkedRepos[0]))
    print(Colors.yellow + '   > Email : ' + Colors.white + email + Colors.white)
except:
    Clear()
    print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))
    print(Colors.red + "   > An exception occurred" + Colors.white)
getpass.getpass("")
