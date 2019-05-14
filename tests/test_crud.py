import unittest
from app import app
import json
from models import db, Company, CompanyProduct, PhoneRecharge


class TestCrud(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        db.create_all()
        self.client = app.test_client()

    def populate_some_data(self):
        company1 = Company(id="claro_11", name="Claro SP")
        company1_prod1 = CompanyProduct(id="claro_10", value=10.0, company_id="claro_11")
        company1_prod2 = CompanyProduct(id="claro_20", value=20.0, company_id="claro_11")
        db.session.add(company1)
        db.session.add(company1_prod1)
        db.session.add(company1_prod2)
        company2 = Company(id="tim_11", name="Tim SP")
        company2_prod1 = CompanyProduct(id="tim_10", value=10.0, company_id="tim_11")
        company2_prod2 = CompanyProduct(id="tim_20", value=20.0, company_id="tim_11")
        db.session.add(company2)
        db.session.add(company2_prod1)
        db.session.add(company2_prod2)
        db.session.commit()

    def test_get_companies_portfolio(self):
        self.populate_some_data()
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
                self.assertTrue(type(product['value']), float)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
