# -*- coding=utf-8 -*-
from flask import Flask, render_template, redirect, request, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from sim.simr import runSim
import os

app = Flask(__name__,
static_folder = "./TomasuloPanel/dist/static",
template_folder = "./TomasuloPanel/dist")

UPLOAD_FOLDER='./upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['nel'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/upload', methods=['GET', 'POST', 'OPTION'])
def upload_file():
    # print(request.values['ars'][1])
    if request.method=='POST':
        print('em')
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            # flash('No selected file')
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            (a,b) = runSim(config={
                'ars': int(request.values['ars']),
                'mrs': int(request.values['mrs']),
                'lb': int(request.values['lb']),
                'add': int(request.values['add']),
                'mul': int(request.values['mul']),
                'ld': int(request.values['ld']),
                'reg': int(request.values['reg'])
            }, progFile='./upload/'+filename)
            return jsonify({'a':a,'b':b})
        # return redirect(url_for('uploaded_file',
        #                         filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post action="/api/upload" enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# @app.route('/run/<filename>')
# def uploaded_file(filename):
#     with open('./upload/'+filename) as f:
#         lines = f.readlines()
#         print(lines)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
        