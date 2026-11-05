import jsonschema
import requests
import pytest

BASE_URL = "https://guild-expedition.fly.dev"


candidate_schema = {"required":["candidate_id", "name", "job", "level"], 
                    "properties" : {
                        "canditate_id" : { "type" : "integer" },
                        "job" : {"type" : "string"},
                        "level" : {"type" : "integer"},
                        "guild" : {"type" : "string"}
                    }}

def test_candidate_matches_schema():
    response = requests.get("https://guild-expedition.fly.dev/heroes/candidates/3")

    #                    instance : 검사 대상        schema : 기대 결과     
    jsonschema.validate(instance=response.json(), schema=candidate_schema)


