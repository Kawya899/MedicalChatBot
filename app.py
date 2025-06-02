from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Set your Gemini API key
genai.configure(api_key="AIzaSyA6onp0ZGmHyb9Z32q3pQ-CL3Z6IJ6h7K0")  # Replace with your real API key

# Dictionary of disease keywords to doctors info
doctors_db = {
    "hypertension": [
        {"name": "Dr. John Smith", "specialty": "Cardiologist", "contact": "john.smith@hospital.com, +123456789"},
        {"name": "Dr. Emma Lee", "specialty": "Internal Medicine", "contact": "emma.lee@clinic.com, +987654321"}
    ],
    "diabetes": [
        {"name": "Dr. Alice Brown", "specialty": "Endocrinologist", "contact": "alice.brown@hospital.com, +111222333"},
        {"name": "Dr. Michael Green", "specialty": "Diabetologist", "contact": "michael.green@clinic.com, +444555666"}
    ],
    # Add more diseases and doctor lists here (up to 30)
    # ...
}

def find_doctors(disease):
    disease = disease.lower()
    for key in doctors_db:
        if key in disease:
            return doctors_db[key]
    return None

def format_doctors_info(doctors_list):
    if not doctors_list:
        return ""
    info = "\n\nYou may also consider consulting these specialist doctors:\n"
    for doc in doctors_list:
        info += f"- {doc['name']} ({doc['specialty']}), Contact: {doc['contact']}\n"
    return info

def shorten_reply(text, max_length=600):
    if len(text) > max_length:
        return text[:max_length].rsplit('.', 1)[0] + "..."
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']

    prompt = f"""You are a medical chatbot. A user will type in a disease or symptom.
You will:
- Suggest the best foods to manage it.
- Explain simply and briefly why each food is beneficial (keep the answer under 150 words).
- Answer follow-up questions clearly and simply.

User: {user_input}
Bot:"""

    if "hypertension" in user_input.lower():
        reply = "Foods like bananas, spinach, and oats are helpful in managing hypertension. They are rich in potassium and fiber, which help lower blood pressure."
        reply += format_doctors_info(doctors_db["hypertension"])

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # or 'gemini-1.5-pro'
        response = model.generate_content(prompt)
        reply = shorten_reply(response.text)

        # Check for matching doctors
        doctors_list = find_doctors(user_input)
        if doctors_list:
            reply += format_doctors_info(doctors_list)

        return jsonify({'response': reply})

    except Exception as e:
        return jsonify({'response': 'Error: ' + str(e)})

if __name__ == '__main__':
    app.run(debug=True)