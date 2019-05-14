from flask import Flask, jsonify
from settings import app
from models import CompanyProduct, Company


@app.route('/CompanyProducts', methods=["GET"])
def get_companies_portfolio():
    portfolios = []
    for company in Company.query.all():
        portfolio = {}
        portfolio["company_id"] = company.id
        portfolio["products"] = CompanyProduct.get_list_of_products_from_company(company.id)
        portfolios.append(portfolio)
    return jsonify(portfolios)


app.run(host='0.0.0.0')
