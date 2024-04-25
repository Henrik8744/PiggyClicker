import json
import time
import threading
import sys
buildingFilename = "JsonFiles\PiggyPrices.json"
clickerFilename = "JsonFiles\ClickerUpgrades.json"
balance = 0
moneyPerClick = 1
moneyPerSecond = 0

sys.setrecursionlimit(999999999)

def getFile(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: file {filename} not found. :(")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file {filename}.")

buildingData = getFile(buildingFilename)
clickerData = getFile(clickerFilename)

def menu():
    global balance
    global moneyPerClick
    global moneyPerSecond
    hasAccount = input("Do you have an account already? ")
    if hasAccount == "Yes" or hasAccount == "yes" or hasAccount == "y":
        username = input("What is the username? ")
        password = input("What is the password? ")

def perSecond():
    global balance
    global moneyPerSecond
    while True:
        moneyPerSecond = ((buildingData[0]["MPS"] * buildingData[0]["Amount"]) + (buildingData[1]["MPS"] * buildingData[1]["Amount"]) + (buildingData[2]["MPS"] * buildingData[2]["Amount"]))
        balance += moneyPerSecond
        time.sleep(1)

def decide():
    print("Type 1 to click")
    print("Type 2 to buy clicker upgrades")
    print("Type 3 for buildings")
    print("Type 4 for building upgrades")
    print("Type 5 see your stats")
    print(f"You have ${balance:.2f}")
    decision = input("What would you like to do? ").strip()
    if decision == "1":
        click()
    elif decision == "2":
        purchaseClickerUpgrades()
    elif decision == "3":
        purchaseBuildings()
    elif decision == "4":
        purchaseBuildingUpgrades()
    elif decision == "5":
         checkStats()
    else:
        click()

def click():
    global balance
    global moneyPerClick
    balance += moneyPerClick
    decide()

def purchaseClickerUpgrades():
    global moneyPerClick
    print(f"${clickerData[0]["Price"]} {clickerData[0]["Name"]} ${clickerData[0]["MPC"]}/sec")
    print(f"${clickerData[1]["Price"]} {clickerData[1]["Name"]} ${clickerData[1]["MPC"]}/sec")
    print(f"${clickerData[2]["Price"]} {clickerData[2]["Name"]} ${clickerData[2]["MPC"]}/sec")
    print(f"${clickerData[3]["Price"]} {clickerData[3]["Name"]} ${clickerData[3]["MPC"]}/sec")
    print(f"${clickerData[4]["Price"]} {clickerData[4]["Name"]} ${clickerData[4]["MPC"]}/sec")
    print(f"${clickerData[5]["Price"]} {clickerData[5]["Name"]} ${clickerData[5]["MPC"]}/sec")
    try:
        purchaseDecision = int(input("What would you like to buy? ").strip())
        clickerData[purchaseDecision - 1]["Bought"] = True
        moneyPerClick += clickerData[purchaseDecision - 1]["MPC"]
        with open(clickerFilename, 'w') as clickerDataFile:
            clickerDataFile.write(str(clickerData).replace("'", '"').replace("True", "true").replace("False", "false"))
            clickerDataFile.close()
            print("Purchase complete!")
            time.sleep(1.5)
            decide()
    except ValueError:
        print("Please enter a valid number")
        time.sleep(4)
        purchaseClickerUpgrades()
    except IndexError:
        print("Please enter a valid number")
        time.sleep(4)
        purchaseClickerUpgrades()

def purchaseBuildings():
        print(f"${buildingData[0]["Price"]:.2f} {buildingData[0]["Name"]}: ${buildingData[0]["MPS"]:.2f}/sec (You have {buildingData[0]["Amount"]})")
        print(f"${buildingData[1]["Price"]:.2f} {buildingData[1]["Name"]}: ${buildingData[1]["MPS"]:.2f}/sec (You have {buildingData[1]["Amount"]})")
        print(f"${buildingData[2]["Price"]:.2f} {buildingData[2]["Name"]}: ${buildingData[2]["MPS"]:.2f}/sec (You have {buildingData[2]["Amount"]})")
        try:
            purchaseDecision = int(input("What would you like to buy? ").strip())
            buildingData[purchaseDecision - 1]["Amount"] = buildingData[purchaseDecision - 1]["Amount"] + 1
            with open(buildingFilename, 'w') as buildingDataFile:
                buildingDataFile.write(str(buildingData).replace("'", '"').replace("True", "true").replace("False", "false"))
                buildingDataFile.close()
                decide()
        except ValueError:
            print("Please enter a valid number")
            time.sleep(4)
            purchaseBuildings()
        except IndexError:
            print("Please enter a valid number")
            time.sleep(4)
            purchaseBuildings()


def purchaseBuildingUpgrades():
        print(buildingData[0]["Name"])
        print(buildingData[1]["Name"])
        print(buildingData[2]["Name"])
        try:
            selectedBuilding = int(input("Which building would you like to get an upgrade for? ").strip())
            print(f"${buildingData[selectedBuilding - 1]["Upgrades"][0]["Price"]:.2f} {buildingData[selectedBuilding - 1]["Upgrades"][0]["Name"]}")
            print(f"${buildingData[selectedBuilding - 1]["Upgrades"][1]["Price"]:.2f} {buildingData[selectedBuilding - 1]["Upgrades"][1]["Name"]}")
            print(f"${buildingData[selectedBuilding - 1]["Upgrades"][2]["Price"]:.2f} {buildingData[selectedBuilding - 1]["Upgrades"][2]["Name"]}")
            try:
                selectedBuildingUpgrade = int(input("Which upgrade do you want? "))
                buildingData[selectedBuilding - 1]["Upgrades"][selectedBuildingUpgrade - 1]["Bought"] = True
                buildingData[selectedBuilding - 1]["MPS"] *= buildingData[selectedBuilding - 1]["Upgrades"][selectedBuildingUpgrade - 1]["Multiplier"]
                with open(buildingFilename, 'w') as buildingDataFile:
                    buildingDataFile.write(str(buildingData).replace("'", '"').replace("True", "true").replace("False", "false"))
                    buildingDataFile.close()
                    decide()
            except ValueError:
                print("Please enter a valid number")
                time.sleep(4)
                purchaseBuildingUpgrades()
            except IndexError:
                print("Please enter a valid number")
                time.sleep(4)
                purchaseBuildingUpgrades()
        except ValueError:
            print("Please enter a valid number")
            time.sleep(4)
            purchaseBuildingUpgrades()
        except IndexError:
            print("Please enter a valid number")
            time.sleep(4)
            purchaseBuildingUpgrades()
             
 
def checkStats():
        print(f"You have ${balance:.2f}!")
        print(f"You make ${moneyPerClick:.2f} everytime you click!")
        print(f"You make ${moneyPerSecond:.2f} every second!")
        time.sleep(6)
        decide()

menu()

perSecondThread = threading.Thread(target = perSecond)
decideThread = threading.Thread(target = decide)

perSecondThread.start()
decideThread.start()