from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


# Example endpoint
@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello, world!"})


# Example API checker endpoint
@app.route("/check-api", methods=["GET"])
def check_api():
    # Example: Check our own /hello endpoint
    try:
        response = requests.get("http://127.0.0.1:5000/hello", timeout=5)
        if response.status_code == 200:
            return jsonify(
                {
                    "status": "success",
                    "checked_endpoint": "/hello",
                    "response": response.json(),
                }
            )
        else:
            return jsonify(
                {
                    "status": "failure",
                    "checked_endpoint": "/hello",
                    "status_code": response.status_code,
                }
            )
    except requests.RequestException as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
