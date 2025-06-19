# 🌐 JapTran — English ↔ Japanese Translator Web App

**JapTran** is a real-time bilingual web application that allows users to translate between **English and Japanese** using **text**, **speech**, and **handwritten images**. It also supports multilingual chat, where messages are auto-translated according to the user's selected language preference.

---

## 🚀 Features

### 💬 Chat with Language Translation
- Real-time messaging with auto-translation between users.
- Socket.IO-based chat system.
- User-specific language preferences (English/Japanese).

### 📝 Text to Text Translation
- Enter any text and instantly get the translation.
- Uses Google Translate for accurate results.

### 🎤 Speech to Text Translation
- Record audio in English or Japanese.
- Transcribes and translates spoken input.

### ✍️ Handwritten Text Recognition
- Upload images of handwritten text.
- Extracts text using EasyOCR and translates it.

---

## 🛠️ Tech Stack

| Component         | Technology             |
|------------------|------------------------|
| Backend          | Python (Flask)         |
| Real-Time Chat   | Flask-SocketIO         |
| Frontend         | HTML, CSS, JavaScript  |
| OCR              | EasyOCR                |
| Translation API  | Googletrans (Google Translate) |
| Speech Recognition | `speech_recognition` library |
| Database         | SQLite (via SQLAlchemy) |

---

## 🧠 Project Workflow

A complete workflow diagram is included in the repository as `JapTran_Workflow.png`. It illustrates the interaction between users, frontend, backend, and various input translation pipelines.

---

## 🔧 Installation & Running Locally

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/JapTran.git
   cd JapTran

2. **(Optional) Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install required packages:**

   ```bash
   pip install -r requirements.txt

4. **Run the app:**

   ```bash
   python app.py

5. **Open your browser and go to:**

   ```bash
   http://localhost:5000/


You can copy this directly into your `README.md` file under the **Installation & Running Locally** section. Let me know if you'd like to add instructions for deploying it online as well!

## 📁 Project Structure

```text
JapTran/
├── app.py                  # Main Flask backend
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── chat.html
│   ├── login.html
│   └── register.html
├── static/
│   └── style.css           # CSS styles
├── uploads/                # Uploaded handwritten images
├── JapTran_Workflow.png    # Project flowchart diagram (optional)
└── README.md


## 👥 User Guide

1. **Register/Login**  
   - Create an account by entering your username, password, and selecting a preferred language (English or Japanese).

2. **Chat in Real-Time**  
   - Send messages to other users.
   - Messages are automatically translated to the recipient's preferred language.

3. **Text Translation**  
   - Use the text input area to type content and translate between English and Japanese.

4. **Speech Translation**  
   - Click "Start Speaking" to speak in English or Japanese.
   - The app will transcribe and translate your spoken sentence.

5. **Handwriting Recognition**  
   - Upload an image of handwritten text (English or Japanese).
   - The app extracts the text and provides a translated version.

## ✅ To-Do / Future Improvements

- 🌐 Add support for more languages.
- ☁️ Deploy to a cloud platform (e.g., Render, Railway, Vercel).
- 💬 Store chat history and display past messages.
- 🔐 Improve authentication (e.g., email verification, password reset).
- 📱 Make the UI fully responsive for mobile devices.
- 🧠 Add fallback OCR using Tesseract for better recognition accuracy.
- 🎨 Add UI theme switching (light/dark mode).

## 🤝 Acknowledgements

- [Flask](https://flask.palletsprojects.com/) — Backend web framework
- [Socket.IO](https://socket.io/) — Real-time messaging
- [Google Translate](https://translate.google.com/) — Language translation service
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) — Optical character recognition
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) — Audio input processing
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) — Browser-based voice recognition

