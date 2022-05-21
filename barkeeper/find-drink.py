import json

file = open("./data/cocktails.json")
cocktails = json.load(file)

def find_drink(image_ocr):
    image_ocr.capitalize()
    
    choices = []

    for i in range(len(cocktails["cocktails"])):
        cocktail_item = cocktails["cocktails"][i]["name"]
        choices.append(cocktail_item)

    print(choices)

    match = [s for s in choices if s.__contains__(image_ocr)]
    match_count = len(match)
    
    if match_count == 1:
        result = image_ocr + " is found: "+ str(match)
    elif match_count > 1:
        result = image_ocr + " is found with "+ str(match_count) + " matches. Which one would you like to create? " + str(match)    
    else:
        result = image_ocr + " not found. please try again"
    return print(result)

while True:
    image_ocr = input("what drink you want?")
    find_drink(image_ocr)
