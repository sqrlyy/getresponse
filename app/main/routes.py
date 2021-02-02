from app.main import bp
from app import db
from app.models import Segment
from flask import render_template, request, redirect
import requests
import json
from flask import current_app


@bp.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        segment = request.form['segment']
        count = request.form['count']
        tag = request.form['tag']

        inform = Segment(segment=segment, count=count, tag=tag)

        # try:
        db.session.add(inform)
        db.session.commit()
        return redirect('/')
        # except:
        #     return 'Error'
    else:
        auth = requests.get(current_app.config['URL_AUTH'], headers=current_app.config['HEADERS_AUTH'])

        if auth.status_code == 200:
            tags = requests.get(current_app.config['URL_TAGS'], headers=current_app.config['HEADERS_AUTH'])
            tags = json.loads(tags.text)

            segments = requests.get(current_app.config['URL_SEGMENTS'], headers=current_app.config['HEADERS_AUTH'])
            segments = json.loads(segments.text)

    return render_template('main.html', tags=tags, segments=segments)
