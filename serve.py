import logging, hashlib, hmac, subprocess, sys, os, shlex
from flask import Flask, request

# Config
SCRIPT = "pipeline.sh"
SECRET = "hello"
PORT = 5000
EVENT = 'pr:merged'
BRANCH = 'develop'
FLASK_DEBUG = False

#
# https://docs.python.org/2/howto/logging.html
logging.basicConfig(filename='/mnt/log/webhook.log', level=logging.INFO)

app = Flask(__name__)


def display_html(request):
    url_root = request.url_root
    return "".join([
        """Webhook endpoint is online! """,
        """Go to your repository webhook for """,
        """<a href="%s.alpha/webhook">%s.alpha/webhook</a>""" % (url_root, url_root)
    ])


@app.route('/', methods=['GET'])
def index():
    return display_html(request)


@app.route('/.alpha', methods=['GET'])
def alpha():
    return display_html(request)


@app.route('/.alpha/webhook', methods=['GET', 'POST'])
def webhook():

    logging.debug('Request Type: ' + request.method)
    logging.debug(request.headers)

    if request.headers.get('X-Event-Key') == 'diagnostics:ping':
        return 'Pong', 200

    if request.method == "POST":

        sig_payload = request.headers.get('X-Hub-Signature')
        body = request.get_data()
        sig = 'sha256=' + hmac.new(SECRET, body, hashlib.sha256).hexdigest()
        if sig_payload != sig:
            logging.error('X-Hub-Signature does not match!')
            return "Bad Request", 400

        data = request.get_json()
        logging.info(data)

        # Event Payload JSON API https://confluence.atlassian.com/bitbucketserver/event-payload-938025882.html

        eventKey = data['eventKey']
        date = data['date']
        pr_branch = data['pullRequest']['toRef']['displayId']
        pr_commit_short = data['pullRequest']['properties']['mergeCommit']['displayId']
        pr_commit = data['pullRequest']['properties']['mergeCommit']['id']
        pr_title = data['pullRequest']['title']
        actor = data['actor']['displayName']

        if eventKey == EVENT and pr_branch == BRANCH:
            logging.info('PR merged commit: ' + pr_commit_short + ' on ' + pr_branch + ' by ' + actor)

            working_dir = os.path.dirname(os.path.realpath(__file__))
            logging.debug('working_dir: ' + working_dir)
            cmd = shlex.split('bash ' + SCRIPT + ' ' + pr_commit)
            process = subprocess.Popen(cmd, cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            if out:
                logging.info(out)
            if err:
                logging.error(err)

        return "OK", 200
    else:
        return display_html(request)


if __name__ == '__main__':
    logging.info('Webhook endpoint started...')
    app.run(host="0.0.0.0", port=PORT, debug=FLASK_DEBUG)
