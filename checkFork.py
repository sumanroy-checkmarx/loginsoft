import requests
from prettytable import PrettyTable
import os
import sys
from bs4 import BeautifulSoup


# Main Package List

github=[]
package404 = []
forkedList = []
otherDomain = []
lumatchPackage = []


def isGOPackageForked(package) -> bool:
    goPKGURL = "https://pkg.go.dev/" + package
    soup = BeautifulSoup(requests.get(goPKGURL).text, 'html.parser')
    unit_meta_repo = soup.find('div', class_='UnitMeta-repo')
    if unit_meta_repo:
        link = unit_meta_repo.find('a')
        if link and 'href' in link.attrs:
            url = link['href']
            content = requests.get(url).text
            return "forked from" in content or "Fork of" in content
    return False

def isFork(url) -> bool:
    response = requests.get(url)
    content = response.text
    if "forked from" in content or "Fork of" in content:
        return True
    else:
        return False
    

def main(filename):
        # Get the list of packages
    with open(filename, "r") as file:
        data = [package.strip() for package in file.readlines() if package.strip()]
        
    for package in data[:]:
        if "." in package:
            if "github.com" in package:
                github.append(package)
                data.remove(package)
            else:
                otherDomain.append(package)
                data.remove(package)
        else:
            lumatchPackage.append(package)
    
    counter=0
    githubListLength=len(github)
    for package in github[:]:
        url="https://"+package
        counter=counter+1
        print(f"Checking for fork {counter}/{githubListLength}",end="\r")
        if requests.get(url).status_code==404:
            gopkg="https://pkg.go.dev/"+package
            if requests.get(gopkg).status_code==404:
                package404.append(package)
                github.remove(package)
            else:
                if isGOPackageForked(package=package):
                    forkedList.append(package)
                    github.remove(package)
                    
        else:
            if isFork(url=url):
                forkedList.append(package)
                github.remove(package)
                
    table=PrettyTable()
    max_length = max(len(github), len(forkedList), len(package404), len(otherDomain), len(lumatchPackage))
    github.extend([""] * (max_length - len(github)))
    forkedList.extend([""] * (max_length - len(forkedList)))
    package404.extend([""] * (max_length - len(package404)))
    otherDomain.extend([""] * (max_length -len(otherDomain)))
    lumatchPackage.extend([""] * (max_length - len(lumatchPackage)))

    table = PrettyTable()
    table.add_column("Original", github)
    table.add_column("Forked", forkedList)
    table.add_column("404", package404)
    table.add_column("Other Domain",otherDomain)
    table.add_column("Lumatch",lumatchPackage)

    table.align["Original"]="l"
    table.align["Forked"]="l"
    table.align["404"]="l"
    table.align["Other Domain"]="l"
    table.align["Lumatch"]="l"

    print(table)

if __name__ == '__main__':
    try:
        filename = "urls.txt" if len(sys.argv) <= 1 else sys.argv[1]
        if os.path.isfile(filename):
            main(filename=filename)
        else:
            print("Please provide a file containing package names/domains")
            exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
    except KeyboardInterrupt:
        sys.exit(0)
        