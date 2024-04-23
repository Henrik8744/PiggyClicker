import json
import time
import threading
filename = "JsonFiles\PiggyPrices.json"
balance = 0
moneyPerClick = 1
moneyPerSecond = 0.1
# oppenedFile = open(filename)
# data = json.load(oppenedFile)
# for i in data:
#     print(i)
def getFile():
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: file {filename} not found. :(")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file {filename}.")

buildingData = getFile()
# buidlingUpgradesData = getFile("JsonFiles\PiggyBuildingUpgrades.json")

def click():
    global balance
    global moneyPerClick
    balance += moneyPerClick
    decide()

def perSecond():
    global balance
    while True:
        balance += moneyPerSecond
        time.sleep(1)

def decide():
    global moneyPerSecond
    print("Type 1 to click")
    print("Type 2 to buy clicker upgrades")
    print("Type 3 for buildings")
    print("Type 4 for building upgrades")
    print("Type 5 see your stats")
    print(f"You have ${balance:.2f}")
    decision = input("What would you like to do? ").strip()
    if decision == "1":
        click()
    elif decision == "3":
        print(f"${buildingData[0]["Price"]:.2f} {buildingData[0]["Name"]}: ${buildingData[0]["MPS"]:.2f}/sec (You have {buildingData[0]["Amount"]})")
        print(f"${buildingData[1]["Price"]:.2f} {buildingData[1]["Name"]}: ${buildingData[1]["MPS"]:.2f}/sec (You have {buildingData[1]["Amount"]})")
        print(f"${buildingData[2]["Price"]:.2f} {buildingData[2]["Name"]}: ${buildingData[2]["MPS"]:.2f}/sec (You have {buildingData[2]["Amount"]})")
        purchaseDecision = int(input("What would you like to buy? ").strip())
        moneyPerSecond += buildingData[purchaseDecision - 1]["MPS"]
        buildingData[purchaseDecision - 1]["Amount"] = buildingData[purchaseDecision - 1]["Amount"] + 1
        with open(filename, 'w') as buildingDataFile:
            buildingDataFile.write(str(buildingData).replace("'", '"').replace("True", "true").replace("False", "false"))
            buildingDataFile.close()
            decide()
    elif decision == "4":
        print(buildingData[0]["Name"])
        print(buildingData[1]["Name"])
        print(buildingData[2]["Name"])
        selectedBuilding = int(input("Which building would you like to get an upgrade for? ").strip())
        print(f"${buildingData[selectedBuilding - 1]["Upgrades"][0]["Price"]:.2f} {buildingData[selectedBuilding - 1]["Upgrades"][0]["Name"]}")
        print(f"${buildingData[selectedBuilding - 1]["Upgrades"][1]["Price"]:.2f} {buildingData[selectedBuilding - 1]["Upgrades"][1]["Name"]}")
        print(f"${buildingData[selectedBuilding - 1]["Upgrades"][2]["Price"]:.2f} {buildingData[selectedBuilding - 1]["Upgrades"][2]["Name"]}")
        selectedBuildingUpgrade = int(input("Which upgrade do you want? "))
        buildingData[selectedBuilding - 1]["Upgrades"][selectedBuildingUpgrade - 1]["Bought"] = True
        buildingData[selectedBuilding - 1]["MPS"] = buildingData[selectedBuilding - 1]["MPS"] * buildingData[selectedBuilding - 1]["Upgrades"][selectedBuildingUpgrade - 1]["Multiplier"]
        with open(filename, 'w') as buildingDataFile:
            buildingDataFile.write(str(buildingData).replace("'", '"').replace("True", "true").replace("False", "false"))
            buildingDataFile.close()
            decide()

    elif decision == "5":
        print(f"You have ${balance:.2f}!")
        print(f"You make ${moneyPerClick:.2f} everytime you click!")
        print(f"You make ${moneyPerSecond:.2f} every second!")
        time.sleep(6)
        decide()
    else:
        click()


perSecondThread = threading.Thread(target = perSecond)
decideThread = threading.Thread(target = decide)

perSecondThread.start()
decideThread.start()