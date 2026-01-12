from flask import Flask, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'received_photos'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "未上传文件"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"status": "error", "message": "未选择文件"}), 400
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        print(f"收到照片：{file.filename}")
        return jsonify({"status": "success", "message": "上传成功"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)