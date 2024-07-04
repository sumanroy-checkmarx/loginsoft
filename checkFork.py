import requests
from prettytable import PrettyTable
from tqdm import tqdm
from sys import exit

packageList = []
FourOhFourList = []
ForkedList = []
OriginalList = []

def main():
    with open("urls.txt", "r") as file:
        data = file.readlines()

    for line in data:
        line = line.strip()
        if line != "":
            packageList.append(line)

    # Initialize tqdm with the total number of packages to process
    progress_bar = tqdm(total=len(packageList), desc="Processing Packages")

    for package in packageList:
        if "." in package:
            craftedURL = "https://" + package
            response = requests.get(url=craftedURL)
            if response.status_code == 404:
                goPKGURL = "https://pkg.go.dev/" + package
                response = requests.get(url=goPKGURL)
                if response.status_code == 404:
                    FourOhFourList.append(package)
                else:
                    OriginalList.append(package)

            if "forked from" in response.text or "Fork of" in response.text:
                ForkedList.append(package)
            else:
                OriginalList.append(package)

        elif "." not in package:
            goPKGURL = "https://pkg.go.dev/" + package
            response = requests.get(url=goPKGURL)
            if response.status_code == 404:
                FourOhFourList.append(package)
            else:
                OriginalList.append(package)

        # Update the progress bar
        progress_bar.update(1)

    progress_bar.close()

    # Equalize the lengths of the lists by padding with empty strings
    max_length = max(len(OriginalList), len(ForkedList), len(FourOhFourList))
    serialNumbers = list(range(1, max_length + 1))

    OriginalList.extend([""] * (max_length - len(OriginalList)))
    ForkedList.extend([""] * (max_length - len(ForkedList)))
    FourOhFourList.extend([""] * (max_length - len(FourOhFourList)))

    table = PrettyTable()
    table.add_column("S.No", serialNumbers)
    table.add_column("Original", OriginalList)
    table.add_column("Forked", ForkedList)
    table.add_column("404", FourOhFourList)
    table.align["Original"] = "l"
    table.align["Forked"] = "l"
    table.align["404"] = "l"
    print(table)

try:
    main()
except Exception as e:
    print(f"Exception {e}")
except KeyboardInterrupt:
    exit(0)
