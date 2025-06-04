-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER
);

INSERT INTO users (name, email, age) VALUES
('Kavya', 'kavya@example.com', 22),
('Nimal', 'nimal@example.com', 30);

-- CONVERSATIONS TABLE
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    user_message TEXT,
    bot_response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO conversations (user_id, user_message, bot_response) VALUES
(1, 'What food is good for diabetes?', 'Foods like whole grains, leafy greens, and fish are great for managing diabetes.'),
(2, 'I have high blood pressure', 'Bananas and oats can help lower blood pressure.');

-- DOCTORS TABLE
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    specialty TEXT,
    contact TEXT,
    disease_tag TEXT
);

INSERT INTO doctors (name, specialty, contact, disease_tag) VALUES
('Dr. John Smith', 'Cardiologist', 'john.smith@hospital.com, +123456789', 'hypertension'),
('Dr. Emma Lee', 'Internal Medicine', 'emma.lee@clinic.com, +987654321', 'hypertension'),
('Dr. Alice Brown', 'Endocrinologist', 'alice.brown@hospital.com, +111222333', 'diabetes'),
('Dr. Michael Green', 'Diabetologist', 'michael.green@clinic.com, +444555666', 'diabetes');

-- FEEDBACK TABLE
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER,
    rating INTEGER,
    comment TEXT,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

INSERT INTO feedback (conversation_id, rating, comment) VALUES
(1, 5, 'Very helpful!'),
(2, 4, 'Good suggestions.');

-- SYMPTOMS TABLE
CREATE TABLE IF NOT EXISTS symptoms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    related_disease TEXT
);

INSERT INTO symptoms (name, related_disease) VALUES
('frequent urination', 'diabetes'),
('chest pain', 'hypertension'),
('blurred vision', 'diabetes'),
('shortness of breath', 'hypertension');

-- LANGUAGE SUPPORT TABLE
CREATE TABLE IF NOT EXISTS language_support (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT,
    english TEXT,
    sinhala TEXT,
    tamil TEXT
);

INSERT INTO language_support (key, english, sinhala, tamil) VALUES
('greeting', 'Hello! How can I help you?', 'හෙලෝ! මම ඔබට උපකාර කළ හැක.', 'வணக்கம்! நான் உங்களுக்கு உதவ முடியும்.'),
('goodbye', 'Take care! Bye!', 'සතුටින් ඉන්න! ගිහින් එන්න!', 'கவனமாக இருங்கள்! விடைபெறுகிறேன்!');

-- APPOINTMENTS TABLE
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    doctor_id INTEGER,
    date DATE,
    time TIME,
    status TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

INSERT INTO appointments (user_id, doctor_id, date, time, status) VALUES
(1, 1, '2025-06-05', '10:00:00', 'confirmed'),
(2, 3, '2025-06-06', '14:00:00', 'pending');

-- DISEASE INFORMATION TABLE
CREATE TABLE IF NOT EXISTS disease_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    disease_name TEXT,
    description TEXT,
    food_suggestions TEXT
);

INSERT INTO disease_info (disease_name, description, food_suggestions) VALUES
('diabetes', 'A chronic condition that affects how your body turns food into energy.', 'Leafy greens, whole grains, low-sugar fruits'),
('hypertension', 'High blood pressure condition that can cause heart problems.', 'Bananas, spinach, oats, garlic');

-- CHAT SUMMARY TABLE
CREATE TABLE IF NOT EXISTS chat_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    total_chats INTEGER,
    last_active DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO chat_summary (user_id, total_chats, last_active) VALUES
(1, 5, '2025-06-03 12:34:00'),
(2, 3, '2025-06-02 15:20:00');
