import json
import time
import threading
import sys
buildingFilename = "JsonFiles\PiggyPrices.json"
clickerFilename = "JsonFiles\ClickerUpgrades.json"
playerFilename = "JsonFiles\PlayerData.json"
guestFilename = "JsonFiles\GuestData.json"
balance = 0
moneyPerClick = 1
moneyPerSecond = 0
playerInData = None

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
playerData = getFile(playerFilename)
guestData = getFile(guestFilename)

def startThreads():
    perSecondThread = threading.Thread(target = perSecond)
    decideThread = threading.Thread(target = decide)
    perThreeMinutesThread = threading.Thread(target = perThreeMinutes)
    decideThread.start()
    perSecondThread.start()
    perThreeMinutesThread.start()

def menu():
    hasAccount = input("Do you have an account already? ")
    if hasAccount == "Yes" or hasAccount == "yes" or hasAccount == "y":
        username = input("What is the username? ")
        password = input("What is the password? ")
        for i in range(0, len(playerData)):
            if playerData[i]["Username"] == username and playerData[i]["Password"] == password:
                load(i)
            else: 
                print("Incorrect password or username")
                menu()
    elif hasAccount == "No" or hasAccount == "no" or hasAccount == "n":
        makeAccount = input("Would you like to make an account? ")
        if makeAccount == "Yes" or makeAccount == "yes" or makeAccount == "y":
            username = input("What is the username? ")
            password = input("What is the password? ")
            playerData.append({
                "Username": username,
                "Password": password,
                "Balance": 0,
                "MPS": 0,
                "MPC": 0
            })
            with open(playerFilename, 'w') as playerDataFile:
                playerDataFile.write(str(playerData).replace("'", '"').replace("True", "true").replace("False", "false"))
                playerDataFile.close()
                startThreads()
        else:
            print("Well that's too bad make one")
            time.sleep(2)
            menu()
    else:
        print("Please enter yes or no")
        time.sleep(2)
        menu()

def load(player):
    global balance
    global moneyPerClick
    global moneyPerSecond
    global playerInData
    playerInData = player
    balance = playerData[playerInData]["Balance"]
    moneyPerClick = playerData[playerInData]["MPC"]
    moneyPerSecond = playerData[playerInData]["MPS"]
    # for building in playerData[playerInData]["Buildings"]:
    #     for upgrade in building["Upgrades"]:
    #         if upgrade["Bought"] == True:
    #             buildingData[building]["Upgrades"][upgrade]["Multiplier"]
    startThreads()

def save(decision):
    if playerInData != None:
        playerData[playerInData]["Balance"] = balance
        playerData[playerInData]["MPC"] = moneyPerClick
        playerData[playerInData]["MPS"] = moneyPerSecond
        with open(playerFilename, 'w') as playerDataFile:
            playerDataFile.write(str(playerData).replace("'", '"').replace("True", "true").replace("False", "false"))
            playerDataFile.close()
            if decision == "quit":
                print("Game saved!")
                exit()
            else:
                print("Game saved!")
                time.sleep(1)
                decide()
    else:
        if decision == "quit":
            print("Sorry you don't have an account, the game will not save")
            exit()

def perSecond():
    global balance
    global moneyPerSecond
    while True:
        moneyPerSecond = ((buildingData[0]["MPS"] * playerData[playerInData]["Buildings"][0]["Amount"]) + (buildingData[1]["MPS"] * playerData[playerInData]["Buildings"][1]["Amount"]) + (buildingData[2]["MPS"] * playerData[playerInData]["Buildings"][1]["Amount"]))
        balance += moneyPerSecond
        time.sleep(1)

def perThreeMinutes():
    while True:
        time.sleep(180)
        save("Don't quit")

def decide():
    print("Type 1 to click")
    print("Type 2 to buy clicker upgrades")
    print("Type 3 for buildings")
    print("Type 4 for building upgrades")
    print("Type 5 see your stats")
    print("Type 6 to save and quit")
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
    elif decision == "6":
        save("quit")
    else:
        click()

def click():
    global balance
    global moneyPerClick
    balance += moneyPerClick
    decide()

def purchaseClickerUpgrades():
    global moneyPerClick
    for i in range(0, len(clickerData)):
        print(f"${clickerData[i]["Price"]} {clickerData[i]["Name"]} ${clickerData[i]["MPC"]}/sec (type {i + 1} to purchase)")
    try:
        purchaseDecision = int(input("What would you like to buy? ").strip())
        if playerInData != None:
            playerData[playerInData]["ClickerUpgrades"][purchaseDecision - 1]["Bought"] = True
            moneyPerClick += clickerData[purchaseDecision - 1]["MPC"]
            with open(playerFilename, 'w') as playerDataFile:
                playerDataFile.write(str(playerData).replace("'", '"').replace("True", "true").replace("False", "false"))
                playerDataFile.close()
                print("Purchase complete!")
                time.sleep(1)
                decide()
        else:
            moneyPerClick += clickerData[purchaseDecision - 1]["MPC"]
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
        for i in range(0, len(buildingData)):
            print(f"${buildingData[i]["Price"]:.2f} {buildingData[i]["Name"]}: ${buildingData[i]["MPS"]:.2f}/sec (You have {playerData[playerInData]["Buildings"][i]["Amount"]})")
        try:
            purchaseDecision = int(input("What would you like to buy? ").strip())
            numberOfPurchased = int(input("How many would you like to buy? ").strip())
            if playerInData != None:
                playerData[playerInData]["Buildings"][purchaseDecision - 1]["Amount"] = playerData[playerInData]["Buildings"][purchaseDecision - 1]["Amount"] + numberOfPurchased
                with open(playerFilename, 'w') as playerDataFile:
                    playerDataFile.write(str(playerData).replace("'", '"').replace("True", "true").replace("False", "false"))
                    playerDataFile.close()
                    decide()
            else:
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
        for i in range(0, len(buildingData)):
            print(buildingData[i]["Name"])
        try:
            selectedBuilding = int(input("Which building would you like to get an upgrade for? ").strip())
            for i in range(0, len(buildingData[selectedBuilding - 1]["Upgrades"])):
                print(f"${buildingData[selectedBuilding - 1]["Upgrades"][i]["Price"]:.2f} {buildingData[selectedBuilding - 1]["Upgrades"][i]["Name"]}")
            try:
                selectedBuildingUpgrade = int(input("Which upgrade do you want? "))
                if playerInData != None:
                    if playerData[playerInData]["Buildings"][selectedBuilding - 1]["Upgrades"][selectedBuildingUpgrade - 1]["Bought"] == False:
                        playerData[playerInData]["Buildings"][selectedBuilding - 1]["Upgrades"][selectedBuildingUpgrade - 1]["Bought"] = True
                        buildingData[selectedBuilding - 1]["MPS"] *= buildingData[selectedBuilding - 1]["Upgrades"][selectedBuildingUpgrade - 1]["Multiplier"]
                        with open(playerFilename, 'w') as playerDataFile:
                            playerDataFile.write(str(playerData).replace("'", '"').replace("True", "true").replace("False", "false"))
                            playerDataFile.close()
                            decide()
                    else:
                        print("Sorry you already bought this!")
                        time.sleep(1.5)
                        decide()
                # else:
                #     guestData[0]["Buildings"][selectedBuilding - 1]["Upgrades"][selectedBuildingUpgrade - 1]["Bought"] = True
                #     buildingData[selectedBuilding - 1]["MPS"] *= buildingData[selectedBuilding - 1]["Upgrades"][selectedBuildingUpgrade - 1]["Multiplier"]
                #     with open(guestFilename, 'w') as guestDataFile:
                #         guestDataFile.write(str(guestData).replace("'", '"').replace("True", "true").replace("False", "false"))
                #         guestDataFile.close()
                #         decide()
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