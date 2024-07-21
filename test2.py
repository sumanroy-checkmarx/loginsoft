import requests
from bs4 import BeautifulSoup

with open("delta.txt","r") as file:
    data = [package.strip() for package in file.readlines() if package.strip()]


github=[]
otherDomain=[]
notfound=[]
lumatch=[]
forked=[]

for package in data[:]:
    if "." in package:
        print(f"Checking {package}")
        if "github.com" in package:
            github.append(package)
            data.remove(package)
        else:
            otherDomain.append(package)
            data.remove(package)

    else:
        lumatch.append(package)

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

print("---------------------\nLumatch Only\n---------------\n",* lumatch, sep='\n')
print("---------------------\nOther Domain\n---------------\n",* otherDomain, sep='\n')

def isFork(url) -> bool:
    response = requests.get(url)
    content = response.text
    if "forked from" in content or "Fork of" in content:
        return True
    else:
        return False
    
print("---------------------\n")
for package in github[:]:
    url="https://"+package
    print(f"Checking for fork {package}")
    if requests.get(url).status_code==404:
        gopkg="https://pkg.go.dev/"+package
        if requests.get(gopkg).status_code==404:
            notfound.append(package)
            github.remove(package)
        else:
            if isGOPackageForked(package=package):
                forked.append(package)
                github.remove(package)    max_length = max(len(packages), len(forkedList), len(package404), len(otherDomain))
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
    else:
        if isFork(url=url):
            forked.append(package)
            github.remove(package)


print("\n---------------------\n404s\n------------------------\n",* notfound, sep='\n')
print("\n---------------------\nFound\n-----------------------\n",* github, sep='\n')
print("\n---------------------\nForked\n-----------------------\n",* forked, sep='\n')      