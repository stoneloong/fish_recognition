# -*- coding: utf-8 -*-
import datetime
import logging as rel_log
import os
import shutil
from datetime import timedelta
from paddlex import deploy
from flask import *

import core.main

UPLOAD_FOLDER = r'./uploads'

ALLOWED_EXTENSIONS = set(['png'])
app = Flask(__name__)
app.secret_key = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

werkzeug_logger = rel_log.getLogger('werkzeug')
werkzeug_logger.setLevel(rel_log.ERROR)


# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='./index.html'))

#update file
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)        
        shutil.copy(src_path, './tmp/image')
        image_path = os.path.join('./tmp/image', file.filename)
        print(src_path, image_path)
        print(file.filename)
        yucejieguo = str(core.main.prediction(image_path))
        print(yucejieguo)
        image_data = core.main.pre_process(image_path)
        core.main.prediction_seg(image_data)
        fn = image_data[1]+'.png'
        core.main.last_process(fn)
        return jsonify({'status': 1,
                        'image_url': 'http://127.0.0.1:5003/tmp/image/'+fn,
                        'draw_url': 'http://127.0.0.1:5003/tmp/draw/'+fn,
                        'yucejieguo': yucejieguo
                        })

    return jsonify({'status': 0})


# show photo
@app.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    if request.method == 'GET':
        if not file is None:
            image_data = open(f'tmp/{file}',"rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response

if __name__ == '__main__':
    files = ['uploads', 'tmp/draw','tmp/image', 'tmp/mask', 'tmp/uploads']
    for ff in files:
        if not os.path.exists(ff):
            os.makedirs(ff)
    app.run(host='127.0.0.1', port=5003, debug=True)
