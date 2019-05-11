from unittest import TestCase
import requests

class TestCrud(TestCase):
    def setUp(self):
        self.hostname = "http://localhost:5000"

    def test_insert_company_portfolio(self):
        req = requests.get(self.hostname + "/")
        import pdb
        pdb.set_trace()

