from python : 3.10-slim-buster
workdir /app
copy . /app

run apt-get update -y && apt install awscli -y

run apt-get update &&  pip install --upgrade pip && pip install -r requirements.txt
cmd ["python3", "app.py"]