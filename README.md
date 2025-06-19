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
