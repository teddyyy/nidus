# nidus
Notification of Internet Draft Update using Slack

## Install
```
pip install -r requirements.txt
```

## Run Script
```
python notify.py SLACK_BOT_USER_OAUHT_TOKEN
```

## Docker Environment
### Build Image
```
docker build . -t nidus
```

### Run Script
```
docker run -it nidus python notify.py xoxb-xxxxxxxxxx
```
