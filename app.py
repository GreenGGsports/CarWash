from flask import Flask
from src.controllers.reservation_controller import reservation_ctrl
from src.views.reservation_view import reservation_view

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/car_wash.db'  # Replace with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Register blueprints
app.register_blueprint(reservation_ctrl, url_prefix='/reservation/add')
app.register_blueprint(reservation_view, url_prefix='/reservation')

if __name__ == "__main__":
    app.run(debug=True)
