import requests
from prettytable import PrettyTable
import os
import sys
from bs4 import BeautifulSoup

packages = []
package404 = []
forkedList = []
otherDomain = []


# Now check for 404
def getBase(package) -> str:
    parts = package.rstrip('/').split('/')

    if len(parts) > 2 and 'v' in parts[-1]:
        parts.pop()
    
    return '/'.join(parts)

def is404(package) -> bool:
    github = "https://" + package
    goPKG = "https://pkg.go.dev/" + package

    baseGithub = "https://" + getBase(package=package)
    baseGOPkg = "https://pkg.go.dev/" + getBase(package=package)

    try:
        if requests.get(github).status_code == 404:
            if requests.get(goPKG).status_code == 404:
                if requests.get(baseGithub).status_code != 404 or requests.get(baseGOPkg).status_code != 404:
                    return False
                else:
                    return True
            else:
                return False
        else:
            return False
    except requests.RequestException:
        return False


def returnHTMLContent(link):
    try:
        response = requests.get(url=link)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return ""


def isFork(url) -> bool:
    base=getBase(url)
    content = returnHTMLContent(base)
    if "forked from" in content or "Fork of" in content:
        return True
    else:
        return False

def check404():
    totalPackages = len(packages)
    progress = 0
    for package in packages[:]:
        print(f"Checking 404 Status : {progress}/{totalPackages}", end="\r")
        if is404(package=package):
            package404.append(package)
            packages.remove(package)
        progress += 1
    print()

def filterForked():
    totalPackages = len(packages)
    progress = 0
    for package in packages[:]:
        print(f"Filtering Packages : {progress}/{totalPackages}", end="\r")
        if "." in package:
            # Now check if it's a fork or not
            url="https://"+package
            if isFork(url):
                forkedList.append(package)
                packages.remove(package)
        progress += 1
    print()

def filterDomains():
    totalPackages = len(packages)
    progress = 0
    for package in packages[:]:
        print(f"Filtering Domains : {progress}/{totalPackages}", end="\r")
        if "github.com" not in package:
            otherDomain.append(package)
            packages.remove(package)
        progress += 1
    print()

def main(filename):
    # Get the list of packages
    with open(filename, "r") as file:
        data = file.readlines()

        for line in data:
            line = line.strip()
            if line != "":
                if "." in line:
                    packages.append(line)

    check404()
    filterForked()
    filterDomains()

    # Make all lists the same length
    max_length = max(len(packages), len(forkedList), len(package404), len(otherDomain))
    packages.extend([""] * (max_length - len(packages)))
    forkedList.extend([""] * (max_length - len(forkedList)))
    package404.extend([""] * (max_length - len(package404)))
    otherDomain.extend([""] * (max_length -len(otherDomain)))

    table = PrettyTable()
    table.add_column("Original", packages)
    table.add_column("Forked", forkedList)
    table.add_column("404", package404)
    table.add_column("Other Domain",otherDomain)

    table.align["Original"]="l"
    table.align["Forked"]="l"
    table.align["404"]="l"
    table.align["Other Domain"]="l"

    print(table)

try:
    filename = "urls.txt" if len(sys.argv) <= 1 else sys.argv[1]
    if os.path.isfile(filename):
        main(filename=filename)
    else:
        print("Please provide a file containing package names/domains")
        exit(0)
except KeyboardInterrupt:
    sys.exit(0)
except Exception as e:
    print(f"Exception: {e}")
