from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Healthletic Lifestyle Flask API"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/api/users")
def users():
    return jsonify([
        {
            "id": 1,
            "name": "John"
        },
        {
            "id": 2,
            "name": "Alice"
        }
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)