from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from settings import app
import datetime
from settings import logger
from passlib.hash import pbkdf2_sha256

db = SQLAlchemy(app)


class Company(db.Model):
    __tablename__ = "Company"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)


class CompanyProduct(db.Model):
    __tablename__ = "CompanyProduct"
    id = db.Column(db.String, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    company_id = db.Column(db.String, ForeignKey('Company.id'))

    def json(self):
        return {"id": self.id, "value": self.value}

    def get_list_of_products_from_company(_company_id):
        return [product.json() for product in
                CompanyProduct.query.filter_by(company_id=_company_id)]


class PhoneRecharge(db.Model):
    __tablename__ = "PhoneRecharge"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    company_id = db.Column(db.String, ForeignKey('Company.id'))
    product_id = db.Column(db.String, ForeignKey('CompanyProduct.id'))
    phone_number = db.Column(db.String, nullable=False)
    value = db.Column(db.Float, nullable=False)

    def get_datetime_string(self):
        return self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    def json(self):
        return {
            "id": self.id,
            "created_at": self.get_datetime_string(),
            "company_id": self.company_id,
            "product_id": self.product_id,
            "phone_number": self.phone_number,
            "value": self.value
        }

    def get_recharge_by_id(_id):
        recharge = PhoneRecharge.query.filter_by(id=_id)
        if recharge.count() < 1:
            logger.info('Recharge with recharge id {} not found'.format(_id))
            return None
        else:
            recharge = recharge.first()
            return recharge.json()

    def get_recharge_by_phone_number(phone_number):
        recharge = PhoneRecharge.query.filter_by(phone_number=phone_number)
        if recharge.count() < 1:
            logger.info('Recharges with phone_number {} not found'.format(
                phone_number))
            return None
        else:
            recharges = recharge
            return [recharge.json() for recharge in recharges]

    def do_recharge(_company_id, _product_id, phone, _value):
        status_message = "Attempt to Recharge phone: {},"\
            " with options: company:{}, pid: {}, value: {},"\
            " status: {}"

        status_message = status_message.format(
            phone, _company_id, _product_id, _value, '{}')

        company_product = CompanyProduct.query.filter_by(
            id=_product_id, company_id=_company_id, value=_value)

        if not company_product or company_product.count() < 1:
            logger.info(status_message.format('Failed, not recharge option'))
            return {'error': 'Not a valid Recharge option'}

        if phone.isdigit() and 13 >= len(phone) >= 12:
            new_recharge = PhoneRecharge(
                company_id=_company_id, product_id=_product_id,
                phone_number=phone, value=_value)
            db.session.add(new_recharge)
            db.session.commit()
            logger.info(status_message.format('success'))
            return {'success': 'Recharge made', 'id': new_recharge.id}
        else:
            logger.info(
                status_message.format('Failed, not acceptable phone format'))
            return {'error': 'Not acceptable phone format'}


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return str({
            'username': self.username,
            'password': self.password
        })

    def username_password_match(_username, _password):
        user = User.query.filter_by(username=_username).first()
        if user is None:
            return False
        if not pbkdf2_sha256.verify(_password, user.password):
            return False
        return True

    def get_all_users():
        return User.query.all()

    def create_user(_username, _password):
        _password = pbkdf2_sha256.hash(_password)
        new_user = User(username=_username, password=_password)
        db.session.add(new_user)
        db.session.commit()
