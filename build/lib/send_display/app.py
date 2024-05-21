from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/v1/customers', methods=['PUT'])
def update_customer():
    data = request.get_json()
    response = custom_function(data)
    return jsonify(response), 200

def custom_function(data):
    if "email" in data and data["email"] == "john.doe@example.com":
        return {
            "message": "Customer updated successfully",
            "customer": data
        }
    else:
        return {
            "message": "Customer update failed",
            "reason": "Invalid email address"
        }

if __name__ == '__main__':
    app.run(debug=True, port=5000)