import unittest
from app import app
import json
from models import db, Company, CompanyProduct, PhoneRecharge
import copy

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

    def check_app_json_and_status_code(self, response, expected_code):
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual(response.status_code, expected_code)

    def test_get_companies_portfolio(self):
        self.populate_some_data()
        response = self.client.get("/CompanyProducts")
        headers = response.headers

        self.check_app_json_and_status_code(response, 200)

        portfolios = json.loads(response.data)

        portfolios_expect = [
            {'company_id': 'claro_11', 
             'products': [
                 {'id': 'claro_10', 'value': 10.0}, 
                 {'id': 'claro_20', 'value': 20.0}]}, 
            {'company_id': 'tim_11', 
             'products': [
                 {'id': 'tim_10', 'value': 10.0}, 
                 {'id': 'tim_20', 'value': 20.0}]}]
        self.assertEqual(portfolios, portfolios_expect)

    def test_get_company_portfolio(self):
        self.populate_some_data()
        response = self.client.get("/CompanyProducts?company_id=claro_11")

        self.check_app_json_and_status_code(response, 200)

        portfolio_expected = {
            'company': 'claro_11',
            'products': [
                {'id': 'claro_10', 'value': 10.0},
                {'id': 'claro_20', 'value': 20.0}]}
        self.assertEqual(portfolio_expected, json.loads(response.data))

        # non-existent company ID test
        response2 = self.client.get("/CompanyProducts?company_id=claro_xy")

        self.check_app_json_and_status_code(response2, 404)

        expected_error = {
            'error': 'Company with id claro_xy was not found'}
        self.assertEqual(expected_error, json.loads(response2.data))

    def test_do_recharge(self):
        self.populate_some_data()
        new_recharge = {
           "company_id": "claro_11",
           "product_id": "claro_10",
           "phone_number": "5511999999999",
           "value": 10.00
        }

        # test valid recharge
        response = self.client.post('/PhoneRecharges', json=new_recharge)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers['Location'], 'http://localhost/PhoneRecharges?id=1')

        # test with wrong number
        recharge_with_wrong_number = copy.deepcopy(new_recharge)
        recharge_with_wrong_number['phone_number'] = "969997509"
        response = self.client.post('/PhoneRecharges', json=recharge_with_wrong_number)
        self.check_app_json_and_status_code(response, 422)
        self.assertEqual(json.loads(response.data), {"error": "Not acceptable phone format"})
        
        # test with wrong company ID
        recharge_with_wrong_cid = copy.deepcopy(new_recharge)
        recharge_with_wrong_cid['company_id'] = "claro_0"
        response = self.client.post('/PhoneRecharges', json=recharge_with_wrong_cid)
        self.check_app_json_and_status_code(response, 422)
        self.assertEqual(json.loads(response.data), {'error': 'Not a valid Recharge option'})

        # test with wrong product id
        recharge_with_wrong_product_id = copy.deepcopy(new_recharge)
        recharge_with_wrong_product_id['product_id'] = 'claro_0'
        response = self.client.post('PhoneRecharges', json=recharge_with_wrong_product_id)
        self.check_app_json_and_status_code(response, 422)
        self.assertEqual(json.loads(response.data), {'error': 'Not a valid Recharge option'})

        # test with wrong value 
        recharge_with_wrong_value = copy.deepcopy(new_recharge)
        recharge_with_wrong_value['value'] = 7.0
        response = self.client.post('PhoneRecharges', json=recharge_with_wrong_value)
        self.check_app_json_and_status_code(response, 422)
        self.assertEqual(json.loads(response.data), {'error': 'Not a valid Recharge option'})


    def tearDown(self):
        db.session.remove()
        db.drop_all()
