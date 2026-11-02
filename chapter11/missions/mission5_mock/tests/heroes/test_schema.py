import jsonschema
import pytest
import requests

BASE_URL = "https://guild-expedition.fly.dev"


CANDIDATE_SCHEMA = {
    "type": "object",
    "required": ["candidate_id", "name", "job", "level", "power", "cost"],
    "properties": {
        "candidate_id": {"type": "integer"},
        "name": {"type": "string"},
        "job": {"type": "string"},
        "level": {"type": "integer", "minimum": 1},
        "power": {"type": "integer", "minimum": 0},
        "cost": {"type": "integer", "minimum": 0},
    },
}


def test_candidate_matches_schema():
    response = requests.get(BASE_URL + "/heroes/candidates/3")
    jsonschema.validate(instance=response.json(), schema=CANDIDATE_SCHEMA)


def test_string_power_fails_schema():
    data = requests.get(BASE_URL + "/heroes/candidates/3").json()
    data["power"] = str(data["power"])

    with pytest.raises(jsonschema.ValidationError) as error:
        jsonschema.validate(instance=data, schema=CANDIDATE_SCHEMA)
    print("오류 메시지:", error.value.message)


@pytest.fixture(scope="session")
def openapi_spec():
    response = requests.get(BASE_URL + "/openapi.json")
    assert response.status_code == 200, f"openapi.json: 기대 200, 실제 {response.status_code}"
    return response.json()


def hero_list_schema(spec):
    return {
        "$ref": "#/components/schemas/HeroList",
        "components": spec["components"],
    }


GUILD_SCHEMA = {
    "type": "object",
    "required": ["guild_name", "master", "gold", "fame", "hero_count", "max_heroes"],
    "properties": {
        "guild_name": {"type": "string"},
        "master": {"type": "string"},
        "gold": {"type": "integer", "minimum": 0},
        "fame": {"type": "integer", "minimum": 0},
        "hero_count": {"type": "integer", "minimum": 0},
        "max_heroes": {"type": "integer"},
    },
}


def test_guild_matches_schema(guild):
    data = requests.get(BASE_URL + "/guild", headers=guild).json()
    jsonschema.validate(instance=data, schema=GUILD_SCHEMA)


def test_hero_list_matches_schema(guild, openapi_spec):
    requests.post(BASE_URL + "/guild/heroes", json={"candidate_id": 1}, headers=guild)
    requests.post(BASE_URL + "/guild/heroes", json={"candidate_id": 7}, headers=guild)

    data = requests.get(BASE_URL + "/guild/heroes", headers=guild).json()
    jsonschema.validate(instance=data, schema=hero_list_schema(openapi_spec))


def test_wrong_type_fails_schema(guild, openapi_spec):
    requests.post(BASE_URL + "/guild/heroes", json={"candidate_id": 1}, headers=guild)
    data = requests.get(BASE_URL + "/guild/heroes", headers=guild).json()
    data["items"][0]["total_power"] = "120"

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=data, schema=hero_list_schema(openapi_spec))


def test_missing_key_fails_schema(guild, openapi_spec):
    requests.post(BASE_URL + "/guild/heroes", json={"candidate_id": 1}, headers=guild)
    data = requests.get(BASE_URL + "/guild/heroes", headers=guild).json()
    del data["items"][0]["candidate_id"]

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=data, schema=hero_list_schema(openapi_spec))
