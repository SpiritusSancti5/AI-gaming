import requests
import json
from random import sample, choice
from time import sleep

# See our help page to learn how to get a Microsoft API Key at
#  http://help.aigaming.com/wiw-mssignup
headers_vision = {'Ocp-Apim-Subscription-Key': 'YOUR-MICROSOFT-COMPUTER-VISION-API-KEY-HERE'}
vision_base_url = "https://westeurope.api.cognitive.microsoft.com/vision/v2.0/"

analysed_tiles = []
previous_move = []


# =============================================================================
# calculate_move() overview
#  1. Analyse the upturned tiles and remember them
#  2. Determine if you have any matching tiles
#  3. If we have matching tiles:
#        use them as a move
#  4. If no matching tiles:
#        Guess two tiles for this move
#
#  Important point: calculate_move can only remember data between moves
#    if we store it in analysed_tiles
#  Use analysed_tiles to remember the tiles we have seen
#  We recognise animals for you, you must do landmarks and words
#
#  Get more help at http://help.aigaming.com/match-game
#
def calculateMove(gamestate):
    global analysed_tiles
    global previous_move
    # Record the number of tiles in the game
    # so we know how many tiles we need to loop through
    num_tiles = len(gamestate["Board"])

    # If we have not yet added analysed_tiles
    # (i.e. It is the first turn)
    if analysed_tiles == []:
        # Create a list of tile information
        for index in range(num_tiles):
            # Mark tile as not analysed
            analysed_tiles.append({})
            analysed_tiles[index]["State"] = "UNANALYSED"
            analysed_tiles[index]["Subject"] = None

    # If there are upturned tiles from our last turn.
    # The very first move you make does not have any upturned tiles, and
    # if your last move matched tiles, you will not have any upturned tiles
    if gamestate["UpturnedTiles"] != []:
        # Analyse the tiles images using the Microsoft API and
        # store results in analysed_tiles
        analyse_tiles(gamestate["UpturnedTiles"], gamestate)
    # If it is our first turn, or our previous move was a match
    else:
        # If it is not our first move of the game
        # Then our previous move successfully matched two tiles
        if previous_move != []:
            # Update our AnalysedTiles to mark the previous tiles as matched
            analysed_tiles[previous_move[0]]["State"] = "MATCHED"
            analysed_tiles[previous_move[1]]["State"] = "MATCHED"

    # Print out the updated analysed_tiles
    # Python print statements appear in column 3 of this Editor window
    # and can be used for debugging
    print("Analysed Tiles: {}".format(json.dumps(analysed_tiles, indent=4)))

    # Check the stored tile information in analysed_tiles
    # to see if there are any matching tiles
    match = search_for_matching_tiles()
    # If we have found a matching pair
    if match is not None:
        # Print out the move for debugging ----------------->
        print("Matching Move: {}".format(match))
        # Set our move to be these matching tiles
        move = match
    # If we don't have any matching tiles
    else:
        # Create a list of all the unanalysed tiles
        unanalysed_tiles = get_unanalysed_tiles()
        # If there are tiles we haven't analysed yet
        if unanalysed_tiles != []:
            # Choose the unanalysed tiles that you want to turn over
            # in your next move. We turn over a random pair of
            # unanalysed tiles, but, could you make a more intelligent
            # choice?
            move = sample(unanalysed_tiles, 2)
            # Print out the move here ----------------->
            print("New Tiles Move: {}".format(move))
        # If the unanalysed_tiles list is empty (all tiles have been analysed)
        else:
            # If all else fails, we will need to manually match each tile

            # Create a list of all the unmatched tiles
            unmatched_tiles = get_unmatched_tiles()

            # Turn over two random tiles that haven't been matched
            # TODO: It would be more efficient to remember which tiles you
            #       have tried to match.
            move = sample(unmatched_tiles, 2)
            # Print the move out here ----------------->
            print("Random Combination Move: {}".format(move))

    # Store our move to look back at next turn
    previous_move = move
    # Print out the current gamestate here ----------------->
    print("Gamestate: {}".format(json.dumps(gamestate)))
    # Return the move we wish to make
    return {"Tiles": move}


# Get the unmatched tiles
#
# Outputs:
#   list of integers - A list of unmatched tile numbers
#
# Returns the list of tiles that haven't been matched
def get_unmatched_tiles():
    # Create a list of all the unmatched tiles
    unmatched_tiles = []
    # For every tile in the game
    for index, tile in enumerate(analysed_tiles):
        # If that tile hasn't been matched yet
        if tile["State"] != "MATCHED":
            # Add that tile to the list of unmatched tiles
            unmatched_tiles.append(index)
    # Return the list
    return unmatched_tiles


# Identify all of the tiles that we have not yet analysed with the
# Microsoft API.
#
# Output:
#  list of integers - only those tiles that have not yet been analysed
#                     by the Microsoft API
#
# Returns the list of tiles that haven't been analysed
# (according to analysed_tiles)
def get_unanalysed_tiles():
    # Filter out analysed tiles
    unanalysed_tiles = []
    # For every tile that hasn't been matched
    for index, tile in enumerate(analysed_tiles):
        # If the tile hasn't been analysed
        if tile["State"] == "UNANALYSED":
            # Add that tile to the list of unanalysed tiles
            unanalysed_tiles.append(index)
    # Return the list
    return unanalysed_tiles


# Analyses the inputted list of tiles
#
# Inputs:
#   tiles:       list of JSON objects - A list of tile objects that contain a
#                                       url and an index
#   gamestate:   JSON object          - The current state of the game
#
# Given a list of tiles we want to analyse and the animal list, calls the
# analyse_tile function for each of the tiles in the list
def analyse_tiles(tiles, gamestate):
    # For every tile in the list 'tiles'
    for tile in tiles:
        # Call the analyse_tile function with that tile
        # along with the gamestate
        analyse_tile(tile, gamestate)


# Analyses the inputted tile
#
# Inputs:
#   tile:      JSON object - A tile object that contains a url and an index
#   gamestate: JSON object - The current state of the game
#
# Given a tile, analyse it to determine its subject and record the information
# in analysed_tiles using the Microsoft APIs
def analyse_tile(tile, gamestate):
    # If we have already analysed the tile
    if analysed_tiles[tile["Index"]]["State"] != "UNANALYSED":
        # We don't need to analyse the tile again, so stop
        return

    # Call analysis
    analyse_url = vision_base_url + "analyze"
    params_analyse = {'visualFeatures': 'categories,tags,description,faces,imageType,color,adult',
                      'details': 'celebrities,landmarks'}
    data = {"url": tile["Tile"]}
    msapi_response = microsoft_api_call(analyse_url, params_analyse, headers_vision, data)

    # Check if the subject of the tile is an animal
    subject = check_for_animal(msapi_response, gamestate["AnimalList"])
    # If we haven't determined the subject of the image yet
    if subject is None:
        # Check if the subject of the tile is a landmark
        subject = check_for_landmark(msapi_response)
    # If we still haven't determined the subject of the image yet
    if subject is None:
        # TODO: Use the Microsoft OCR API to determine if the tile contains a
        # word. You can get more information about the Microsoft Cognitive API
        # OCR function at:
        # https://westus.dev.cognitive.microsoft.com/docs/services/56f91f2d778daf23d8ec6739/operations/56f91f2e778daf14a499e1fc
        # Use our previous example to check_for_animal as a guide
        pass
    # Remember this tile by adding it to our list of known tiles
    # Mark that the tile has now been analysed
    analysed_tiles[tile["Index"]]["State"] = "ANALYSED"
    analysed_tiles[tile["Index"]]["Subject"] = subject


# Check Microsoft API results for an animal
#
# Inputs:
#   msapi_response: JSON dictionary - A dictionary containing all the
#                                     information the Microsoft API has returned
#   animal_list:    list of strings - A list of all the possible animals in
#                                     the game
# Outputs:
#   string - The name of the animal
#
# Given the result of the Analyse Image API call and the list of animals,
# returns whether there is an animal in the image
def check_for_animal(msapi_response, animal_list):
    # Initialise our subject to None
    subject = None
    # For every tag in the returned tags, in descending confidence order
    for tag in sorted(msapi_response["tags"], key=lambda x: x['confidence'], reverse=True):
        # If the tag has a name and that name is one of the animals in our list
        if "name" in tag and tag["name"] in animal_list:
            # Record the name of the animal that is the subject of the tile
            # (We store the subject in lowercase to make comparisons easier)
            subject = tag["name"].lower()
            # Print out the animal we have found here ----------------->
            print("Animal: {}".format(subject))
            # Exit the for loop
            break
    # Return the subject
    return subject


# ----------------------------------- TODO -----------------------------------
#
# Inputs:
#   msapi_response: JSON dictionary - A dictionary containing all the
#                                     information the Microsoft API has returned
# Outputs:
#   string - The name of the animal
#
# Given the result of the Analyse Image API call, returns whether there is a
# landmark in the image
def check_for_landmark(msapi_response):
    # TODO: We strongly recommend copying the result of the Microsoft API into
    # a JSON formatter (e.g. https://jsonlint.com/) to better understand what
    # the API is returning and how you will access the landmark information
    # that you need.
    # Here is an example of accessing the information in the JSON:
    # msapi_response["categories"][0]["detail"]["landmarks"][0]["name"].lower()

    # Initialise our subject to None
    subject = None
    # For every category in the returned categories

    # If the category has detail provided, and the detail contains a landmark

    # Record the name of the landmark that is the subject of the tile
    # (We usually store the subject in lowercase to make comparisons easier)

    # Print the landmark we have found here ----------------->

    # Exit the for loop

    # Return the subject
    return subject


# Find matching tile subjects
#
# Outputs:
#   list of integers - A list of two tile indexes that have matching subjects
#
# Search through analysed_tiles for two tiles recorded
# under the same subject
def search_for_matching_tiles():
    # For every tile subject and its index
    for index_1, tile_1 in enumerate(analysed_tiles):
        # Loop through every tile subject and index
        for index_2, tile_2 in enumerate(analysed_tiles):
            # If the two tile's subject is the same and isn't None and the tile
            # hasn't been matched before, and the tiles aren't the same tile
            if tile_1["State"] == tile_2["State"] == "ANALYSED" and tile_1["Subject"] == tile_2["Subject"] and tile_1["Subject"] is not None and index_1 != index_2:
                # Choose these two tiles
                # Return the two chosen tiles as a list
                return [index_1, index_2]
    # If we have not matched any tiles, return no matched tiles
    return None


# Call the Microsoft API
#
# Inputs:
#   url:     string     - The url to the Microsoft API
#   params:  dictionary - Configuration parameters for the request
#   headers: dictionary - Subscription key to allow request to be made
#   data:    dictionary - Input to the API request
# Outputs:
#   JSON dictionary - The result of the API call
#
# Given the parameters, makes a request to the specified url, the request is
# retried as long as there is a volume quota error
def microsoft_api_call(url, params, headers, data):
    # Make API request
    response = requests.post(url, params=params, headers=headers, json=data)
    # Convert result to JSON
    res = response.json()
    # While we have exceeded our request volume quota
    while "statusCode" in res and res["statusCode"] == 429:
        # Wait for 1 second
        sleep(1)
        # Print that we are retrying the API call here ----------------->
        print("Retrying")
        # Make API request
        response = requests.post(url, params=params, headers=headers, json=data)
        # Convert result to JSON
        res = response.json()
    # Print the result of the API call here ----------------->
    print(res)
    # Return JSON result of API request
    return res
