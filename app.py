from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests, json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///information.db'
db = SQLAlchemy(app)


class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    segment = db.Column(db.String(255), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String(255), nullable=False)


URL_AUTH = 'https://api.getresponse.com/v3/accounts'
URL_TAGS = 'https://api.getresponse.com/v3/tags'
URL_SEGMENTS = 'https://api.getresponse.com/v3/search-contacts'
KEY = 'pgeu0bwiitvuijtmtwo369npkgr5m813'

headers_auth = {'X-Auth-Token': 'api-key ' + KEY,
                'X-Domain': 'test.getresponseservices.ru',
                'Content-Type': 'application/json'
                }


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        segment = request.form['segment']
        count = request.form['count']
        tag = request.form['tag']

        inform = Information(segment=segment, count=count, tag=tag)

        try:
            db.session.add(inform)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error'
    else:
        auth = requests.get(URL_AUTH, headers=headers_auth)

        if auth.status_code == 200:
            tags = requests.get(URL_TAGS, headers=headers_auth)
            tags = json.loads(tags.text)

            segments = requests.get(URL_SEGMENTS, headers=headers_auth)
            segments = json.loads(segments.text)

    return render_template('main.html', tags=tags, segments=segments)


def cron():
    cron_info = Information.query.all()
    for inf in cron_info:
        segment_contacts = requests.get(URL_SEGMENTS + '/' + inf.segment + '/contacts', headers=headers_auth)
        if segment_contacts is not None and segment_contacts.status_code == 200:
            segment_contacts = json.loads(segment_contacts.text)
            i = 0
            while i < inf.count:
                requests.post('https://api.getresponse.com/v3/contacts/' + segment_contacts[i]['contactId'],
                              headers=headers_auth, data=json.dumps({"tags": [inf.tag]}))
                i += 1


if __name__ == '__main__':
    app.run()
