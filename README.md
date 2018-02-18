# webhook

A simple repository webhook for CI/CD pipeline

### Testing Pipeline Script

- Open one terminal and `watch less queue`

- Open another terminal and `bash test_pipeline.sh`


### Start Webhook Endpoint

```
pip install virtualenv
virtualenv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp config.json.sample config.json

python serve.py
[ctrl+c]
```

Running as systemd service

```
cd /home/deploy
git clone https://github.com/victorskl/webhook.git
cd webhook
chmod +x start.sh
mkdir -p /mnt/log
chown -R deploy:deploy /mnt/log
cp webhook.service /etc/systemd/system
systemctl enable webhook
systemctl start webhook
systemctl status webhook
tail -f /mnt/log/webhook.log

curl -X GET http://0.0.0.0:5000/.alpha/webhook
```