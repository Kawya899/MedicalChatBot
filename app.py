from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import sqlite3

app = Flask(__name__)

# Configure Gemini API key (replace with your real key)
genai.configure(api_key="AIzaSyA6onp0ZGmHyb9Z32q3pQ-CL3Z6IJ6h7K0")

def get_db_connection():
    conn = sqlite3.connect('medical_chatbot.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_doctors_by_disease(disease):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT name, specialty, contact 
        FROM doctors 
        WHERE LOWER(disease_tag) LIKE ?
    """
    cur.execute(query, ('%' + disease.lower() + '%',))
    doctors = cur.fetchall()
    conn.close()
    return doctors

def get_disease_info(disease):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT description, food_suggestions 
        FROM disease_info 
        WHERE LOWER(disease_name) = ?
    """
    cur.execute(query, (disease.lower(),))
    data = cur.fetchone()
    conn.close()
    return data

def shorten_reply(text, max_length=600):
    if len(text) > max_length:
        return text[:max_length].rsplit('.', 1)[0] + "..."
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message'].strip()
    disease_keyword = user_input.lower()

    disease_info = get_disease_info(disease_keyword)
    doctors = get_doctors_by_disease(disease_keyword)

    disease_text = ""
    if disease_info:
        disease_text += f"Disease Description: {disease_info['description']}\n"
        disease_text += f"Food Suggestions: {disease_info['food_suggestions']}\n"

    if doctors:
        disease_text += "Specialist doctors:\n"
        for doc in doctors:
            disease_text += f"- {doc['name']} ({doc['specialty']}), Contact: {doc['contact']}\n"

    prompt = f"""You are a helpful medical chatbot. The user provided this input:
\"\"\"{user_input}\"\"\"

Here is some known info about the disease and doctors:
{disease_text}

Based on this info, suggest the best foods to manage the condition, explain why they are good (keep under 150 words), and respond clearly and simply.

Bot:"""

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        ai_reply = shorten_reply(response.text)

        ai_reply_html = "<p>" + ai_reply.replace('\n', '<br>') + "</p>"
        disease_html = (
            f"<p><strong>Disease Info:</strong> {disease_info['description']}<br>"
            f"<strong>Food Suggestions:</strong> {disease_info['food_suggestions']}</p>"
            if disease_info else ""
        )
        doctors_html = (
            "<br><br><strong>Here are some specialist doctors you may consider.</strong>"
            if doctors else ""
        )

        final_reply_html = ai_reply_html + disease_html + doctors_html

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO conversations (user_id, user_message, bot_response) VALUES (?, ?, ?)",
            (1, user_input, final_reply_html)
        )
        conn.commit()
        conn.close()

        return jsonify({'response': final_reply_html})

    except Exception as e:
        return jsonify({'response': f"<p><strong>Error occurred:</strong> {str(e)}</p>"})

# New route to fetch doctor details separately
@app.route('/doctors')
def doctors():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, specialty, contact FROM doctors")
    doctors = cur.fetchall()
    conn.close()

    doctors_list = [dict(doc) for doc in doctors]
    return jsonify({'doctors': doctors_list})

if __name__ == '__main__':
    app.run(debug=True)