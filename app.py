from flask import Flask, request, jsonify
from flask_cors import CORS
from rdkit import Chem
from rdkit.Chem import Draw
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route('/draw_molecule', methods=['GET'])
def draw_molecule():
    smiles = request.args.get('smiles', '').strip()
    if not smiles:
        return jsonify({"error": "No SMILES provided"}), 400

    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return jsonify({"error": "Invalid SMILES"}), 400

    # Generate 2D image, e.g. 300x300
    img = Draw.MolToImage(mol, size=(300, 300))

    # Convert to base64
    buf = BytesIO()
    img.save(buf, format='PNG')
    base64_str = base64.b64encode(buf.getvalue()).decode("utf-8")

    return jsonify({
        "image": "data:image/png;base64," + base64_str
    })

if __name__ == '__main__':
    # Listen on all IPs, port 5000
    app.run(host='0.0.0.0', port=5000)
