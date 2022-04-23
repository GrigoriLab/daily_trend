import json
import os

from django.conf import settings

from apps.api.tests.base import BaseTestCase


class SearchInterestTestCase(BaseTestCase):
    fixtures = [
        "trend.json",
        "user.json"
    ]

    def test_search_interest_unauthorized(self):
        resp = self.api_client.get("search_interest/")
        self.assertEqual(resp.status_code, 401)

    def test_get_for_all_keywords(self):
        self.api_client.login("admin", "admin")
        resp = self.api_client.get("search_interest/")
        fixture_data = os.path.join(settings.FIXTURE_DIRS[0], "data/all_keywords.json")
        with open(fixture_data, 'r') as f:
            expected_keywords = json.load(f)
            self.assertDictEqual(expected_keywords, resp.json)

    def test_get_for_keyword(self):
        self.api_client.login("admin", "admin")
        resp = self.api_client.get("search_interest/?keyword=blue%20bloods")
        fixture_data = os.path.join(settings.FIXTURE_DIRS[0], "data/blue_bloods_search_interests.json")
        with open(fixture_data, 'r') as f:
            expected_keywords = json.load(f)
            self.assertDictEqual(expected_keywords, resp.json)
