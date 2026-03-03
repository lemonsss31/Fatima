from flask import Flask, jsonify, render_template

app = Flask(__name__)

STATUS_FILE = "status.txt"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/detect")
def detect():
    try:
        with open(STATUS_FILE, "r") as f:
            status = f.read().strip()

        return jsonify({"discoloration": status == "true"})
    except:
        return jsonify({"discoloration": False})

if __name__ == "__main__":
    app.run(debug=True)