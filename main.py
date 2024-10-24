from flask import Flask, jsonify, request, send_from_directory
import os
import time
import threading

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "Server is running!"

# Route for file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'fbxFile' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['fbxFile']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.fbx'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200
    else:
        return jsonify({"error": "File type not supported"}), 400

# Route to get the name of the most recent file
@app.route('/get-latest-file', methods=['GET'])
def get_latest_file():
    files = os.listdir(UPLOAD_FOLDER)
    fbx_files = [f for f in files if f.endswith('.fbx')]
    if fbx_files:
        latest_file = max(fbx_files, key=lambda f: os.path.getctime(os.path.join(UPLOAD_FOLDER, f)))
        return jsonify({"filename": latest_file}), 200
    else:
        return jsonify({"error": "No FBX files found"}), 404

# Route to access files from the uploads folder
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    response = send_from_directory(UPLOAD_FOLDER, filename)
    threading.Thread(target=delete_files_after_delay, args=(10,)).start()
    
    return response

# Function to delete files from the uploads folder after a delay
def delete_files_after_delay(delay):
    time.sleep(delay)
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                print(f"File {filename} removed.")
        except Exception as e:
            print(f"Error while trying to delete file {filename}: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
