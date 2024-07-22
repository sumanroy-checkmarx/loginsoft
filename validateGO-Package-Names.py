import requests
import sys


# Change this
REPO_NAME="https://github.com/hashicorp/vault"
FILE_PATH="go-package-names.txt"


packages = []
with open(FILE_PATH, "r") as file:
    for line in file:
        if "##" in line:
            line = line.strip().replace('"', "").replace("#", "").strip()
            if "." in line:
                packages.append(line)

counter=0
packageLength=len(packages)
try:
    for package in packages:
        response=requests.get(url="https://"+package,allow_redirects=True)
        counter=counter+1
        print(f"Progress {counter}/{packageLength}",end="\r")
        if response.url == REPO_NAME:
            print(f"\n[+] Redirect {package} -> https://{package}")
except Exception as e:
    print(f"Error {e}")
except KeyboardInterrupt:
    sys.exit(0)