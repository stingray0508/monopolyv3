import numpy as np
import random
import sys
import os
from itertools import chain
import torch
import torch.nn.functional as F
import tkinter as tk
import time
import random
import itertools
from nn import use_nn_forward

with open("textinput", "r") as file:
    lines = file.readlines()
    number_of_players = int(lines[0].strip())
    starting_money = int(lines[1].strip())

print(number_of_players)
print(starting_money)
names = []

with open("output", "w") as file:
    pass

#window = tk.Tk()
#window.title("Monopoly Board")


# Create a canvas to draw the board


def generate_random_names(number):
    counter = 1
    while counter < number + 1:
        name = "p" + str(counter)
        names.append(name)
        counter = counter + 1


class node():
    def __init__(self, name, price, owner, rent, houseprice, house1, house2, house3, house4, hotel, mortgage, color,
                 houses, housing, maxcolor, x1, y1, x2, y2):
        self.name = name
        self.price = price
        self.owner = owner
        self.rent = rent
        self.houseprice = houseprice
        self.house1 = house1
        self.house2 = house2
        self.house3 = house3
        self.house4 = house4
        self.hotel = hotel
        self.mortgage = mortgage
        self.color = color
        self.houses = houses
        self.housing = housing
        self.maxcolor = maxcolor
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class piece():
    def __init__(self, name, square, money, properties, jail_time, jail_card, color):
        self.name = name
        self.square = square
        self.money = money
        self.properties = []
        self.jail_time = jail_time
        self.jail_card = jail_card
        self.color = color


squares = []


def setup_properties():
    # -1 is no ownner, -2 is unbuyable, -3 is no prices
    # 1 is purple, 2 is turquoise, 3 is pink, 4 is orange, 5 is red, 6 is yellow, 7 is green, 8 is blue, 9 is railroad, 10 is utility
    global squares
    squares.append(node("Start", 0, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 90, 90))
    squares.append(
        node("Mediterranean Avenue", 60, -1, 2, 50, 10, 30, 90, 160, 250, 30, 1, 0, 1, 2, 100, 10, 190, 90, ))
    squares.append(node("Community Chest", 0, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 200, 10, 290, 90))
    squares.append(node("Baltic Avenue", 60, -1, 4, 50, 20, 60, 180, 320, 450, 30, 1, 0, 1, 2, 300, 10, 390, 90))
    squares.append(node("Income Tax", 200, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 400, 10, 490, 90))
    squares.append(node("Reading Railroad", 200, -1, 0, 0, 0, 0, 0, 0, 0, 100, 9, 0, 0, 0, 500, 10, 590, 90))
    squares.append(node("Oriental Avenue", 100, -1, 6, 50, 30, 90, 270, 400, 550, 50, 2, 0, 1, 3, 600, 10, 690, 90))
    squares.append(node("Chance", 0, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 700, 10, 790, 90))
    squares.append(node("Vermont Avenue", 100, -1, 6, 50, 30, 90, 270, 400, 550, 50, 2, 0, 1, 3, 800, 10, 890, 90))
    squares.append(node("Connecticut Avenue", 120, -1, 8, 50, 40, 100, 300, 450, 600, 60, 2, 0, 1, 3, 900, 10, 990, 90))
    squares.append(node("Jail", 0, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 10, 1090, 90))
    squares.append(
        node("St. Charles Place", 140, -1, 10, 100, 50, 150, 450, 625, 750, 70, 3, 0, 1, 3, 1000, 110, 1090, 190))
    squares.append(node("Electric Company", 150, -1, 0, 0, 0, 0, 0, 0, 0, 75, 10, 0, 0, 0, 1000, 210, 1090, 290))
    squares.append(
        node("States Avenue", 140, -1, 10, 100, 50, 150, 450, 625, 750, 70, 3, 0, 1, 3, 1000, 310, 1090, 390))
    squares.append(
        node("Virginia Avenue", 160, -1, 12, 100, 60, 180, 500, 600, 900, 80, 3, 0, 1, 3, 1000, 410, 1090, 490))
    squares.append(node("Pennsylvania Railroad", 200, -1, 0, 0, 0, 0, 0, 0, 0, 100, 9, 0, 0, 0, 1000, 510, 1090, 590))
    squares.append(
        node("St. James Place", 180, -1, 14, 100, 70, 200, 550, 750, 950, 90, 4, 0, 1, 3, 1000, 610, 1090, 690))
    squares.append(node("Community Chest", 0, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 710, 1090, 790))
    squares.append(
        node("Tennessee Avenue", 180, -1, 14, 100, 70, 200, 550, 750, 950, 90, 4, 0, 1, 3, 1000, 810, 1090, 890))
    squares.append(
        node("New York Avenue", 200, -1, 16, 100, 80, 220, 600, 800, 1000, 100, 4, 0, 1, 3, 1000, 910, 1090, 990))
    squares.append(node("Free Parking", 0, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 1010, 1090, 1090))
    squares.append(
        node("Kentucky Avenue", 220, -1, 18, 150, 90, 250, 700, 875, 1050, 100, 5, 0, 1, 3, 900, 1010, 990, 1090))
    squares.append(node("Chance", 0, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 800, 1010, 890, 1090))
    squares.append(
        node("Indiana Avenue", 220, -1, 18, 150, 90, 250, 700, 875, 1050, 100, 5, 0, 1, 3, 700, 1010, 790, 1090))
    squares.append(
        node("Illinois Avenue", 240, -1, 20, 150, 100, 300, 750, 925, 1100, 120, 5, 0, 1, 3, 600, 1010, 690, 1090))
    squares.append(node("B&O Railroad", 200, -1, 0, 0, 0, 0, 0, 0, 100, 0, 10, 0, 0, 0, 500, 1010, 590, 1090))
    squares.append(
        node("Atlantic Avenue", 260, -1, 22, 150, 110, 330, 800, 957, 1150, 130, 6, 0, 1, 3, 400, 1010, 490, 1090))
    squares.append(
        node("Ventnor Avenue", 260, -1, 22, 150, 110, 330, 800, 957, 1150, 130, 6, 0, 1, 3, 300, 1010, 390, 1090))
    squares.append(node("Water Works", 150, -1, 0, 0, 0, 0, 0, 0, 0, 75, 10, 0, 0, 0, 200, 1010, 290, 1090))
    squares.append(
        node("Marvin Gardens", 280, -1, 24, 150, 120, 360, 850, 1025, 1200, 140, 6, 0, 1, 3, 100, 1010, 190, 1090))
    squares.append(node("Go To Jail", 0, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 1010, 90, 1090))
    squares.append(
        node("Pacific Avenue", 300, -1, 26, 200, 130, 390, 900, 1100, 1275, 100, 7, 0, 1, 3, 10, 910, 90, 990))
    squares.append(
        node("North Carolina Avenue", 300, -1, 26, 200, 130, 390, 900, 1100, 1275, 100, 7, 0, 1, 3, 10, 810, 90, 890))
    squares.append(node("Community Chest", 0, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 710, 90, 790))
    squares.append(
        node("Pennsylvania Avenue", 320, -1, 28, 200, 150, 450, 1000, 1200, 1400, 160, 7, 0, 1, 3, 10, 610, 90, 690))
    squares.append(node("Short Line", 200, -1, 0, 0, 0, 0, 0, 0, 0, 100, 9, 0, 0, 0, 10, 510, 90, 590))
    squares.append(node("Chance", 0, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 410, 90, 490))
    squares.append(node("Park Place", 350, -1, 35, 200, 175, 500, 1100, 1300, 1500, 175, 8, 0, 1, 2, 10, 310, 90, 390))
    squares.append(node("Luxury Tax", 100, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 210, 90, 290))
    squares.append(node("Boardwalk", 400, -1, 50, 200, 200, 600, 1400, 1700, 2000, 200, 8, 0, 1, 2, 10, 110, 90, 190))
    mortgaged = []


def color_count():
    counter = 0

    checked = []
    # need to count color types

    while counter < len(squares):
        counter = 0
        while not squares[counter].owner == -1 and not counter in checked:
            counter = counter + 1
            if not counter < len(squares):
                break
        looking_for = squares[counter].color
        counter = 0
        while counter < len(squares):
            total_count = 0
            if squares[counter].color == looking_for:
                total_count = total_count + 1
            counter = counter + 1
        counter = 0
        while counter < len(squares):
            if squares[counter].color == looking_for:
                squares[counter].maxcolor = total_count
                checked.append(counter)
            counter = counter + 1


def setup_chance():
    global chance
    chance = ["ADVANCE TO GO", "ADVANCE TO BOARDWALK", "ADVANCE TO ILLINOIS AVE", "ADVANCE TO ST. CHARLES PLACE",
              "TAKE A RIDE ON READING",
              "ADVANCE TO NEAREST RAILROAD", "ADVANCE TO NEAREST RAILROAD", "ADVANCE TO NEAREST UTILITY",
              "GO BACK 3 SPACES", "BANK PAYS YOU DIVIDEND OF 50", "YOUR BUILDING AND LOAN MATURES COLLECT 150",
              "PAY POOR TAX OF 15", "ELECTED CHAIRMAN OF BOARD PAY EACH PLAYER 50",
              "PAY 25 FOR EACH HOUSE AND 100 FOR EACH HOTEL",
              "GO TO JAIL", "GET OUT OF JAIL FREE"]
    random.shuffle(chance)


def setup_community_chest():
    global community_chest
    community_chest = ["PAY SCHOOL TAX OF 150", "COLLECT 50 FROM EACH PLAYER", "YOU INHERIT 100",
                       "PAY HOSPITAL 100", "INCOME TAX REFUND COLLECT 20", "GO TO JAIL", "GET OUT OF JAIL FREE",
                       "WIN 10 IN A BEAUTY CONTEST", "STREET REPAIRS 40 PER HOUSE AND 115 PER HOTEL",
                       "BANK ERROR COLLECT 200",
                       "ADVANCE TO GO", "XMAS FUND MATURES COLLECT 100", "DOCTORS FEE PAY 50",
                       "SALE FROM STOCK GAIN 45",
                       "RECIEVE 45 FROM SERVICES", "LIFE INSURANCE MATURES COLLECT 100"]
    random.shuffle(community_chest)


def create_pieces():
    global pieces
    counter = 0
    while counter < number_of_players:
        pieces.append(piece(names[counter], 0, starting_money, "", -1, 0, "#%02x%02x%02x" % (
        random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))))
        counter = counter + 1


def roll_dice():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice = dice1 + dice2
    return dice1, dice2, dice


def in_jail(dice1, dice2, input):
    # Check if the player is in jail
    if pieces[piece_turn].jail_time > -1:
        print(pieces[piece_turn].name, "is in jail")

        # Check if the player can get out of jail
        if (input == 1 and pieces[piece_turn].money > 50) or pieces[piece_turn].jail_card > 0 or dice1 == dice2:
            if dice1 == dice2:
                # If the dice rolls are the same, the player gets out of jail
                pieces[piece_turn].jail_time = -1
                print(pieces[piece_turn].name, "rolled doubles and got out of jail")
            elif pieces[piece_turn].jail_card > 0:
                # If the player has a "jail card," use it and add it back to the respective deck
                pieces[piece_turn].jail_card -= 1
                if "GET OUT OF JAIL FREE" not in chance:
                    chance.append("GET OUT OF JAIL FREE")
                else:
                    community_chest.append("GET OUT OF JAIL FREE")
                print(pieces[piece_turn].name, "used a 'Get Out of Jail Free' card and got out of jail")
            elif input == 1 and pieces[piece_turn].money >= 50:
                # If the player chooses to pay and has enough money, pay $50 to get out of jail
                pieces[piece_turn].money -= 50
                print(pieces[piece_turn].name, "paid $50 and got out of jail")

            pieces[piece_turn].jail_time = -1
            print(pieces[piece_turn].name, "is out of jail")
        else:
            if pieces[piece_turn].jail_time == 3:
                # If the player has been in jail for three turns, pay $50 to get out of jail
                pieces[piece_turn].money -= 50
                pieces[piece_turn].jail_time = -1
                print(pieces[piece_turn].name, "paid $50 and got out of jail")
                print(pieces[piece_turn].name, "is out of jail")
            else:
                pieces[piece_turn].jail_time += 1
            print(pieces[piece_turn].name, "is in jail. Current time:", pieces[piece_turn].jail_time)
        return 1
    else:
        return 0


def find_place(place):
    counter = 0
    while not squares[counter].name == place:
        counter = counter + 1
    return counter


def move_piece():
    if pieces[piece_turn].square + dice > len(squares) - 1:
        pieces[piece_turn].square = pieces[piece_turn].square + dice - len(squares)
        pieces[piece_turn].money = pieces[piece_turn].money + 200
    else:
        pieces[piece_turn].square = (pieces[piece_turn].square) + dice
    print(" ", pieces[piece_turn].name, "rolled ", dice, "moved to ", squares[pieces[piece_turn].square].name,
          pieces[piece_turn].square)
    if squares[pieces[piece_turn].square].name == "Go To Jail":
        pieces[piece_turn].square = find_place("Jail")
        pieces[piece_turn].jail_time = 0


def isChance():
    if squares[pieces[piece_turn].square].name == "Chance":
        # ["ADVANCE TO GO", "ADVANCE TO BOARDWALK", "ADVANCE TO ILLINOIS AVE", "ADVANCE TO ST. CHARLES PLACE", "TAKE A RIDE ON READING",
        # "ADVANCE TO NEAREST RAILROAD", "ADVANCE TO NEAREST RAILROAD", "ADVANCE TO NEAREST UTILITY",
        # "GO BACK 3 SPACES", "BANK PAYS YOU DIVIDEND OF 50", "YOUR BUILDING AND LOAN MATURES COLLECT 150",
        # "PAY POOR TAX OF 15", "ELECTED CHAIRMAN OF BOARD PAY EACH PLAYER 50", "PAY 25 FOR EACH HOUSE AND 100 FOR EACH HOTEL",
        # "GO TO JAIL", "GET OUT OF JAIL FREE"]

        card = chance[0]
        print("card: ", card)
        if card == "ADVANCE TO GO":
            pieces[piece_turn].square = 0
            pieces[piece_turn].money = pieces[piece_turn].money + 200
        elif card == "ADVANCE TO BOARDWALK":
            pieces[piece_turn].square = find_place("Boardwalk")
        elif card == "ADVANCE TO ILLINOIS AVE":
            pieces[piece_turn].square = find_place("Illinois Avenue")
        elif card == "ADVANCE TO ST. CHARLES PLACE":
            pieces[piece_turn].square = find_place("St. Charles Place")
        elif card == "TAKE A RIDE ON READING":
            pieces[piece_turn].square = find_place("Reading Railroad")
        elif card == "ADVANCE TO NEAREST RAILROAD":
            counter = pieces[piece_turn].square
            while not squares[counter].color == 9:
                counter = counter + 1
                if counter > len(squares) - 1:
                    counter = 0
                    pieces[piece_turn].money = pieces[piece_turn].money + 200
            pieces[piece_turn].square = counter
            multiplier = 2
        elif card == "ADVANCE TO NEAREST UTILITY":
            counter = pieces[piece_turn].square
            while not squares[counter].color == 10:
                counter = counter + 1
                if counter > len(squares) - 1:
                    counter = 0
                    pieces[piece_turn].money = pieces[piece_turn].money + 200
            pieces[piece_turn].square = counter
            multiplier = 10
        elif card == "GO BACK 3 SPACES":
            pieces[piece_turn].square = pieces[piece_turn].square - 3
        elif card == "BANK PAYS YOU DIVIDEND OF 50":
            pieces[piece_turn].money = pieces[piece_turn].money + 50
        elif card == "YOUR BUILDING AND LOAN MATURES COLLECT 150":
            pieces[piece_turn].money = pieces[piece_turn].money + 150
        elif card == "PAY POOR TAX OF 15":
            pieces[piece_turn].money = pieces[piece_turn].money - 15
        elif card == "ELECTED CHAIRMAN OF BOARD PAY EACH PLAYER 50":
            counter = 0
            while counter < len(pieces):
                if not counter == piece_turn:
                    pieces[counter].money = pieces[counter].money + 50
                    pieces[piece_turn].money = pieces[piece_turn].money - 50
                counter = counter + 1
        elif card == "GO TO JAIL":
            pieces[piece_turn].square = find_place("Jail")
            pieces[piece_turn].jail_time = 0
        elif card == "PAY 25 FOR EACH HOUSE AND 100 FOR EACH HOTEL":
            total_house = 0
            total_hotel = 0
            counter = 0
            while counter < len(pieces[piece_turn].properties):
                if pieces[piece_turn].properties[counter].houses > 0:
                    if pieces[piece_turn].properties[counter].houses < 5:
                        total_house = total_house + pieces[piece_turn].properties[counter].houses
                    else:
                        total_hotel = total_hotel + 1
                counter = counter + 1
            pieces[piece_turn].money = pieces[piece_turn].money - ((total_house * 25) + total_hotel * 100)


        elif card == "GET OUT OF JAIL FREE":
            pieces[piece_turn].jail_card = pieces[piece_turn].jail_card + 1

        chance.pop(0)
        if not card == "GET OUT OF JAIL FREE":
            chance.append(card)


def isCommunityChest():
    if squares[pieces[piece_turn].square].name == "Community Chest":
        # ["PAY SCHOOL TAX OF 150", "COLLECT 50 FROM EACH PLAYER", "YOU INHERIT 100",
        # "PAY HOSPITAL 100", "INCOME TAX REFUND COLLECT 20", "GO TO JAIL", "GET OUT OF JAIL FREE",
        # "WIN 10 IN A BEAUTY CONTEST", "STREET REPAIRS 40 PER HOUSE AND 115 PER HOTEL",
        # "BANK ERROR COLLECT 200",
        # "ADVANCE TO GO", "XMAS FUND MATURES COLLECT 100", "DOCTORS FEE PAY 50", "SALE FROM STOCK GAIN 45",
        # "RECIEVE 45 FROM SERVICES", "LIFE INSURANCE MATURES COLLECT 100"]

        card = community_chest[0]
        print("card: ", card)
        if card == "PAY SCHOOL TAX OF 150":
            pieces[piece_turn].money = pieces[piece_turn].money - 150
        elif card == "COLLECT 50 FROM EACH PLAYER":
            counter = 0
            while counter < len(pieces):
                if not counter == piece_turn:
                    pieces[counter].money = pieces[counter].money - 50
                pieces[piece_turn].money = pieces[piece_turn].money + 50
                counter = counter + 1
        elif card == "YOU INHERIT 100":
            pieces[piece_turn].money = pieces[piece_turn].money + 100
        elif card == "PAY HOSPITAL 100":
            pieces[piece_turn].money = pieces[piece_turn].money - 100
        elif card == "INCOME TAX REFUND COLLECT 20":
            pieces[piece_turn].money = pieces[piece_turn].money + 20
        elif card == "GO TO JAIL":
            pieces[piece_turn].square = find_place("Jail")
            pieces[piece_turn].jail_time = 0
        elif card == "GET OUT OF JAIL FREE":
            pieces[piece_turn].jail_card = pieces[piece_turn].jail_card + 1
        elif card == "WIN 10 IN A BEAUTY CONTEST":
            pieces[piece_turn].money = pieces[piece_turn].money + 10
        elif card == "STREET REPAIRS 40 PER HOUSE AND 115 PER HOTEL":
            total_house = 0
            total_hotel = 0
            counter = 0
            while counter < len(pieces[piece_turn].properties):
                if pieces[piece_turn].properties[counter].houses > 0:
                    if pieces[piece_turn].properties[counter].houses < 5:
                        total_house = total_house + pieces[piece_turn].properties[counter].houses
                    else:
                        total_hotel = total_hotel + 1
                counter = counter + 1
            pieces[piece_turn].money = pieces[piece_turn].money - ((total_house * 40) + total_hotel * 115)
        elif card == "BANK ERROR COLLECT 200":
            pieces[piece_turn].money = pieces[piece_turn].money + 200
        elif card == "ADVANCE TO GO":
            pieces[piece_turn].square = 0
            pieces[piece_turn].money = pieces[piece_turn].money + 200
        elif card == "XMAS FUND MATURES COLLECT 100":
            pieces[piece_turn].money = pieces[piece_turn].money + 100
        elif card == "DOCTORS FEE PAY 50":
            pieces[piece_turn].money = pieces[piece_turn].money - 50
        elif card == "SALE FROM STOCK GAIN 45":
            pieces[piece_turn].money = pieces[piece_turn].money + 45
        elif card == "RECIEVE 45 FROM SERVICES":
            pieces[piece_turn].money = pieces[piece_turn].money + 45
        elif card == "LIFE INSURANCE MATURES COLLECT 100":
            pieces[piece_turn].money = pieces[piece_turn].money + 100
        community_chest.pop(0)
        if not card == "GET OUT OF JAIL FREE":
            community_chest.append(card)


def buy_property(input):
    if squares[pieces[piece_turn].square].owner == -1 and pieces[piece_turn].money > squares[
        pieces[piece_turn].square].price and input == 1 and not squares[pieces[piece_turn].square] in mortgaged:
        pieces[piece_turn].money = pieces[piece_turn].money - squares[pieces[piece_turn].square].price
        squares[pieces[piece_turn].square].owner = piece_turn
        pieces[piece_turn].properties.append(squares[pieces[piece_turn].square])
        print("  bought", squares[pieces[piece_turn].square].name, squares[pieces[piece_turn].square].price)


def pay_fees():
    if squares[pieces[piece_turn].square].owner == -2 and squares[pieces[piece_turn].square].housing != 1:
        pieces[piece_turn].money = pieces[piece_turn].money - squares[pieces[piece_turn].square].price
        print(pieces[piece_turn].name, "Fees paid ", squares[pieces[piece_turn].square].price, " at ",
              squares[pieces[piece_turn].square].name)


def collect_rent():
    if squares[pieces[piece_turn].square].owner > -1:
        if squares[pieces[piece_turn].square].housing == 1:
            if squares[pieces[piece_turn].square].owner != piece_turn:
                if squares[pieces[piece_turn].square] not in mortgaged:
                    rent = 0
                    if squares[pieces[piece_turn].square].houses == 0:
                        rent = squares[pieces[piece_turn].square].rent
                    elif squares[pieces[piece_turn].square].houses == 1:
                        rent = squares[pieces[piece_turn].square].house1
                    elif squares[pieces[piece_turn].square].houses == 2:
                        rent = squares[pieces[piece_turn].square].house2
                    elif squares[pieces[piece_turn].square].houses == 3:
                        rent = squares[pieces[piece_turn].square].house3
                    elif squares[pieces[piece_turn].square].houses == 4:
                        rent = squares[pieces[piece_turn].square].house4
                    elif squares[pieces[piece_turn].square].houses == 5:
                        rent = squares[pieces[piece_turn].square].hotel + squares[pieces[piece_turn].square].house4

                    pieces[piece_turn].money -= rent
                    pieces[squares[pieces[piece_turn].square].owner].money += rent

                    print(pieces[piece_turn].name, "paid", pieces[squares[pieces[piece_turn].square].owner].name,
                          "$" + str(rent), "in rent")
                else:
                    print(pieces[piece_turn].name, " did not pay ",
                          pieces[squares[pieces[piece_turn].square].owner].name, " because mortgaged")


def buy_house(input):
    if squares[pieces[piece_turn].square].housing != 1:
        return
    # Check if the property has less than 4 houses and the current player is the owner
    if squares[pieces[piece_turn].square].houses < 5 and squares[pieces[piece_turn].square].owner == piece_turn:
        counter = 0
        number_of_color = 0
        looking_for = squares[pieces[piece_turn].square].color

        # Count the number of properties owned by the player that have the same color as the current property
        while counter < len(pieces[piece_turn].properties):
            if pieces[piece_turn].properties[counter].color == looking_for:
                number_of_color += 1
            counter += 1

        # Check if the player has enough properties of the same color, enough money, and the input value is 1
        minimum_color = squares[pieces[piece_turn].square].maxcolor
        if number_of_color >= minimum_color and pieces[piece_turn].money > squares[
            pieces[piece_turn].square].houseprice and input == 1:
            pieces[piece_turn].money -= squares[pieces[piece_turn].square].houseprice

            squares[pieces[piece_turn].square].houses += 1
            print(pieces[piece_turn].name, "bought a house at", squares[pieces[piece_turn].square].name, " for ",
                  squares[pieces[piece_turn].square].houseprice)


def railroad_functions(multiplier):
    if squares[pieces[piece_turn].square].color == 9 and squares[pieces[piece_turn].square].owner >= 0 \
            and squares[pieces[piece_turn].square].owner != piece_turn:
        counter = 0
        rail_count = 0
        while counter < len(pieces[squares[pieces[piece_turn].square].owner].properties):
            if pieces[squares[pieces[piece_turn].square].owner].properties[counter].color == 9:
                rail_count = rail_count + 1
                print("rail count", rail_count)
            counter = counter + 1
        if rail_count == 1:
            pieces[piece_turn].money = pieces[piece_turn].money - (25 * multiplier)
            pieces[squares[pieces[piece_turn].square].owner].money += (25 * multiplier)
            print(pieces[piece_turn].name, " paid ", 25 * multiplier, " to ", squares[pieces[piece_turn].square].owner,
                  "railroad")
        if rail_count == 2:
            pieces[piece_turn].money = pieces[piece_turn].money - (50 * multiplier)
            pieces[squares[pieces[piece_turn].square].owner].money += (50 * multiplier)
            print(pieces[piece_turn].name, " paid ", 25 * multiplier, " to ", squares[pieces[piece_turn].square].owner,
                  "railroad")
        if rail_count == 3:
            pieces[piece_turn].money = pieces[piece_turn].money - (100 * multiplier)
            pieces[squares[pieces[piece_turn].square].owner].money += (100 * multiplier)
            print(pieces[piece_turn].name, " paid ", 25 * multiplier, " to ", squares[pieces[piece_turn].square].owner,
                  "railroad")
        if rail_count == 4:
            pieces[piece_turn].money = pieces[piece_turn].money - (200 * multiplier)
            pieces[squares[pieces[piece_turn].square].owner].money += (200 * multiplier)
            print(pieces[piece_turn].name, " paid ", 25 * multiplier, " to ", squares[pieces[piece_turn].square].owner,
                  "railroad")


def utility_functions():
    if squares[pieces[piece_turn].square].color == 10 and squares[pieces[piece_turn].square].owner >= 0 and squares[
        pieces[piece_turn].square].owner != piece_turn:

        counter = 0
        utility_count = 0
        while counter < len(pieces[squares[pieces[piece_turn].square].owner].properties):
            if pieces[squares[pieces[piece_turn].square].owner].properties[counter].color == 10:
                utility_count = utility_count + 1
            counter = counter + 1
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        dice = dice1 + dice2
        if utility_count == 1 and multiplier == 1:
            pieces[piece_turn].money = pieces[piece_turn].money - (dice * 4)
            pieces[squares[pieces[piece_turn].square].owner].money = pieces[squares[
                pieces[piece_turn].square].owner].money + (dice * 4)
            print(pieces[piece_turn].name, " paid ", dice * 4, " to ",
                  pieces[squares[pieces[piece_turn].square].owner].name)
        else:
            pieces[piece_turn].money = pieces[piece_turn].money - (dice * 10)
            pieces[squares[pieces[piece_turn].square].owner].money = pieces[squares[
                pieces[piece_turn].square].owner].money + (dice * 10)


def is_broke():
    if pieces[piece_turn].money < 0:
        print(pieces[piece_turn].name, "ran out of money on round", round + 1, pieces[piece_turn].money)
        return 1
    else:
        return 0


def get_board_state():
    board_state = np.full((45, number_of_players), -1)
    current_player = 0
    while current_player < number_of_players:
        counter = 0
        # first 39 are properties, 40 is money, 41 is location, 42 is if in jail
        while counter < len(pieces[current_player].properties):
            col = squares.index(pieces[current_player].properties[counter])
            row = current_player
            board_state[col][row] = int(pieces[current_player].properties[counter].houses)

            counter = counter + 1

        board_state[40][current_player] = (pieces[current_player].money)

        board_state[41][current_player] = int(pieces[current_player].square)

        board_state[42][current_player] = pieces[current_player].jail_time

        board_state[43][current_player] = dice1
        board_state[44][current_player] = dice2
        current_player += 1

    squares_mortgaged = []
    for properties in mortgaged:
        squares_mortgaged.append(int(squares.index(properties)))

    flattened_array = np.concatenate((np.array(list(chain.from_iterable(board_state))), squares_mortgaged))
    while len(flattened_array) < (180 + len(squares)):
        flattened_array = np.append(flattened_array, 0)
    return flattened_array.astype(np.int64)


def get_player_networth(player):
    networth = pieces[player].money
    for i in range(len(pieces[player].properties)):
        networth += pieces[player].properties[i].price + (
                    pieces[player].properties[i].houseprice * pieces[player].properties[i].houses)
    return networth


def mortgage(yes):
    if yes == 0:
        return
    lowest_price = 1000000000
    cheapest_property = -1
    for i in range(len(pieces[piece_turn].properties)):
        property_price = pieces[piece_turn].properties[i].houses * pieces[piece_turn].properties[i].houseprice + \
                         pieces[piece_turn].properties[i].price
        if property_price < lowest_price and (pieces[piece_turn].properties[i] not in mortgaged):
            lowest_price = property_price
            cheapest_property = i

    if not cheapest_property == -1:
        mortgaged.append(pieces[piece_turn].properties[cheapest_property])
        cost = int(pieces[piece_turn].properties[cheapest_property].houses * pieces[piece_turn].properties[
            cheapest_property].houseprice * 0.5) + pieces[piece_turn].properties[cheapest_property].mortgage
        pieces[piece_turn].money += int(
            pieces[piece_turn].properties[cheapest_property].houses * pieces[piece_turn].properties[
                cheapest_property].houseprice * 0.5)
        pieces[piece_turn].properties[cheapest_property].houses = 0
        pieces[piece_turn].money += pieces[piece_turn].properties[cheapest_property].mortgage
        print(pieces[piece_turn].name, " mortgaged ", pieces[piece_turn].properties[cheapest_property].name, " for ",
              cost)


def buy_back(yes):
    if yes == 0:
        return
    for i in range(len(mortgaged)):
        if mortgaged[i].owner == piece_turn and pieces[piece_turn].money >= (mortgaged[i].mortgage * 1.1):
            pieces[mortgaged[i].owner].money -= int(mortgaged[i].mortgage * 2)
            print(pieces[piece_turn].name, " bought back ", mortgaged[i].name, " for ", int(mortgaged[i].mortgage * 2))
            mortgaged.pop(i)

        return


def draw_board():
    return
    canvas.delete("all")

    scale = 1.2
    # Draw the squares on the canvas
    i = 0
    while i < len(squares):
        x1 = squares[i].x1
        y1 = squares[i].y1
        x2 = squares[i].x2
        y2 = squares[i].y2

        label = squares[i].name.replace(" ", "\n")
        label += "\n \n Houses: " + str(squares[i].houses)
        if squares[i] in mortgaged:
            label += "\n Is mortgaged "

        x1_scaled = x1 / scale
        y1_scaled = y1 / scale
        x2_scaled = x2 / scale
        y2_scaled = y2 / scale

        if squares[i].owner >= 0:
            color = pieces[squares[i].owner].color
        else:
            color = "white"

        # 1 is purple, 2 is turquoise, 3 is pink, 4 is orange, 5 is red, 6 is yellow, 7 is green, 8 is blue, 9 is railroad, 10 is utility
        colors = ["purple", "turquoise", "pink", "orange", "red", "yellow", "green", "blue"]

        if squares[i].color - 1 < len(colors) and squares[i].color > 0:
            outline = colors[squares[i].color - 1]
        else:
            outline = "black"

        canvas.create_rectangle(x1_scaled, y1_scaled, x2_scaled, y2_scaled, fill=color, outline=outline, width=5)

        canvas.create_text((x1_scaled + x2_scaled) / 2, (y1_scaled + y2_scaled) / 2, text=label,
                           font=("Arial", 6, "bold"), justify="center")

        i += 1

    # Drawing pieces
    circle_radius = 10
    visited = []

    for i in range(len(pieces)):
        if pieces[i].square in visited:

            x = (((squares[pieces[i].square].x1 + squares[pieces[i].square].x2) / 2) / scale) + (i % 6 * 6.5)
            y = (((squares[pieces[i].square].y1 + squares[pieces[i].square].y2) / 2) / scale) + (i % 8 * 6.5)
        else:
            x = (((squares[pieces[i].square].x1 + squares[pieces[i].square].x2) / 2) / scale)
            y = (((squares[pieces[i].square].y1 + squares[pieces[i].square].y2) / 2) / scale)

        x -= 20
        y -= 20
        canvas.create_oval(x - circle_radius, y - circle_radius,
                           x + circle_radius, y + circle_radius,
                           fill=pieces[i].color)
        canvas.create_text(x, y, text=pieces[i].name, font=("Arial", circle_radius, "bold"), fill="black")

        visited.append(pieces[i].square)

    i = 0
    x = canvas_width / 2
    y = (canvas_height / 2) - (len(pieces) * 10)
    while i < len(pieces):
        text = pieces[i].name + ": " + str(pieces[i].money) + "$  Networth: " + str(get_player_networth(i))
        canvas.create_text(x, y, text=text, font=("Arial", 12), fill="black", justify="center")
        y += 20
        i += 1
    y += 40
    canvas.create_text(x, y, text=("Round: " + str(round)), font=("Arial", 12), fill="black", justify="center")
    y += 20
    canvas.create_text(x, y, text=("Game: " + str(number_of_games + 1)), font=("Arial", 12), fill="black", justify="center")

    canvas.create_text(200, 200, text=chance[0].replace(" ", "\n"), font=("Arial", 12))
    canvas.create_text(750, 750, text=community_chest[0].replace(" ", "\n"), font=("Arial", 12))

    window.update()


def nn_inputs(board_state, strategy_length):
    possible_inputs = []
    combinations = np.array(list(itertools.product([0, 1], repeat=strategy_length)))
    for strategy in combinations:
        possible_inputs.append(np.concatenate((board_state, strategy)))
    return possible_inputs


def use_nn():
    possible_inputs = nn_inputs(get_board_state(), 5)
    highest_money = -10000000000
    best_strategy = []
    last_nn_input = []
    for test_input in possible_inputs:
        output = use_nn_forward(test_input, -1)
        if output > highest_money:
            highest_money = output
            best_strategy = test_input[-5:]
            last_nn_input = test_input
    return best_strategy, last_nn_input



generate_random_names(number_of_players)

max_number_of_games = 1000
number_of_games = 0
round_average_array = []
winner = -1
setup_properties()

pieces = []

#canvas_width = 925
#canvas_height = 925
#canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="white")
#canvas.pack()

while number_of_games < max_number_of_games:

    print("")
    print("------------------------")
    print("Game start")
    print("")
    print("")
    time.sleep(0)
    round = 1
    piece_turn = 0
    mortgaged = []
    multiplier = 0
    squares = []
    chance = []
    community_chest = []
    pieces = []
    setup_properties()
    color_count()
    setup_chance()
    setup_community_chest()
    create_pieces()
    #draw_board()
    winner = -1
    # time.sleep(3)
    last_nn_input = []
    decisions = []
    while True:
        multiplier = 1

        # time.sleep(1)
        dice1, dice2, dice = roll_dice()
        if piece_turn == 0:
            if len(last_nn_input) > 0:

                loss = abs(pieces[piece_turn].money - use_nn_forward(last_nn_input, -1))

                with open("output", "a") as file:
                    file.write("Predicted: " + str(use_nn_forward(last_nn_input, -1)))
                    file.write("  Actual: " + str(pieces[piece_turn].money))
                    file.write("  Loss: " + str(loss) + "\n")
                    if round % 20 == 0:
                        file.flush()

                use_nn_forward(last_nn_input, loss)

            decisions, last_nn_input = use_nn()

        else:
            decisions = [random.choice([0, 1]), random.choice([0, 1]), random.choice([0, 1]),
                         random.choice([0, 1]), random.choice([0, 1])]
        print(decisions)

        if in_jail(dice1, dice2, decisions[0]) == 0:
            move_piece()
            isChance()
            isCommunityChest()
            pay_fees()
            collect_rent()
            railroad_functions(multiplier)
            utility_functions()
            buy_house(decisions[3])
            buy_property(decisions[4])
            buy_back(decisions[2])
            mortgage(decisions[1])
            broke = is_broke()
            if broke == 1:
                print(pieces[piece_turn].name, "ran out of money on round", round + 1, pieces[piece_turn].money)
                winner = -1
                break

        piece_turn = piece_turn + 1
        if piece_turn == len(pieces):
            piece_turn = 0
            round = round + 1
            end = "round over " + str(round)
            for person in pieces:
                end += " | " + person.name + " " + str(person.money) + " | "
            print(end, "--------------------")
        if round > 99:
            highest = 0
            winner = -1
            for player in pieces:
                if player.money > highest:
                    highest = player.money
                    winner = player.name
            break

        #draw_board()
        #window.update()

    round_average_array.append(round)
    number_of_games = number_of_games + 1
    #draw_board()

if winner != -1:
    print("The player with the most money after 100 rounds is: ", winner)
time.sleep(10)

#window.mainloop()

sys.exit()
