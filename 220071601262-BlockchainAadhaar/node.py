from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            "index": block.index,
            "timestamp": str(block.timestamp),
            "name": block.name,
            "aadhaar_no": block.aadhaar_no,
            "gender": block.gender,
            "dob": block.dob,
            "address": block.address,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })
    return jsonify({"length": len(blockchain.chain), "chain": chain_data}), 200

@app.route('/add_block', methods=['POST'])
def add_block():
    values = request.get_json()
    required = ['name','aadhaar_no','gender','dob','address']
    if not all(k in values for k in required):
        return 'Missing values', 400
    if blockchain.is_aadhaar_registered(values['aadhaar_no']):
        return 'Aadhaar exists', 400
    block = blockchain.add_block(
        values['name'], values['aadhaar_no'],
        values['gender'], values['dob'], values['address']
    )
    return jsonify({
        "message": "Block added",
        "index": block.index,
        "hash": block.hash
    }), 201

if __name__ == "__main__":
    app.run(port=5000)  # Change port for other nodes
