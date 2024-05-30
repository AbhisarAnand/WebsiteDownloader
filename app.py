from flask import Flask, request, send_file, render_template, redirect, url_for, after_this_request
import subprocess
import os
import zipfile
import shutil

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
DOWNLOAD_DIR = 'website_download'
ZIP_FILE_NAME = 'downloaded_website.zip'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if url:
            download_folder = os.path.join(DOWNLOAD_FOLDER, DOWNLOAD_DIR)
            if os.path.exists(download_folder):
                shutil.rmtree(download_folder)
            os.makedirs(download_folder)

            # Run wget to download the website
            subprocess.run(['wget', '-P', download_folder, '-r', '-np', '-k', '-E', url])

            # Zip the downloaded content
            zip_path = os.path.join(DOWNLOAD_FOLDER, ZIP_FILE_NAME)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for root, dirs, files in os.walk(download_folder):
                    for file in files:
                        zipf.write(os.path.join(root, file),
                                   os.path.relpath(os.path.join(root, file),
                                                   os.path.join(download_folder, '..')))

            # Clean up the downloaded folder
            shutil.rmtree(download_folder)

            return redirect(url_for('download_file', file_name=ZIP_FILE_NAME))

    return render_template('index.html')

@app.route('/downloads/<file_name>')
def download_file(file_name):
    file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
    
    @after_this_request
    def remove_file(response):
        try:
            os.remove(file_path)
        except Exception as e:
            app.logger.error(f'Error removing file {file_path}: {e}')
        return response

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False)
