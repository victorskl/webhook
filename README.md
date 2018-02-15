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

python serve.py

chmod +x start.sh
cp webhook.service /etc/systemd/system
systemctl enable webhook
systemctl start webhook
```