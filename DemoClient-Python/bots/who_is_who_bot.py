from random import choice
import requests
from itertools import zip_longest, chain

headers_face = {'Ocp-Apim-Subscription-Key': 'YOUR-MICROSOFT-FACE-API-KEY-HERE'}
headers_vision = {'Ocp-Apim-Subscription-Key': 'YOUR-MICROSOFT-COMPUTER-VISION-API-KEY-HERE'}

face_api_url = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/detect'
face_compare_api_url = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/verify'
ocr_vision_api_url = 'https://westeurope.api.cognitive.microsoft.com/vision/v1.0/ocr'


# =============================================================================
# This calculateMove() function is where you need to write your code. When it
# is first loaded. After you enter your Microsoft API keys it will play a complete 
# game for you using the Helper functions that are defined below. The Helper 
# functions give great example code that shows you how to manipulate the data you 
# receive and the move that you have to return.
#

def calculateMove(gameState):
    # Print the gameState that describes the current state of the game, prints appear over here ----->
    print(gameState)

    # There are three different rounds in this game. We need to make different
    # moves depending on the round we are in.

    # There are three rounds in the following order:
    # - CHOOSE CHARACTER: This is where you choose the character your opponent has to guess
    # - QUESTIONS: This is where you ask questions about the character you have to guess
    # - GUESS OPPONENT: This is where you compare the image of the character you correctly
    #                   guessed against a lineup of other characters and an alternative image
    #                   of the correct character

    # ---------------------- If we are in the first round ----------------------
    if gameState["Round"] == "CHOOSE CHARACTER":
        # Initialise our variables for storing information about the characters name and face attributes
        characterFaces = []
        characterNames = []
        # We are provided with a list of image urls that contain the characters in the game
        # There are multiple characters on each image
        # We will loop through every image of characters that we are provided with
        for grid in gameState["ImageGrids"]:
            # For every image we will call Microsoft's OCR API 
            # to determine the names of the characters

            # We will set the parameters for the OCR call as follows:
            # 'language': 'unk' - This sets the language to auto-detection
            # 'detectOrientation ': 'false' - We know all of our text will be oriented correctly
            params_ocr = {'language': 'unk', 'detectOrientation ': 'false'}
            # We will set the input JSON for the OCR call to contain the URL to our image
            json = {"url": grid}
            # Now we make the call to the Microsoft API and get a response
            response = requests.post(ocr_vision_api_url, params=params_ocr, headers=headers_vision, json=json)
            # Here we convert the response to JSON
            names = response.json()
            print(names)  # Print the response to the console ----->
            # The response from the API needs to be ordered sensibly 
            # which we do in the listNames function
            # (we highly recommend improving this function to work more reliably)
            characterNames = listNames(names, characterNames)
            # Now you have a list of the names of the characters in our game


            # We recommend calling the Microsoft Face API next, in a similar way to how
            # we called the OCR API above. We will need to specify the parameters and the
            # JSON input

            # Check out Microsoft's documentation here for more information:
            # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395236
            # We advise collecting the following face attributes:
            # age, gender,smile, facialHair, glasses, emotion, hair, accessories
            # params_face = {}
            # json = {}

            # Now we should make the call to the Microsoft API and get a response
            # response = 

            # Then convert the response to JSON
            # faces = 
            # print(faces)  # Print the response to the console ----->


            # With your face data, we have provided a short helper function listFaces()
            # that 'should' organise the faces into the same order that the names were 
            # listed. There is definitely room for improvment here
            # characterFaces = listFaces(faces, characterFaces)

        # Now we have looped through all of the images and gathered all of our data
        # we will save this data into 'persistentData' for later use
        persistentData["Names"] = characterNames
        persistentData["Faces"] = characterFaces
        # Here we print out the information to see what has been returned ---->
        print("Name information: {0}".format(persistentData["Names"]))
        print("Face information: {0}".format(persistentData["Faces"]))
        # All that is left is for us to make our move. In this round we need to choose
        # a character that our opponent has to guess. This is represented by the character's
        # index. Their index represents their position in the images so index 0 would be the
        # top left character in the first image, 15 would be the bottom right character in the
        # first image, and 31 would be the bottom right character in the second image, etc.

        # We shall keep this simple and always choose the character in the top left of the
        # first image. i.e. index 0 (This may not be the best strategy)
        character = 0
        # Now we format our move correctly as a JSON key-value pair and return it
        return {"MyCharacter": character}
    # ---------------------- If we are in the second round ----------------------
    elif gameState["Round"] == "QUESTIONS":
        # We do not know how far through the second round we are yet so let's check

        # If there are more than seven potential characters left for us to choose from
        if len(gameState["RemainingCharacters"]) > 7:
            # We will ask another random question
            question = choice(gameState["RemainingQuestions"])
            # You will notice that during your games you will end up making invalid moves.
            # This is because some of the questions in "RemainingQuestions" need extra
            # information. (The "Name" and "Age" questions.) We advise either adding the
            # extra information to these questions or not asking them.

            # Now we return our question. Notice that our question is part of a list. If you
            # add extra questions to this list they will be treated as one big question
            # separated by 'and's. e.g. [["Hair", "Black"],["Gender", "Male"]] is equivalent
            # to asking "Are they a male with black hair?"
            return {"Questions": [question]}
        else:  # If there are seven or less potential characters left for us to choose from
            # We are going to attempt to guess the name of our opponent's character. We will
            # do this by randomly guessing one of the names we recorded in persistentData in
            # the first round.
            question = ["Name", "Is", choice(persistentData["Names"])]
            # We should be able to ask a better question though since we have already eliminated
            # plenty of characters with our other questions, it seems inefficient to guess names
            # of characters that have been eliminated
            # question = ["Name", "Is", persistentData["Names"][choice(gameState["RemainingCharacters"])]]

            # Now we format our move correctly as a JSON key-value pair and return it
            # Note: It would be a bad idea to add multiple questions here. Why is that?
            return {"Questions": [question]}  # If we are correct we will progress to the third round
    # ---------------------- If we are in the third and final round ----------------------
    else:
        # In this round we have been presented with a lineup of characters,
        # one of them is an alternative image of the character we guessed in
        # the previous round

        # To start with we will simply choose a random person 
        # from that lineup whom we haven't yet eliminated
        guess = choice(gameState["RemainingCharacters"])

        # We reckon the best approach to this round is to use Microsoft's face
        # verification API to compare our character "MyCharacterImage" with the
        # list of people in the lineup "ComparisonImages"

        # Commented below is the start of a function that will help you choose
        # the person from the lineup who looks most like our character. It is up
        # to you to complete it!
        # listComparisons(gameState["ComparisonImages"], gameState["MyCharacterImage"])

        # Now we format our move correctly as a JSON key-value pair and return it
        return {"OppCharacter": guess}


# The aim of this function is given the result from the Computer Vision OCR API "nameData"
# and a list of names "currentList", we will append the character names to the list of names
# in index order
def listNames(nameData, currentList):
    # The OCR API breaks the image down into "regions", these regions are usually
    # columns of text
    # Let's initialise the list of columns as an empty list
    columns = []
    # For every column (region) in the list of regions we receive
    for column in nameData["regions"]:
        # We first initialise the names we have found in the current column to an empty list
        curColumn = []
        # For every name (line of text) in the list of lines in the current column
        for name in column["lines"]:
            # Every line contains a list of "words", we should combine these
            # words to form the name and then add that name to our current column list
            n = ""  # Initialise our name so far as an empty string
            for part in name["words"]:  # For every word on the line
                n += part["text"]  # Join it to our name so far 'n'
                n += " "  # Along with a space
            # Remove the last space from the end of the name
            n = n[:-1]
            # Now we append that name to the list of names in the current column
            curColumn.append(n)
        # We now append our column of names to the list of columns
        columns.append(curColumn)
    # Unfortunately a list of columns isn't how we want to record our names. The index order
    # is a list of rows. Luckily the following complicated-looking line of code fixes this
    # for us and we append the list to the existing inputted list
    currentList += list(filter(None.__ne__, chain(*zip_longest(*columns))))

    # Now we return the updated list
    return currentList


# Given the result from the Microsoft Face API "faceData" and a list of faces and 
# their attributes we append the face attributes of the characters to current list 
# in index order
def listFaces(faceData, currentList):
    # Since we know that the height of every person is 280 and the width is 250 we can
    # work out where each face belongs in the index by sorting the list as follows
    faceData.sort(key=lambda x: int(x["faceRectangle"]["top"] / 280) * 4 + int(x["faceRectangle"]["left"] / 250))

    # TODO Check whether there are multiple faces in a single photo

    # Next we append these face attributes to our existing inputted list
    currentList += [x["faceAttributes"] for x in faceData]

    # Now we return the updated list
    return currentList


    # Given the comparison image urls "comparisonImages", and the image they should be
    # compared against "myCharacterImage", returns a list of confidence values of how
    # likely the character in the lineup is to be the same person as myCharacterImage
    # def listComparisons(comparisonImages, myCharacterImage):
    # To get a confidence value that two faces belong to the same person
    # we need to use Microsoft's Face Verification API, an example request 
    # to this API would be as follows:
    # response = requests.post(face_compare_api_url, params={}, headers=headers_face, json={'faceId1': my_face_id, 'faceId2': comparison_id})
    # Notice that the inputted JSON contains two key-value pairs 'faceId1' and 'faceId2',
    # unlike the previous API calls instead of providing a URL to an image we need to
    # provide two face ids.
    # We can get these faceIds from the Face API we used in round 1, then with these ids
    # we can compare the faces in the lineup to our character.

    # Get MyCharacter face id

    # params_face = {
    #     'returnFaceId': 'true',
    #     'returnFaceLandmarks': 'false',
    #     'returnFaceAttributes': '',
    # }
    # response = requests.post(face_api_url, params=params_face, headers=headers_face, json={"url": myCharacterImage})
    # faces = response.json()
    # my_face_id = faces[0]["faceId"]


    # Then similarly for every image in the lineup, get their face id

    # And finally compare the face ids of the lineup to your character's face id similar to below
    # response = requests.post(face_compare_api_url, params={}, headers=headers_face, json={'faceId1': my_face_id, 'faceId2': comparison_id})
    # comparison = response.json()

    # Check out Microsoft's documentation here for more information:
    # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f3039523a

    # Now return your results