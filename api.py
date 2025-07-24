from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
from blockchain import Blockchain

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests (for React or other frontend)

# Initialize blockchain
civ_chain = Blockchain()

# Create folders for media if they don't exist
os.makedirs("photos", exist_ok=True)
os.makedirs("qrcodes", exist_ok=True)

@app.route("/")
def index():
    return "✅ CivChain API is running."

@app.route("/api/add", methods=["POST"])
def add_survivor():
    try:
        data = request.json

        name = data.get("name", "Unknown")
        location = data.get("location", "Unknown")
        status = data.get("status", "unknown")
        notes = data.get("notes", "")
        timestamp = time.ctime()

        survivor_data = {
            "name": name,
            "location": location,
            "status": status,
            "notes": notes,
            "recorded_at": timestamp
        }

        civ_chain.add_block(survivor_data)
        civ_chain.save_to_file()

        return jsonify({
            "message": "Survivor data added to CivChain",
            "block_index": len(civ_chain.chain) - 1,
            "data": survivor_data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/chain", methods=["GET"])
def get_chain():
    chain_data = []

    for block in civ_chain.chain:
        block_info = {
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        }
        chain_data.append(block_info)

    return jsonify({"chain": chain_data, "length": len(chain_data)}), 200

if __name__ == "__main__":
    app.run(debug=True)
