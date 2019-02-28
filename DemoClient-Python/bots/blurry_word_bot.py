from time import sleep
import json
import requests
from bots.mover import persistentData

headers_visual = {'Ocp-Apim-Subscription-Key': 'YOUR_MICROSOFT_COMPUTER_VISION_API_KEY_HERE'}
headers_spell = {'Ocp-Apim-Subscription-Key': 'YOUR_MICROSOFT_BING_SPELL_CHECK_API_KEY_HERE',
                 'Content-Type': 'application/x-www-form-urlencoded'}


def calculateMove(gameState):
    if 'num_analysed_images' not in persistentData:  # If we haven't analysed any images (start of game)
        persistentData['num_analysed_images'] = 0  # Initialise the number of analysed images to zero
    img_num = persistentData['num_analysed_images']  # Set 'img_num' equal to the next image to be analysed
    images = gameState['Images']  # Get the list of image URLs
    cur_image = images[img_num]  # Get the next image URL to analyse
    while True:
        try:
            ocr_text = imageToText(cur_image)  # Converts image to text using Microsoft's Computer Vision API
        except requests.exceptions.HTTPError:  # If there is a problem with the API call
            sleep(2)  # Wait for 2 seconds before trying again
        else:
            break
    while True:
        try:
            spell_checked_text = spellCheck(
                ocr_text)  # Try to fix any spelling mistakes using Microsoft's Bing Spell Check API
        except requests.exceptions.HTTPError:  # If there is a problem with the API call
            sleep(2)  # Wait for 2 seconds before trying again
        else:
            break
    if img_num < len(images) - 1:  # If there are more images to analyse
        persistentData['num_analysed_images'] += 1  # Increment the number of images we have analysed
    else:  # Otherwise if we have analysed all of the images
        persistentData['num_analysed_images'] = 0  # Start from the beginning again
    return {'Index': img_num,
            'Guess': spell_checked_text}  # Submit 'spell_checked_text' as a guess for image number 'img_num'


def imageToText(img):  # Given an image, converts the text in that image to a string
    # Set the URL for the API call
    url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/ocr?language=en&detectOrientation=True'
    body = {'url': img}  # Set the body of our API call to be the image URL
    response = requests.post(url, data=json.dumps(body),
                             headers=headers_visual)  # Send the API request using our API key as the header
    response.raise_for_status()  # Raise an error if request failed (Usually caused by invalid API key)
    data = json.loads(response.text)  # Convert the Response object into JSON

    text = ''  # Initialise our result string

    if 'regions' in data:  # If at least one region of text has been identified
        for region in data['regions']:  # For every region of text in the image
            if 'lines' in region:  # If at least one line of text has been identified in the region
                for line in region['lines']:  # For every line of text in the current region
                    if 'words' in line:  # If at least one word has been identified in the line
                        for word in line['words']:  # For every word in the current line
                            text += word['text'] + " "  # Add the word our result
    text = text[:-1]  # Remove the surplus white space we added onto the end of the final word
    return text  # Return our result


def spellCheck(text):  # Given a string, attempt to correct the spelling errors within it
    # Set the URL for the API call
    url = 'https://api.cognitive.microsoft.com/bing/v7.0/spellcheck/?mode=proof&mkt=en-GB'
    body = 'Text=' + text  # Set the body of our API call to be the input string
    response = requests.post(url, data=body.encode('utf-8'),
                             headers=headers_spell)  # Send the API request using our API key as the header
    response.raise_for_status()  # Raise an error if request failed (Usually caused by invalid API key)
    data = json.loads(response.text)  # Convert the Response object into JSON

    progress = 0  # Set our progress through the input string to zero
    corrected_text = ''  # Initialise our result string
    if 'flaggedTokens' in data:  # If at least one error has been detected in the string
        for error in data['flaggedTokens']:  # For every suggested correction
            location = error['offset']  # Record the starting location of the misspelt word
            misspelt = error['token']  # Record the misspelt word
            correction = error['suggestions'][0][
                'suggestion']  # Set the correction equal to the first suggested word in the list of suggestions
            corrected_text += text[
                              progress:location] + correction  # Add all the text from the end of the previous mistake to the start of the new one; followed by the corrected word
            progress = location + len(
                misspelt)  # Set our progress through the text to the end of the current misspelling
    corrected_text += text[progress:]  # Add all the remaining text
    return corrected_text  # Return our result
