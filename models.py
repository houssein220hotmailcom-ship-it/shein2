from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float)

class Order(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    product = db.Column(db.String(200))
    product_id = db.Column(db.String(50))
    qty = db.Column(db.Integer)
    price = db.Column(db.Float)
    customer = db.Column(db.String(200))
    phone = db.Column(db.String(100))
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "product": self.product,
            "product_id": self.product_id,
            "qty": self.qty,
            "price": self.price,
            "customer": self.customer,
            "phone": self.phone,
            "status": self.status,
            "created_at": self.created_at.isoformat() + "Z"
        }

def init_db():
    db.create_all()
