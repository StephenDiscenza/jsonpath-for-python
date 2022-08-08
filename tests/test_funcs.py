import json
from src.JSONPathLite.main import get_json_item, update_json_element, write_new_json_element
import pytest


# assumes the current working directory is the root of the project
with open('./tests/data.json', 'r') as f:
    TEST_DATA = json.load(f)


def test_get_present_item():
    path = '$.Friends[?Name="Bill"].CanThisFriendLiftMe'
    expected_result = True
    assert get_json_item(TEST_DATA, path) == expected_result , f'Did not find {str(expected_result)} at {path}'
    

def test_get_missing_item():
    path = '$.Friends[?Name="Bob"].CanThisFriendLiftMe'
    expected_result = None
    assert get_json_item(TEST_DATA, path) == expected_result , f'Did not find {str(expected_result)} at {path}'


def test_update_present_item():
    path = '$.Friends[?Name="Sue"].Pets[?Name="Whiskers"].Friendly'
    value = True
    update_json_element(TEST_DATA, path, value)
    assert get_json_item(TEST_DATA, path) == value, f'The value at {path} is not equal to {value}'


def test_update_missing_item():
    path = '$.Friends[?Name="Sue"].Pets[?Name="Spot"].Friendly'
    value = True
    with pytest.raises(Exception):
        update_json_element(TEST_DATA, path, value)


def test_write_field_at_valid_path():
    path = '$.Friends[?Name="Sue"].Pets[?Name="Whiskers"]'
    new_field_name = 'Eats'
    value = 'Mice'
    write_new_json_element(TEST_DATA, path, value, new_field_name)
    assert get_json_item(TEST_DATA, path + '.Eats') == 'Mice', f'The value at {path}.Eats is not Mice'


def test_write_array_at_valid_path():
    path = '$'
    new_array_name = 'Enemies'
    value = []
    write_new_json_element(TEST_DATA, path, value, new_array_name)
    assert get_json_item(TEST_DATA, path + '.Enemies') == [], f'The value at {path}.Enemies is not an empty array'


def test_add_item_to_array():
    path = '$.Enemies'
    value = {'Name': 'Donald', 'IsJerk': True}
    write_new_json_element(TEST_DATA, path, value)
    assert get_json_item(TEST_DATA, path + '[?Name="Donald"].IsJerk') == True, f'The value at {path}+[?Name="Donald"].IsJerk is not True'


def test_add_item_at_invalid_path():
    path = '$.Enemies[?Name="Bill"]'
    new_field_name = 'HostilitiesBegan'
    value = '2022-04-11'
    with pytest.raises(Exception):
        write_new_json_element(TEST_DATA, path, value, new_field_name)
    

def test_multiple_criteria():
    path = '$.Friends[?Name="Bill"].Pets[?Name="Spot"&&Species="Dog"].Name'
    value = 'Spot'
    assert get_json_item(TEST_DATA, path) == value, f'The value at {path} is not {value}.'