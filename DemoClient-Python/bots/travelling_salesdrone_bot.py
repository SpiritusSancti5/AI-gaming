from random import randint, choice, shuffle
from math import hypot


def calculateMove(gamestate):
    print(gamestate)
    a = [i for i in range(len(gamestate["CityCoords"]))]  # Produces a list of all the city indexes
    shuffle(a)  # Randomly orders the list of cities
    print(a)
    move = {"Path": a}  # Sets move to be the random order of cities
    return move


# Given two city coordinates of the form [x, y] returns the distance between them
def get_distance(origin, destination):
    distance = hypot(abs(origin[0] - destination[0]), abs(origin[1] - destination[1]))
    return distance


# Given the list of city coordinates, the current city index, and a list of available cities indexes to choose from
# calculates the closest city (from the list of available cities) to the current city and returns it
def find_closest_city(coords, cur_city, available_cities):
    closest_city = available_cities[0]  # initialise closest city so far to the first city in the list
    closest_distance = get_distance(coords[cur_city], coords[
        closest_city])  # Initialise the distance to the closest city as the distance to the first city in the list

    for next_city in available_cities[1:]:  # For all remaining cities
        next_distance = get_distance(coords[cur_city],
                                     coords[next_city])  # Calculate the distance to it from our current city
        if next_distance < closest_distance:  # If this distance is our new shortest
            closest_distance = next_distance  # Update closest_distance
            closest_city = next_city  # Update closest_city

    return closest_city  # Return the closest city we found