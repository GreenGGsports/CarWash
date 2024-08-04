from setup import create_app
from flask_cors import CORS

if __name__ == "__main__":
    app = create_app('development')
    CORS(app)
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
    
