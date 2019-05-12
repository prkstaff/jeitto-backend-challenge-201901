import unittest
from app import app
import json


class TestCrud(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.hostname = "http://localhost:5000"

    def test_get_companies_portfolio(self):
        response = self.client.get("/CompanyProducts")
        headers = response.headers

        # assert Json Header
        self.assertEqual('application/json', headers['Content-Type'])

        # assert status code
        self.assertEqual(response.status_code, 200)

        portfolios = json.loads(response.data)
        for portfolio in portfolios:
            self.assertTrue(all(['company_id' in portfolio, 'products' in portfolio]))
            for product in portfolio['products']:
                self.assertTrue(all(['id' in product, 'value' in product]))
