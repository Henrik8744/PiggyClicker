# Import necessary libraries
import json
import time
import threading
import sys

# Define file paths
buildingFilename = "PiggyClicker\JsonFiles\PiggyPrices.json"
clickerFilename = "PiggyClicker\JsonFiles\ClickerUpgrades.json"
playerFilename = "PiggyClicker\JsonFiles\PlayerData.json"
playerBackupFilename = "PiggyClicker\JsonFiles\PlayerDataBackup.json"
guestFilename = "PiggyClicker\JsonFiles\GuestData.json"

# Initialize global variables
balance = 0
moneyPerClick = 1
moneyPerSecond = 0
playerInData = None 

# Set recursion limit
sys.setrecursionlimit(999999999)

# Define function to load JSON data from a file
def getFile(filename):
    try:
        # Open and read the file
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        # Handle file not found error
        print(f"Error: file {filename} not found. :(")
    except json.JSONDecodeError:
        # Handle invalid JSON format error
        print(f"Error: Invalid JSON format in file {filename}.")

# Load data from files
buildingData = getFile(buildingFilename)
clickerData = getFile(clickerFilename)
playerData = getFile(playerFilename)
playerDataBackup = getFile(playerBackupFilename)
guestData = getFile(guestFilename)

class Menu:
    # Define global variables
    global guestData
    global playerInData

    def menu():
        global playerData
        # Ask user if they have an account
        hasAccount = input("Do you have an account already? ").lower()

        # If user has an account
        if hasAccount in ["yes", "y"]:
            username = input("What is the username? ")
            password = input("What is the password? ")

            # Check if username and password match any in the playerData
            for i in range(0, len(playerData)):
                if playerData[i]["Username"] == username and playerData[i]["Password"] == password:
                    # If match found, load the user data
                    Menu.load(i, "Normal")
                    return
                
            print("Incorrect password or username")
            Menu.menu()

        # If user does not have an account
        elif hasAccount in ["no", "n"]:
            makeAccount = input("Would you like to make an account? ").lower()

            # If user wants to make an account
            if makeAccount in ["yes", "y"]:
                username = input("What is the username? ")
                password = input("What is the password? ")

                # If playerData is None, initialize it as an empty list
                if playerData is None:
                    playerData = []

                # Now you can safely append to playerData
                playerData.append(
                    {
                        "Username": username,
                        "Password": password,
                        "Balance": 0.00,
                        "MPC": 1.00,
                        "MPS": 0.00,
                        "ClickerUpgrades": [{"Id": i, "Bought": False} for i in range(1, 7)],
                        "Buildings": [
                            {
                                "Name": building,
                                "Amount": 0,
                                "Upgrades": [{"Id": i, "Bought": False} for i in range(1, 4)]
                            } for building in ["Farm", "Butcher", "Shop"]
                        ]
                    }
                )

                playerInData = -1

                # Write playerData to file
                with open(playerFilename, 'w') as playerDataFile:
                    playerDataFile.write(str(playerData).replace("'", '"').replace("True", "true").replace("False", "false"))
                    Menu.load(playerInData, "Normal")

            # If user does not want to make an account
            else:
                print("Created guest account, you will not be able to save your progress.")
                guestData = [
                    {
                        "Balance": 0.00,
                        "MPC": 1.00,
                        "MPS": 0.00,
                        "ClickerUpgrades": [{"Id": i, "Bought": False} for i in range(1, 7)],
                        "Buildings": [
                            {
                                "Name": building,
                                "Amount": 0,
                                "Upgrades": [{"Id": i, "Bought": False} for i in range(1, 4)]
                            } for building in ["Farm", "Butcher", "Shop"]
                        ]
                    }
                ]

                # Write guestData to file
                with open(guestFilename, 'w') as guestDataFile:
                    guestDataFile.write(str(guestData).replace("'", '"').replace("True", "true").replace("False", "false"))
                time.sleep(2)
                GuestMode.startThreads()

        # If user input is not recognized
        else:
            print("Please enter yes or no")
            time.sleep(2)
            Menu.menu()

    def load(player, mode):
        global balance
        global moneyPerClick
        global moneyPerSecond
        global playerInData

        # If mode is normal, load player data
        if mode == "Normal":
            playerInData = player
            balance = playerData[playerInData]["Balance"]
            moneyPerClick = playerData[playerInData]["MPC"]
            moneyPerSecond = playerData[playerInData]["MPS"]
            NormalMode.startThreads()

class NormalMode:
    # Starts two threads, one for perSecond and one for decide
    def startThreads():
        perSecondThread = threading.Thread(target = NormalMode.perSecond)
        decideThread = threading.Thread(target = NormalMode.decide)
        decideThread.start()
        perSecondThread.start()

    # Saves the player's data and exits the game if the decision is "quit"
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
                    NormalMode.decide()
        else:
            if decision == "quit":
                print("Sorry you don't have an account, the game will not save")
                exit()

    # Increases the balance by moneyPerSecond every second
    def perSecond():
        global balance
        global moneyPerSecond
        while True:
            moneyPerSecond = ((buildingData[0]["MPS"] * playerData[playerInData]["Buildings"][0]["Amount"]) + 
                              (buildingData[1]["MPS"] * playerData[playerInData]["Buildings"][1]["Amount"]) + 
                              (buildingData[2]["MPS"] * playerData[playerInData]["Buildings"][2]["Amount"]))
            balance += moneyPerSecond
            time.sleep(1)

    # Presents the user with options and calls the corresponding function based on the user's decision
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
            NormalMode.click()
        elif decision == "2":
            NormalMode.purchaseClickerUpgrades()
        elif decision == "3":
            NormalMode.purchaseBuildings()
        elif decision == "4":
            NormalMode.purchaseBuildingUpgrades()
        elif decision == "5":
            NormalMode.checkStats()
        elif decision == "6":
            NormalMode.save("quit")
        else:
            NormalMode.click()

    # Increases the balance by moneyPerClick
    def click():
        global balance
        global moneyPerClick
        balance += moneyPerClick
        NormalMode.decide()

    # Allows the user to purchase clicker upgrades
    def purchaseClickerUpgrades():
        global moneyPerClick
        for i in range(0, len(clickerData)):
            print(f"${clickerData[i]["Price"]} {clickerData[i]["Name"]} ${clickerData[i]["MPC"]}/sec (type {i + 1} to purchase)")
        try:
            purchaseDecision = int(input("What would you like to buy? ").strip())
            if playerInData != None:
                if playerData[playerInData]["ClickerUpgrades"][purchaseDecision - 1]["Bought"] == False:
                    playerData[playerInData]["ClickerUpgrades"][purchaseDecision - 1]["Bought"] = True
                    moneyPerClick += clickerData[purchaseDecision - 1]["MPC"]
                    playerData[playerInData]["MPC"] = moneyPerClick
                    with open(playerFilename, 'w') as playerDataFile:
                        playerDataFile.write(str(playerData).replace("'", '"').replace("True", "true").replace("False", "false"))
                        playerDataFile.close()
                        print("Purchase complete!")
                        time.sleep(1)
                        NormalMode.decide()
                else:
                    print("Sorry you already bought this!")
                    time.sleep(1.5)
                    NormalMode.decide()
            else:
                moneyPerClick += clickerData[purchaseDecision - 1]["MPC"]
                NormalMode.decide()
        except ValueError:
            print("Please enter a valid number")
            time.sleep(4)
            NormalMode.purchaseClickerUpgrades()
        except IndexError:
            print("Please enter a valid number")
            time.sleep(4)
            NormalMode.purchaseClickerUpgrades()

    # Allows the user to purchase buildings
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
                        NormalMode.decide()
                else:
                    NormalMode.decide()
            except ValueError:
                print("Please enter a valid number")
                time.sleep(4)
                NormalMode.purchaseBuildings()
            except IndexError:
                print("Please enter a valid number")
                time.sleep(4)
                NormalMode.purchaseBuildings()

    # Allows the user to purchase building upgrades
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
                                NormalMode.decide()
                        else:
                            print("Sorry you already bought this!")
                            time.sleep(1.5)
                            NormalMode.decide()
                except ValueError:
                    print("Please enter a valid number")
                    time.sleep(4)
                    NormalMode.purchaseBuildingUpgrades()
                except IndexError:
                    print("Please enter a valid number")
                    time.sleep(4)
                    NormalMode.purchaseBuildingUpgrades()
            except ValueError:
                print("Please enter a valid number")
                time.sleep(4)
                NormalMode.purchaseBuildingUpgrades()
            except IndexError:
                print("Please enter a valid number")
                time.sleep(4)
                NormalMode.purchaseBuildingUpgrades()         
    
    # Displays the user's stats
    def checkStats():
            print(f"You have ${balance:.2f}!")
            print(f"You make ${moneyPerClick:.2f} everytime you click!")
            print(f"You make ${moneyPerSecond:.2f} every second!")
            time.sleep(6)
            NormalMode.decide()

class GuestMode:
    # This method starts two threads: one for per second income and one for user decisions
    def startThreads():
        perSecondThread = threading.Thread(target = GuestMode.perSecond)
        decideThread = threading.Thread(target = GuestMode.decide)
        decideThread.start()
        perSecondThread.start()

    # This method calculates the per second income based on the buildings owned and updates the balance every second
    def perSecond():
        global balance
        global moneyPerSecond
        while True:
            moneyPerSecond = ((buildingData[0]["MPS"] * guestData[-1]["Buildings"][0]["Amount"]) + (buildingData[1]["MPS"] * guestData[-1]["Buildings"][1]["Amount"]) + (buildingData[2]["MPS"] * guestData[-1]["Buildings"][2]["Amount"]))
            balance += moneyPerSecond
            time.sleep(1)

    # This method provides the user with options to interact with the game
    def decide():
        print("Type 1 to click")
        print("Type 2 to buy clicker upgrades")
        print("Type 3 for buildings")
        print("Type 4 for building upgrades")
        print("Type 5 see your stats")
        print("Type 6 to quit")
        print(f"You have ${balance:.2f}")
        decision = input("What would you like to do? ").strip()
        if decision == "1":
            GuestMode.click()
        elif decision == "2":
            GuestMode.purchaseClickerUpgrades()
        elif decision == "3":
            GuestMode.purchaseBuildings()
        elif decision == "4":
            GuestMode.purchaseBuildingUpgrades()
        elif decision == "5":
            GuestMode.checkStats()
        elif decision == "6":
            exit()
        else:
            GuestMode.click()

    # This method increases the balance by the money per click value
    def click():
        global balance
        global moneyPerClick
        balance += moneyPerClick
        GuestMode.decide()

    # This method allows the user to purchase clicker upgrades
    def purchaseClickerUpgrades():
        global moneyPerClick
        for i in range(0, len(clickerData)):
            print(f"${clickerData[i]["Price"]} {clickerData[i]["Name"]} ${clickerData[i]["MPC"]}/sec (type {i + 1} to purchase)")
        try:
            purchaseDecision = int(input("What would you like to buy? ").strip())
            if guestData[-1]["ClickerUpgrades"][purchaseDecision - 1]["Bought"] == False:
                guestData[-1]["ClickerUpgrades"][purchaseDecision - 1]["Bought"] = True
                moneyPerClick += clickerData[purchaseDecision - 1]["MPC"]
                guestData[-1]["MPC"] = moneyPerClick
                with open(guestFilename, 'w') as guestDataFile:
                    guestDataFile.write(str(guestData).replace("'", '"').replace("True", "true").replace("False", "false"))
                    guestDataFile.close()
                    GuestMode.decide()
            else:
                print("Sorry you already bought this!")
                time.sleep(1.5)
                GuestMode.decide()
        except ValueError:
            print("Please enter a valid number")
            time.sleep(4)
            GuestMode.purchaseClickerUpgrades()
        except IndexError:
            print("Please enter a valid number")
            time.sleep(4)
            GuestMode.purchaseClickerUpgrades()

    # This method allows the user to purchase buildings
    def purchaseBuildings():
            for i in range(0, len(buildingData)):
                print(f"${buildingData[i]["Price"]:.2f} {buildingData[i]["Name"]}: ${buildingData[i]["MPS"]:.2f}/sec (You have {guestData[-1]["Buildings"][i]["Amount"]})")
            try:
                purchaseDecision = int(input("What would you like to buy? ").strip())
                numberOfPurchased = int(input("How many would you like to buy? ").strip())
                guestData[-1]["Buildings"][purchaseDecision - 1]["Amount"] = guestData[-1]["Buildings"][purchaseDecision - 1]["Amount"] + numberOfPurchased
                with open(guestFilename, 'w') as guestDataFile:
                    guestDataFile.write(str(guestData).replace("'", '"').replace("True", "true").replace("False", "false"))
                    guestDataFile.close()
                    GuestMode.decide()
            except ValueError:
                print("Please enter a valid number")
                time.sleep(4)
                GuestMode.purchaseBuildings()
            except IndexError:
                print("Please enter a valid number")
                time.sleep(4)
                GuestMode.purchaseBuildings()

    # This method allows the user to purchase building upgrades
    def purchaseBuildingUpgrades():
            for i in range(0, len(buildingData)):
                print(buildingData[i]["Name"])
            try:
                selectedBuilding = int(input("Which building would you like to get an upgrade for? ").strip())
                for i in range(0, len(buildingData[selectedBuilding - 1]["Upgrades"])):
                    print(f"${buildingData[selectedBuilding - 1]["Upgrades"][i]["Price"]:.2f} {buildingData[selectedBuilding - 1]["Upgrades"][i]["Name"]}")
                try:
                    selectedBuildingUpgrade = int(input("Which upgrade do you want? "))
                    if guestData[-1]["Buildings"][selectedBuilding - 1]["Upgrades"][selectedBuildingUpgrade - 1]["Bought"] == False:
                        guestData[-1]["Buildings"][selectedBuilding - 1]["Upgrades"][selectedBuildingUpgrade - 1]["Bought"] = True
                        buildingData[selectedBuilding - 1]["MPS"] *= buildingData[selectedBuilding - 1]["Upgrades"][selectedBuildingUpgrade - 1]["Multiplier"]
                        with open(guestFilename, 'w') as guestDataFile:
                            guestDataFile.write(str(guestData).replace("'", '"').replace("True", "true").replace("False", "false"))
                            guestDataFile.close()
                            GuestMode.decide()
                    else:
                        print("Sorry you already bought this!")
                        time.sleep(1.5)
                        GuestMode.decide()
                except ValueError:
                    print("Please enter a valid number")
                    time.sleep(4)
                    GuestMode.purchaseBuildingUpgrades()
                except IndexError:
                    print("Please enter a valid number")
                    time.sleep(4)
                    GuestMode.purchaseBuildingUpgrades()
            except ValueError:
                print("Please enter a valid number")
                time.sleep(4)
                GuestMode.purchaseBuildingUpgrades()
            except IndexError:
                print("Please enter a valid number")
                time.sleep(4)
                GuestMode.purchaseBuildingUpgrades()         

    # This method allows the user to check their current stats
    def checkStats():
            print(f"You have ${balance:.2f}!")
            print(f"You make ${moneyPerClick:.2f} everytime you click!")
            print(f"You make ${moneyPerSecond:.2f} every second!")
            time.sleep(6)
            GuestMode.decide()

# Start the game
Menu.menu()