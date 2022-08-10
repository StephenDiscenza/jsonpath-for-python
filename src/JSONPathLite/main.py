import re

from .utils import handle_search_json_exceptions


def search_json(jsonDocument, pathItems: list):
    '''
    Uses parsed JSONPath components to recursively search though 
    Python lists and dicts which represent a valid JSON structure.
    '''
    if len(pathItems) == 0:
        return jsonDocument
    pathInfo = re.findall(r"[\w\s\d\-\+\%\']+", pathItems[0])
    
    # Searching a dict
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
        if not isinstance(jsonDocument.get(field), list):
            raise Exception(f'Cannot query {jsonDocument.get(field)}. It is not a list')
        # Check for matches for each subfield/value pair
        countOfPairs = len(pathInfo) - 1        
        for item in jsonDocument.get(field):
            foundMatch = True
            pairsIndex = 1
            while pairsIndex < countOfPairs:
                subfield = pathInfo[pairsIndex]
                value = pathInfo[pairsIndex + 1].lstrip("'").rstrip("'")
                if str(item.get(subfield)) != value:
                    foundMatch = False
                    break
                pairsIndex += 2
            if foundMatch == True:
                jsonDocument = item
                return search_json(jsonDocument, pathItems[1:])  
        # If data being searched for couldn't be found, return None
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
    except Exception as e:
        raise handle_search_json_exceptions(path, e, 'Get item')
    return result


def update_json_element(jsonDocument, path: str, value):
    '''
    Upserts the value of the field specified by the supplied path.
    '''
    pathItems = path.split(".")[1:]
    try: 
        containingDict = search_json(jsonDocument, pathItems[:-1])
    except Exception as e:
        raise handle_search_json_exceptions(path, e, 'Update')
    # This is really an upsert
    containingDict[pathItems[-1]] = value


def write_new_json_element(jsonDocument, path: str, value, newElementName=None):
    '''
    Inserts new data into the JSON document. When adding a new value to a list (array)
    newElementName should be ommitted.
    '''
    pathItems = path.split(".")[1:]
    try:
        insertLocation = search_json(jsonDocument, pathItems)
    except Exception as e:
        raise handle_search_json_exceptions(path, e, 'Write new')
    if isinstance(insertLocation, list):
        insertLocation.append(value)
    else:
        insertLocation[newElementName] = value


