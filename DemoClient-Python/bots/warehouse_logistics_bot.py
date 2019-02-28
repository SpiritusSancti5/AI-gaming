from random import randint
from math import ceil


def calculateMove(gameState):
    # Initialise warehouse variables
    items = gameState["Items"]
    fixtures = gameState["Fixtures"]
    inventory = gameState["Inventory"]
    pickers = gameState["Pickers"]
    dispatch_desks = gameState["DispatchDesks"]
    num_pickers = len(pickers)
    num_dispatch_desks = len(dispatch_desks)

    # Initialise move as empty lists
    picker_instructions = [[] for _ in range(num_pickers)]

    for item in items:  # For every item in the list to pick
        fixture_id = findFixtures(item["Id"], inventory, item["Quantity"])[0]  # Pick the first fixture that contains the item
        picker = randint(0, num_pickers - 1)  # Choose a random picker to perform the task
        while not canPick(item["Id"], inventory, pickers[picker]):  # While we have chosen a picker that can't carry the item
            picker = randint(0, num_pickers - 1)  # Re-pick the picker
        dispatch_desk_id = dispatch_desks[randint(0, num_dispatch_desks - 1)]['Id']  # Pick a random dispatch desk
        picker_instructions[picker].append({"Location": fixture_id, "Item": item["Id"], "Quantity": item["Quantity"]})  # Pick up the item
        picker_instructions[picker].append({"Location": dispatch_desk_id, "Item": item["Id"], "Quantity": item["Quantity"]})  # Dispatch the item

    return picker_instructions  # Return our move


# Given an item id and the inventory, returns a list of the fixtures containing that item
def findFixtures(item_id, inventory, quantity):
    fixture_ids = [stock["FixtureId"] for stock in inventory if stock["Id"] == item_id and stock["Quantity"] >= quantity]
    return fixture_ids


# Given an item id and the inventory, returns the size of the item
def getSize(item_id, inventory):
    size = next(stock["Size"] for stock in inventory if stock["Id"] == item_id)
    return size


# Given an item id and the inventory, returns the type of the item
def getType(item_id, inventory):
    item_type = next(stock["Type"] for stock in inventory if stock["Id"] == item_id)
    return item_type


# Given an item id, the inventory, and a picker, returns whether the picker can pick an item of that size and type (If they are carrying nothing else)
def canPick(item_id, inventory, picker):
    pick_type = getType(item_id, inventory) in picker["ItemTypes"]  # Can the picker pick this item type
    pick_size = getSize(item_id, inventory) < picker["MaximumLoad"] or picker["MaximumLoad"] == 0  # Can the picker pick this item size
    return pick_type and pick_size


# Given a fixture id and a quantity of items, returns how long it will take for a picker to pick all of the items from the fixture
def pickTime(fixture, quantity):
    total_time = 0
    while quantity > 1:
        total_time += max(0.1, 1 / quantity)  # Up to a certain point picking from the same fixture repeatedly becomes quicker
        quantity -= 1
    total_time += 1

    return ceil(fixture["PickDifficulty"] * total_time)  # The total time to pick or dispatch a quantity of items, or travel around the warehouse, is always rounded up
