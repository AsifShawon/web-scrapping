from flask import Flask, request, jsonify
from touristSpots import TouristSpots
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_tourist_spots', methods=['GET'])
def get_tourist_spot():
    print('Request received')
    city = request.args.get('city')
    print('City:', city)
    if not city:
        return jsonify({"error": "City parameter is required."}), 400

    tourist_spots = TouristSpots(city).get_tourist_spots()
    return jsonify({"tourist_spots": tourist_spots})


if __name__ == "__main__":
    app.run(debug=True)