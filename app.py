from flask import jsonify, Response, request
from settings import app
from models import CompanyProduct, Company, PhoneRecharge
import json


@app.route('/CompanyProducts', methods=["GET"])
def get_companies_portfolio():
    # if company id passed
    if 'company_id' in request.args:
        company_id = request.args['company_id']
        company = Company.query.filter_by(id=company_id)
        company = company.first()
        if company:
            data = {
                "company": company_id,
                "products": CompanyProduct.get_list_of_products_from_company(
                    company_id)
            }
            return jsonify(data)
        else:
            response = Response(json.dumps({}),
                                status=204, mimetype='application/json')
            return response
    else:
        portfolios = []
        for company in Company.query.all():
            portfolio = {}
            portfolio["company_id"] = company.id
            portfolio["products"] = CompanyProduct.get_list_of_products_from_company(
                company.id)
            portfolios.append(portfolio)
        return jsonify(portfolios)


@app.route('/PhoneRecharges', methods=['GET'])
def get_recharge():
    args = request.args
    if 'id' in args:
        recharge = PhoneRecharge.get_recharge_by_id(args['id'])
        if not recharge:
            return Response(json.dumps(recharge), status=204, mimetype='application/json')
        else: 
            return Response(json.dumps(recharge), status=200, mimetype='application/json')
    elif 'phone_number' in args:
        recharge = PhoneRecharge.get_recharge_by_phone_number(args['phone_number'])
        if not recharge:
            return Response(json.dumps(recharge), status=204, mimetype='application/json')
        else: 
            return Response(json.dumps(recharge), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({
            'error': 'Route requires filter like phone_number or id'}),
                        status=422, mimetype='application/json')


@app.route('/PhoneRecharges', methods=['POST'])
def do_phone_recharge():
    request_data = request.get_json()
    expected_keys = ['company_id', 'product_id', 'phone_number', 'value']
    if all([x in list(request_data.keys()) for x in expected_keys]):
        company_id = request_data['company_id']
        phone_number = request_data['phone_number']
        product_id = request_data['product_id']
        value = request_data['value']
        response = PhoneRecharge.do_recharge(
            company_id, product_id, phone_number, value)
        if 'error' in response:
            response = Response(json.dumps(response), status=422,
                                mimetype='application/json')
            return response
        else:
            create_location = '/PhoneRecharges?id={}'.format(response['id'])
            response = Response(json.dumps(response), status=201,
                                mimetype='application/json',
                                headers={'Location': create_location})
            return response

    else:
        # missing param
        invalid_request_msg = {
            "error": "Missing Parameter"
        }
        response = Response(json.dumps(invalid_request_msg),
                            status=422, mimetype="application/json")
        return response
# {
#    "company_id": "claro_11",
#    "product_id": "claro_10",
#    "phone_number": "5511999999999",
#    "value": 10.00
# }


app.run(host='0.0.0.0')
