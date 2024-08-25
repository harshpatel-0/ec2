from flask import *
import os
from datetime import datetime

app = Flask(__name__, template_folder="templates")
upload_folder = '/hw03/images'  # Put images into directory
# EC2 Directory: /home/ec2-user/hw03/images

@app.route('/') # Define the route for the main page
def main():
    return render_template("index.html")

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file")
        
        for f in uploaded_files:
            if f.filename != '':  # Check if there is a file
                filepath = os.path.join(upload_folder, f.filename)
                f.save(filepath)

        return redirect(url_for('images')) # Redriect to the images route

@app.route('/images') # Displays uploaded images
def images():
    files = []
    for filename in os.listdir(upload_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            filepath = os.path.join(upload_folder, filename)
            size = os.path.getsize(filepath)
            mod_time = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
            files.append((filename, size, mod_time))
    return render_template('table.html', files=files)

@app.route('/images/<filename>') 
def uploaded_file(filename):
    filepath = os.path.join("images", filename) 
    return send_from_directory("images", filename) 


if __name__ == '__main__': # Run app!
    app.run(debug=True, host='0.0.0.0')