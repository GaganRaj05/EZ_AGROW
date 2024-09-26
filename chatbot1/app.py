from flask import Flask, render_template, request, jsonify
import json
import os
app = Flask(__name__)
def load_json(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"The '{filename}' file was not found.")
    try:
        with open(filename) as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding the '{filename}' file.")

# Load schemes data
try:
    schemes_data = load_json('schemes.json')
except (FileNotFoundError, ValueError) as e:
    print(f"Error loading schemes data: {e}")
    schemes_data = {'schemes': []}

# Predefined keyword-based responses
predefined_responses = [
    {
        "keywords": ["hello", "hi", "greetings"],
        "response": "Hello! How can I assist you today?"
    },
    {
        "keywords": ["bye", "goodbye", "see you"],
        "response": "Goodbye! Have a great day!"
    },
    {
        "keywords": ["help", "support", "issue"],
        "response": "I'm here to help! What do you need assistance with?"
    },
    {
        "keywords": ["thanks", "thank you"],
        "response": "You're welcome! If you have more questions, feel free to ask."
    }
]

# Function to search for a scheme by its name with case-insensitive and partial matching
def get_scheme_info(scheme_name):
    scheme_name = scheme_name.lower()
    matches = []

    # Search in schemes.json
    for scheme in schemes_data.get('schemes', []):
        if scheme_name in scheme.get('name', '').lower():
            matches.append({
                "name": scheme.get('name'),
                "description": scheme.get('description'),
                "eligibility": scheme.get('eligibility'),
                "subsidy": scheme.get('subsidy'),
                "link": scheme.get('link')
            })

    if matches:
        return {"matches": matches}

    # Provide alternative suggestions
    error_message = (
        "No matching scheme found. Please check the name or try again later."
    )
    
    suggestions = [
        {"text": "Please visit the official site for more details", "url": "https://official-website.com/"}
    ]
    
    return {
        "error": error_message,
        "suggestions": suggestions
    }

def get_predefined_response(user_text):
    user_text = user_text.lower()

    for response_entry in predefined_responses:
        for keyword in response_entry["keywords"]:
            if keyword in user_text:
                return response_entry["response"]

    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def get_bot_response():
    userText = request.form.get('msg', '').strip()
    if not userText:
        return jsonify({"response": "No input provided. Please enter a scheme name."})

    predefined_response = get_predefined_response(userText)
    if predefined_response:
        return jsonify({"response": predefined_response})

    response = get_scheme_info(userText)

    if 'error' in response:
        suggestions_html = ""
        if response['suggestions']:
            suggestions_html = "<div class='suggestions'>Did you mean: " + ", ".join(
                [f"<a href='{s['url']}' target='_blank'>{s['text']}</a>" for s in response['suggestions']]
            ) + "</div>"
        return jsonify({"response": f"{response['error']} {suggestions_html}"})

    schemes_info = "<br>".join([f"Scheme: {match['name']}<br>"
                                f"Description: {match['description']}<br>"
                                f"Eligibility: {match['eligibility']}<br>"
                                f"Subsidy: {match['subsidy']}<br>"
                                f"Link: <a href='{match['link']}' target='_blank'>Click Here</a>"

                                for match in response['matches']])
    return jsonify({"response": schemes_info})

if __name__ == '__main__':
    app.run(debug=True)
