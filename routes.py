from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from app.encryption import AESCipher

main = Blueprint("main", __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'jpg'}

# Check if the file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route("/")  # Home route for the app
def home():
    return "Welcome to the Data Encryption Service!"

@main.route("/encrypt/aes", methods=["POST"])
def encrypt_aes():
    data = request.json
    key = data.get("key", "defaultkey123456")
    message = data.get("message", "")
    cipher = AESCipher(key)
    encrypted_text = cipher.encrypt(message)
    return jsonify({"encrypted": encrypted_text})

@main.route("/decrypt/aes", methods=["POST"])
def decrypt_aes():
    data = request.json
    key = data.get("key", "defaultkey123456")
    encrypted_text = data.get("encrypted", "")
    cipher = AESCipher(key)
    decrypted_text = cipher.decrypt(encrypted_text)
    return jsonify({"decrypted": decrypted_text})


@main.route("/encrypt/file", methods=["POST"])
def encrypt_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            # Read the file in binary mode
            with open(file_path, 'rb') as f:
                content = f.read()

            key = request.form.get('key', 'defaultkey123456')
            cipher = AESCipher(key)
            encrypted_content = cipher.encrypt(content)

            encrypted_filename = f"encrypted_{filename}"
            encrypted_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], encrypted_filename)
            with open(encrypted_file_path, 'wb') as f:
                f.write(encrypted_content)

            return jsonify({"encrypted_file": encrypted_filename})

        except Exception as e:
            print("Encryption error:", str(e))  # Debugging log
            return jsonify({"error": "Encryption failed"}), 500

    return jsonify({"error": "File format not allowed"}), 400


@main.route("/decrypt/file", methods=["POST"])
def decrypt_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            # Read the file in binary mode
            with open(file_path, 'rb') as f:
                content = f.read()

            key = request.form.get('key', 'defaultkey123456')
            cipher = AESCipher(key)
            decrypted_content = cipher.decrypt(content)

            decrypted_filename = f"decrypted_{filename}"
            decrypted_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], decrypted_filename)
            with open(decrypted_file_path, 'wb') as f:
                f.write(decrypted_content)

            return jsonify({"decrypted_file": decrypted_filename})

        except Exception as e:
            print("Decryption error:", str(e))  # Debugging log
            return jsonify({"error": "Decryption failed"}), 500

    return jsonify({"error": "File format not allowed"}), 400
