from flask import Flask 
from controllers import (
    reservation_controller
)

app = Flask(__name__)

app.register_blueprint(reservation_controller)

if __name__ == '__main__':
    app.run(debug=True)