import main
import json


# assumes the current working directory is the root of the project
with open('./tests/data.json', 'r') as f:
    TEST_DATA = json.load(f)

def new_functionality():
    path = '$.Friends[?Name="Sue"].Pets[?Name="Whiskers"].Friendly'
    value = True
    main.update_json_element(TEST_DATA, path, value)
    print(main.get_json_item(TEST_DATA, path))

if __name__ == '__main__':
    new_functionality()