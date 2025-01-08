from setup import create_app
from flask_cors import CORS

#app = create_app('deployment')
app = create_app('deployment')
#CORS(app)
#app.run(debug=True)
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="127.0.0.1", port=8000)
    
