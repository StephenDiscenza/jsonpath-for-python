import re


def search_json(jsonDocument, pathItems: list):
    '''
    Uses parsed JSONPath components to recursively search though 
    Python lists and dicts which represent a valid JSON structure.
    '''
    if len(pathItems) == 0:
        return jsonDocument
    pathInfo = re.findall(r"[\w\s\d\-\+\%\']+", pathItems[0])
    if len(pathInfo) == 1: # searching a dict
        jsonDocument = jsonDocument.get(pathInfo[0])

    # Searching a list and we have the index
    elif len(pathInfo) == 2: 
        field, index = pathInfo
        try:
            jsonDocument = jsonDocument.get(field)[int(index)]
        except IndexError: 
            # This index does not exist in the data so we return nothing
            return None
    
    # Searching a list and we have a number of subfield/value pairs like [?subfield="value"]
    elif len(pathInfo) >= 3: 
        field = pathInfo[0]
        if type(jsonDocument.get(field)) != list:
            raise Exception(f'Cannot query {jsonDocument.get(field)}. It is not a list')
        # Check for matches for each subfield/value pair
        count_of_pairs = len(pathInfo) - 1        
        for item in jsonDocument.get(field):
            found_match = True
            pairs_index = 1
            while pairs_index < count_of_pairs:
                subfield = pathInfo[pairs_index]
                value = pathInfo[pairs_index + 1].lstrip("'").rstrip("'")
                if str(item.get(subfield)) != value:
                    found_match = False
                    break
                pairs_index += 2
            if found_match == True:
                jsonDocument = item
                return search_json(jsonDocument, pathItems[1:])  
        # If data being searched couldn't be found for we return None
        return None 
    return search_json(jsonDocument, pathItems[1:])


def get_json_item(jsonDocument, path: str):
    '''
    Uses supplied JSONPath to search for and return a value or 
    object from the JSON document. 
    '''
    try:
        pathItems = path.split(".")[1:]
        result = search_json(jsonDocument, pathItems)
    except IndexError:
        result = None
    except:
        raise Exception(f'An unexpected error occured in get_json_request_item. The path was: {path}')
    else:
        return result


def update_json_element(jsonDocument, path: str, value):
    '''
    Upserts the value of the field specified by the supplied path.
    '''
    try:
        pathItems = path.split(".")[1:]
        containingDict = search_json(jsonDocument, pathItems[:-1])
        containingDict[pathItems[-1]] = value
    except:
        raise Exception('Dang, update failed for path: {path}')


def write_new_json_element(jsonDocument, path: str, value, newElementName=None):
    '''
    Inserts new data into the JSON document. When adding a new value to a list (array)
    newElementName should be ommitted.
    '''
    pathItems = path.split(".")[1:]
    insertLocation = search_json(jsonDocument, pathItems)
    if type(insertLocation) == list:
        insertLocation.append(value)
    else:
        try: 
            insertLocation[newElementName] = value
        except:
            raise Exception(f'Dang, could not write a new element at {path}')

