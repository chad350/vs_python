import jsonschema
import requests

BASE_URL = "https://guild-expedition.fly.dev"



ITEM_SCHEMA = {
    "required" : ["item_id","type" , "name", "power", "price"],
    "properties" : {
        "item_id" : {"type" : "integer"},
        "name" : {"type" : "string"},
        "type" : { "enum": ["weapon", "armor", "potion"] },
        "power" : {"type" : "integer"},
        "price" : {"type" : "integer"},
    }}

# 요청	GET BASE_URL + "/shop/items/101"
def test_item_schema():
    response = requests.get(f"{BASE_URL}/shop/items/101")
    jsonschema.validate(instance=response.json() , schema=ITEM_SCHEMA)



ITEM_LIST_SCHEMA = {
    "required" : ["items", "total"],
    "properties" : {
        "items" : {"type" : "array", "items" : ITEM_SCHEMA},
        "total" : {"type" : "integer"}
    }}

# 요청	GET BASE_URL + "/shop/items"
def test_item_list_schema():
    response = requests.get(f"{BASE_URL}/shop/items")
    jsonschema.validate(instance=response.json() , schema=ITEM_LIST_SCHEMA)


DUNGEON_SCHEMA = {
    "required" : [ "dungeon_id", "name", "required_power", "gold_reward", "fame_reward" ],
    "properties" : {
        "dungeon_id" :      {"type" : "integer"},
        "name" :            {"type" : "string"},
        "required_power" :  {"type" : "integer"},
        "gold_reward" :     {"type" : "integer"},
        "fame_reward" :     {"type" : "integer"},
    }}

# GET /dungeons/1 
def test_dungeon_schema():
    response = requests.get(f"{BASE_URL}/dungeons/1 ")
    jsonschema.validate(instance=response.json() , schema=DUNGEON_SCHEMA)


# dungeon_id	"integer"	필수	1
# name	"string"	필수	초록 숲
# required_power	"integer"	필수 · "minimum": 0	200
# gold_reward	"integer"	필수 · "minimum": 0	300
# fame_reward	"integer"	필수 · "minimum": 0	10



# 요청	GET BASE_URL + "/guild" · headers=guild

# guild_name	"string"	필수	student01 길드
# master	"string"	필수	student01
# gold	"integer"	필수 · "minimum": 0	3000
# fame	"integer"	필수 · "minimum": 0	0
# hero_count	"integer"	필수 · "minimum": 0	0
# max_heroes	"integer"	필수	4



# 요청	GET BASE_URL + "/shop/items/999"
# error_code	"string"	필수	ITEM_NOT_FOUND
# message	"string"	필수	999번 아이템이 없습니다.


