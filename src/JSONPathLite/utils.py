import re

class JSONPathValidationError(Exception):
    pass


class JSONSearchError(Exception):
    pass


def validate_json_path(path: str) -> tuple:
    '''
    Validates that the supplied JSON path is valid. Returns two values. 
    The first element is a boolean where True means the path is valid and the second
    is a list of found syntax errors. 
    '''
    validPatterns = [r'\w+\[\?(\w*="\w*"\]|(\w*="\w*"\s*&&\s*)+\w*="\w*"\])', r'\w*', r'\$', r'\w+\[\d+\]']
    pathItems = path.split(".")
    errors = []
    # Checking each item against all the valid paths. If there are any matches the item is valid
    for item in pathItems:
        itemErrors = []
        itemValid = True
        for pattern in validPatterns:
            if re.fullmatch(pattern, item) != None:
                itemValid = True
                break
            else:
                itemValid = False
        if not itemValid:
            itemErrors.append(item)
            errors += itemErrors
    
    if errors:
        validPath = False
    else:
        validPath = True
    return validPath, errors


def handle_search_json_exceptions(path: str, e: Exception) -> Exception:
    pathIsValid, pathErrors = validate_json_path(path)
    if not pathIsValid:
        errorString = ', '.join(pathErrors)
        return JSONPathValidationError(f'Syntax errors were found in the following parts of the supplied JSON path: {errorString}')
    return JSONSearchError(f'An unexpected error occured in search_json. The path was: {path} and the error is: {repr(e)}')