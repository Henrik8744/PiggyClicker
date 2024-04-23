import json
import time
import threading
filename = "PiggyPrices.json"
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

data = getFile()

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
    print("Type 5 to update your balance")
    print(f"You have ${balance:.2f}")
    decision = input("What would you like to do? ").strip()
    if decision == "1":
        click()
    elif decision == "3":
        print(f"${data[0]["Price"]} {data[0]["Name"]}: ${data[0]["MPS"]:.2f}/sec (You have {data[0]["Amount"]})")
        # print(f"${data[1]["Price"]} {data[1]["Name"]}: ${data[1]["MPS"]:.2f}/sec (You have {data[1]["Amount"]})")
        # print(f"${data[2]["Price"]} {data[2]["Name"]}: ${data[2]["MPS"]:.2f}/sec (You have {data[2]["Amount"]})")
        purchaseDecision = int(input("What would you like to buy? ").strip())
        if purchaseDecision == 1:
            moneyPerSecond += data[purchaseDecision - 1]["MPS"]
            data[purchaseDecision -1 ]["Amount"] = data[purchaseDecision -1 ]["Amount"]+1
            with open(filename, 'w') as dataFile:
                dataFile.write(str(data).replace("'", '"'))
                dataFile.close()
                decide()
    else:
        click()


perSecondThread = threading.Thread(target = perSecond)
decideThread = threading.Thread(target = decide)

perSecondThread.start()
decideThread.start()