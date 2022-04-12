import re


def search_json(jsonDocument, pathItems):
    '''
    Uses parsed JSONPath components to recursively search though 
    Python lists and dicts which represent a valid JSON structure.
    '''
    if len(pathItems) == 0:
        return jsonDocument
    pathInfo = re.findall(r"[\w\s\d\-\+\%\']+", pathItems[0])
    if len(pathInfo) == 1: # searching a dict
        jsonDocument = jsonDocument.get(pathInfo[0])

    elif len(pathInfo) == 2: # searching a list and we have the index
        field, index = pathInfo
        jsonDocument = jsonDocument.get(field)[int(index)]
    
    elif len(pathInfo) == 3: # searching a list and we have a subfield/value pair like [?subfield="value"]
        field, subfield, value = pathInfo
        value = value.lstrip("'").rstrip("'")
        if type(jsonDocument.get(field)) != list:
            raise Exception(f'Cannot query {jsonDocument.get(field)} with ?{subfield}={value}')
        for item in jsonDocument.get(field):
            if str(item.get(subfield)) == value:
                jsonDocument = item
                return search_json(jsonDocument, pathItems[1:])
        return None #If item not in list
    
    return search_json(jsonDocument, pathItems[1:])


def get_json_item(jsonDocument, path):
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


def update_json_element(jsonDocument, path, value):
    '''
    Upserts the value of the field specified by the supplied path.
    '''
    try:
        pathItems = path.split(".")[1:]
        containingDict = search_json(jsonDocument, pathItems[:-1])
        containingDict[pathItems[-1]] = value
    except:
        raise Exception('Dang, update failed for path: {path}')


def write_new_json_element(jsonDocument, path, value, newElementName=None):
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

