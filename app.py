from flask import Flask, jsonify, Response
from settings import app
from models import CompanyProduct, Company
import json


@app.route('/CompanyProducts', methods=["GET"])
def get_companies_portfolio():
    portfolios = []
    for company in Company.query.all():
        portfolio = {}
        portfolio["company_id"] = company.id
        portfolio["products"] = CompanyProduct.get_list_of_products_from_company(company.id)
        portfolios.append(portfolio)
    return jsonify(portfolios)


@app.route('/CompanyProducts/<company_id>', methods=['GET'])
def get_company_products(company_id):
    company = CompanyProduct.query.filter_by(id=company_id)
    if company:
        company = company.first()
        data = {
            "company": company_id,
            "products": CompanyProduct.get_list_of_products_from_company(company_id)
        }
        return jsonify(data)
    else:
        invalid_company_id_msg = {
            "error": "Company with id {} was not found".format(company_id)}
        response = Response(json.dumps(invalid_company_id_msg),
                            status=404, mimetype='application/json')


app.run(host='0.0.0.0')
