import os
from flask import Flask, request, jsonify
from schedule import next_bus

app = Flask(__name__)

@app.route("/")
def index():
    return "歡迎使用聯大校車查詢平台"

@app.route("/next_bus")
def get_next_bus():
    destination = request.args.get("destination")
    if not destination:
        return jsonify({"error": "請提供 destination 參數"}), 400

    result = next_bus(destination)
    return jsonify({"result": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)