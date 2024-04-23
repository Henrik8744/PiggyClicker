import json
import time
import threading
balance = 0
moneyPerClick = 1
moneyPerSecond = 0.1

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
    print("Type 1 to click")
    print("Type 2 to buy clicker upgrades")
    print("Type 3 for buildings")
    print("Type 4 for building upgrades")
    print("Type 5 to update your balance")
    print(f"You have ${balance:.2f}")
    decision = input("What would you like to do? ").strip()
    if decision == "1":
        click()
    else:
        click()


perSecondThread = threading.Thread(target = perSecond)
decideThread = threading.Thread(target = decide)

perSecondThread.start()
decideThread.start()