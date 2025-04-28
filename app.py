import os
import logging
from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from flask_socketio import SocketIO, emit, join_room
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from googletrans import Translator
import easyocr
import speech_recognition as sr

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# set up logging
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

db = SQLAlchemy(app)
socketio = SocketIO(app)
translator = Translator()

# Initialize OCR reader
reader = easyocr.Reader(['en', 'ja'])

# Model for User
class User(db.Model):
    id       = db.Column(db.Integer,   primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    language = db.Column(db.String(20), nullable=False)  # English or Japanese

# Utility: file‐extension check
def allowed_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    )

# Routes
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        language = request.form['language']
        if User.query.filter_by(username=username).first():
            return 'Username already exists'
        user = User(username=username, password=password, language=language)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        language = request.form['language']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            session['language'] = language
            return redirect(url_for('chat'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username=session['username'], language=session['language'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('language', None)
    return redirect(url_for('login'))

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text        = data['text']
    src_lang    = data['source_lang']  # e.g. "English" or "Japanese"
    # map to GoogleTrans codes:
    if src_lang.lower() == 'en':
        src_code  = 'en'
        dest_code = 'ja'
    else:
        src_code  = 'ja'
        dest_code = 'en'

    print(src_code, dest_code, src_lang)
    # do the translation
    try:
        translated = translator.translate(text, src=src_code, dest=dest_code).text
    except Exception as e:
        app.logger.error(f"Translation error ({src_code}->{dest_code}): {e}")
        translated = text

    return jsonify({'translated': translated})


@app.route('/voice-translate', methods=['POST'])
def voice_translate():
    text = request.form['voice_text']
    translated_text = translator.translate(text, src='en', dest='ja').text
    return render_template('index.html', voice_translation=translated_text)

# Socket.IO events

@socketio.on('join')
def handle_join(data):
    username = data.get('username')
    app.logger.info(f"Join event received for user: {username}")
    join_room(username)
    app.logger.info(f"User {username} joined room {username}")

@socketio.on('send_message')
def handle_send_message_event(data):
    username = data.get('username')
    message = data.get('message')
    app.logger.info(f"Received message from {username}: {message}")

    sender = User.query.filter_by(username=username).first()
    sender_lang = sender.language if sender else 'English'
    all_users = User.query.all()

    for user in all_users:
        # Echo original back to sender
        if user.username == username:
            emit('receive_message', {'username': username, 'message': message}, room=username)
        else:
            # Translate only if languages differ
            if sender_lang != user.language:
                try:
                    if sender_lang.lower() == 'english':
                        translated = translator.translate(message, src='en', dest='ja').text
                    else:
                        translated = translator.translate(message, src='ja', dest='en').text
                except Exception as e:
                    app.logger.error(f"Translation failed for '{message}' from {username}: {e}")
                    translated = message
            else:
                translated = message

            emit('receive_message', {'username': username, 'message': translated}, room=user.username)


# 🆕 Upload Handwritten Image
@app.route('/upload-handwritten', methods=['POST'])
def upload_handwritten():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Process the uploaded image
    result = reader.readtext(filepath)
    grouped_lines = group_text_by_lines_dynamic(result)

    recognized_text = ""
    for line in grouped_lines:
        line_text = " ".join([text for _, text in line['items']])
        recognized_text += line_text + "\n"

    return jsonify({'recognized_text': recognized_text.strip()})

# 🆕 Group lines properly
def group_text_by_lines_dynamic(results, height_multiplier=0.6):
    lines = []
    for detection in results:
        box, text, conf = detection
        (x1, y1) = box[0]
        (x2, y2) = box[2]
        y_center = (y1 + y2) / 2
        height = abs(y1 - y2)

        matched = False
        for line in lines:
            avg_y = line['avg_y']
            avg_height = line['avg_height']
            if abs(avg_y - y_center) < (avg_height * height_multiplier):
                line['items'].append((x1, text))
                line['y_vals'].append(y_center)
                line['heights'].append(height)
                line['avg_y'] = sum(line['y_vals']) / len(line['y_vals'])
                line['avg_height'] = sum(line['heights']) / len(line['heights'])
                matched = True
                break

        if not matched:
            lines.append({
                'avg_y': y_center,
                'avg_height': height,
                'y_vals': [y_center],
                'heights': [height],
                'items': [(x1, text)]
            })

    for line in lines:
        line['items'].sort(key=lambda x: x[0])
    lines.sort(key=lambda line: line['avg_y'])

    return lines



# Run app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
