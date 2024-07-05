import requests
from prettytable import PrettyTable
from tqdm import tqdm
from sys import exit

packageList = []
FourOhFourList = []
ForkedList = []
OriginalList = []
LumatchOnly=[]

def main():
    with open("urls.txt", "r") as file:
        data = file.readlines()

    for line in data:
        line = line.strip()
        if line != "":
            packageList.append(line)

    # Initialize tqdm with the total number of packages to process
    progressBar = tqdm(total=len(packageList), desc="Checking Packages")

    for package in packageList:
        if "." in package:
            craftedURL = "https://" + package
            response = requests.get(url=craftedURL)
            if response.status_code == 404:
                goPKGURL = "https://pkg.go.dev/" + package
                delta = requests.get(url=goPKGURL)
                if delta.status_code == 404:
                    FourOhFourList.append(package)
                else:
                    OriginalList.append(package)

            elif "forked from" in response.text or "Fork of" in response.text:
                ForkedList.append(package)
            else:
                OriginalList.append(package)

        elif "." not in package:
            goPKGURL = "https://pkg.go.dev/" + package
            goPKGResponse = requests.get(url=goPKGURL)
            if goPKGResponse.status_code == 404:
                LumatchOnly.append(package)
            else:
                OriginalList.append(package)

        # Update the progress bar
        progressBar.update(1)

    progressBar.close()

    # Equalize the lengths of the lists by padding with empty strings
    maxLength = max(len(OriginalList), len(ForkedList), len(FourOhFourList), len(LumatchOnly))
    serialNumbers = list(range(1, maxLength + 1))

    OriginalList.extend([""] * (maxLength - len(OriginalList)))
    ForkedList.extend([""] * (maxLength - len(ForkedList)))
    FourOhFourList.extend([""] * (maxLength - len(FourOhFourList)))
    LumatchOnly.extend([""] * (maxLength - len(LumatchOnly)))

    table = PrettyTable()
    table.add_column("S.No", serialNumbers)
    table.add_column("Original", OriginalList)
    table.add_column("Forked", ForkedList)
    table.add_column("404", FourOhFourList)
    table.add_column("Lumatch Only",LumatchOnly)

    table.align["Original"] = "l"
    table.align["Forked"] = "l"
    table.align["404"] = "l"
    table.align["Lumatch Only"] = "l"
    print(table)

try:
    main()
except Exception as e:
    print(f"Exception {e}")
except KeyboardInterrupt:
    exit(0)
