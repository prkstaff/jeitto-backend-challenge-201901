from flask import Flask, jsonify
from settings import app


@app.route('/CompanyProducts', methods=["GET"])
def HelloWorld():
    companies_portfolio = [
       {
           "company_id": "claro_11",
           "products":[
               {"id": "claro_10", "value": 10.0},
               {"id": "claro_20", "value": 20.0}
           ]
       },
       {
           "company_id": "tim_11",
           "products":[
               {"id": "tim_10", "value": 10.0},
               {"id": "tim_20", "value": 20.0}
           ]
       }
    ]
    return jsonify(companies_portfolio)


app.run(host='0.0.0.0')
