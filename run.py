from app import create_app
import requests
from flask import current_app
from app.models import Segment
import json
from flask_cli import FlaskCLI

app = create_app()
FlaskCLI(app)


@app.cli.command()
def cron():
    cron_info = Segment.query.all()
    for inf in cron_info:
        segment_contacts = requests.get(current_app.config['URL_SEGMENTS'] + '/' + inf.segment + '/contacts',
                                        headers=current_app.config['HEADERS_AUTH'])
        if segment_contacts is not None and segment_contacts.status_code == 200:
            segment_contacts = json.loads(segment_contacts.text)
            i = 0
            while i < inf.count:
                requests.post('https://api.getresponse.com/v3/contacts/' + segment_contacts[i]['contactId'],
                              headers=current_app.config['HEADERS_AUTH'], data=json.dumps({"tags": [inf.tag]}))
                i += 1