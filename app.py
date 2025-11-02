from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import uuid, os
from models import db, Order, Product, init_db

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "orders.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    init_db()
    if Product.query.count() == 0:
        products = [
            Product(id="p1", name="Basic Shirt", price=12.99),
            Product(id="p2", name="Jeans", price=24.50),
            Product(id="p3", name="Sneakers", price=39.99)
        ]
        db.session.add_all(products)
        db.session.commit()

@app.route("/")
def index():
    return render_template("index.html", products=Product.query.all())

@app.route("/product/<product_id>")
def product(product_id):
    prod = Product.query.filter_by(id=product_id).first()
    if not prod:
        return "Product not found", 404
    return render_template("product.html", product=prod)

@app.route("/order", methods=["POST"])
def create_order():
    data = request.form or request.get_json() or {}
    name = data.get("name") or "Anonymous"
    phone = data.get("phone") or ""
    product_id = data.get("product_id")
    qty = int(data.get("qty") or 1)
    prod = Product.query.filter_by(id=product_id).first()
    if not prod:
        return jsonify({"error": "Invalid product"}), 400
    order = Order(
        id=str(uuid.uuid4())[:8],
        product=prod.name,
        product_id=prod.id,
        qty=qty,
        price=prod.price * qty,
        customer=name,
        phone=phone,
        status="pending"
    )
    db.session.add(order)
    db.session.commit()
    if request.form:
        return redirect(url_for("orders_page"))
    return jsonify(order.to_dict()), 201

@app.route("/orders")
def orders_page():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("orders.html", orders=orders)

@app.route("/api/orders")
def api_orders():
    return jsonify([o.to_dict() for o in Order.query.all()])

@app.route("/api/orders/<order_id>/status", methods=["POST"])
def update_status(order_id):
    new_status = (request.json or {}).get("status") or request.form.get("status")
    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return jsonify({"error":"not found"}), 404
    order.status = new_status
    db.session.commit()
    return jsonify(order.to_dict())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
