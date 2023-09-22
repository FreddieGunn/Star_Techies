import sys
sys.path.insert(0, '/home/ec2-user/environment/Star_Techies')

from flask import Flask, jsonify
from resident.resident_home import resident_api
from staff.staff_view_endpoints import staff_api
import boto3


app = Flask(__name__)

app.register_blueprint(resident_api)
app.register_blueprint(staff_api)

@app.route("/")
def hello():
    return "Hello World!"
    


if __name__ == "__main__":
    app.run(debug=True, port=8080)