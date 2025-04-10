from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def serve_pitch():
    return send_file('startup_pitch.html')

@app.route('/pricing')
def serve_pricing():
    return send_file('pricing_tiers.html')

@app.route('/chatbot')
def serve_chatbot():
    return send_file('chatbot_tiers.html')

@app.route('/physical')
def serve_physical():
    return send_file('physical_features.html')  # We'll create this in the future

@app.route('/academic')
def serve_academic():
    return send_file('academic_features.html')  # We'll create this in the future

if __name__ == '__main__':
    print("Startup pitch website running at: http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True) 