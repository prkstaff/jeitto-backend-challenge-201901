from unittest import TestCase
import requests


class TestCrud(TestCase):
    def setUp(self):
        self.hostname = "http://localhost:5000"

    def test_get_companies_portfolio(self):
        response = requests.get(self.hostname + "/CompanyProducts")
        headers = response.headers

        # assert Json Header
        self.assertEqual('application/json', headers['Content-Type'])

        # assert status code
        self.assertEqual(response.status_code, 200)

        portfolios = response.json()
        for portfolio in portfolios:
            self.assertTrue(all(['company_id' in portfolio, 'products' in portfolio]))
            for product in portfolio['products']:
                self.assertTrue(all(['id' in product, 'value' in product]))
