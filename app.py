from flask import Flask, jsonify
from settings import app
from models import CompanyProduct, Company


@app.route('/CompanyProducts', methods=["GET"])
def get_companies_portfolio():
    portfolios = []
    for company in Company.query.all():
        portfolio = {}
        portfolio["company_id"] = company.id
        portfolio["products"] = []
        for product in CompanyProduct.query.filter_by(company_id=company.id):
            portfolio["products"].append({
                "id": product.id,
                "value": product.value
            })
        portfolios.append(portfolio)
    return jsonify(portfolios)


app.run(host='0.0.0.0')
