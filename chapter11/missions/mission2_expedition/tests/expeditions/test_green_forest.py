import time

import pytest
import requests

BASE_URL = "https://guild-expedition.fly.dev"


# TODO 1 · party Fixture (scope="class") · 인자 guild


# TODO 2 · guild Fixture (scope="class") · 인자 token


# TODO 3 · 클래스 전체에 expedition 마커 (pytest.ini 에 이미 등록되어 있습니다)
class TestGreenForest:

    def test_order_items(self, guild, party):
        response = requests.post(BASE_URL + "/guild/orders", json={"item_id": 102, "quantity": 1}, headers=guild)
        assert response.status_code == 201, f"강철 검 주문: 기대 201, 실제 {response.status_code}"
        assert response.json()["remaining_gold"] == 1500, f"검 주문 뒤 골드: 실제 {response.json()['remaining_gold']}"

        response = requests.post(BASE_URL + "/guild/orders", json={"item_id": 201, "quantity": 1}, headers=guild)
        assert response.status_code == 201, f"가죽 갑옷 주문: 기대 201, 실제 {response.status_code}"
        assert response.json()["remaining_gold"] == 1350, f"갑옷 주문 뒤 골드: 실제 {response.json()['remaining_gold']}"

    def test_equip_arin(self, guild, party):
        url = BASE_URL + f"/guild/heroes/{party['arin_id']}/equipment"
        response = requests.put(url, json={"weapon": 102, "armor": 201}, headers=guild)
        assert response.status_code == 200, f"장착: 기대 200, 실제 {response.status_code}"

        total_power = response.json()["total_power"]
        assert total_power == 185, f"아린 총 전투력: 기대 185, 실제 {total_power}"

    def test_storage_is_empty(self, guild):
        data = requests.get(BASE_URL + "/guild/storage", headers=guild).json()
        assert data["total"] == 0, f"창고 종류 수: 기대 0, 실제 {data['total']}"

    def test_party_power(self, guild, party):
        response = requests.get(BASE_URL + "/guild/heroes", headers=guild)
        heroes = {hero["hero_id"]: hero for hero in response.json()["items"]}

        assert heroes[party["arin_id"]]["total_power"] == 185
        assert heroes[party["doyun_id"]]["total_power"] == 140

        party_power = sum(hero["total_power"] for hero in heroes.values())
        assert party_power == 325, f"파티 전투력: 기대 325, 실제 {party_power}"

        required = requests.get(BASE_URL + "/dungeons/1").json()["required_power"]
        assert party_power >= required, f"파티 {party_power}, 필요 {required}"

    def test_send_expedition(self, guild, party):
        body = {"dungeon_id": 1, "hero_ids": [party["arin_id"], party["doyun_id"]]}
        response = requests.post(BASE_URL + "/guild/expeditions", json=body, headers=guild)
        assert response.status_code == 202, f"원정 접수: 기대 202, 실제 {response.status_code}"

        data = response.json()
        assert data["party_power"] == 325, f"파티 전투력: 기대 325, 실제 {data['party_power']}"
        assert data["status"] == "IN_PROGRESS"
        assert data["duration_seconds"] == 2
        TestGreenForest.expedition_id = data["expedition_id"]

    def test_reward_before_complete(self, guild):
        response = requests.post(BASE_URL + f"/guild/expeditions/{self.expedition_id}/reward", headers=guild)
        assert response.status_code == 409, f"이른 보상 요청: 기대 409, 실제 {response.status_code}"
        assert response.json()["error_code"] == "NOT_COMPLETED"

    def test_claim_reward(self, guild):
        expedition_url = BASE_URL + f"/guild/expeditions/{self.expedition_id}"
        time.sleep(3)
        status = requests.get(expedition_url, headers=guild).json()["status"]
        assert status == "COMPLETED", f"원정 상태: 기대 COMPLETED, 실제 {status}"

        response = requests.post(expedition_url + "/reward", headers=guild)
        assert response.status_code == 200, f"보상 수령: 기대 200, 실제 {response.status_code}"

        data = response.json()
        assert data["gold_reward"] == 300, f"보상 골드: 기대 300, 실제 {data['gold_reward']}"
        assert data["fame_reward"] == 10, f"보상 명성: 기대 10, 실제 {data['fame_reward']}"
        assert data["gold"] == 1650, f"보상 뒤 골드: 기대 1650, 실제 {data['gold']}"

    def test_guild_after(self, guild):
        data = requests.get(BASE_URL + "/guild", headers=guild).json()
        assert data["gold"] == 1650, f"최종 골드: 기대 1650, 실제 {data['gold']}"
        assert data["fame"] == 10, f"최종 명성: 기대 10, 실제 {data['fame']}"
        assert data["hero_count"] == 2, f"영웅 수: 기대 2, 실제 {data['hero_count']}"
