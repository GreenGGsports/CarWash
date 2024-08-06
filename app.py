from setup import create_app
from flask_cors import CORS

#app = create_app('deployment')
app = create_app('development')
CORS(app)
#app.run(debug=True)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    
