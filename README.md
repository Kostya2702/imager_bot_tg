# Telegramm bot based @screenshot_bot on Python for an interview.


## Download

If you've Git installed, clone this repo as shown below, otherwise download as ZIP file.

```bash
git clone https://github.com/Kostya2702/imager_bot_tg.git imager
cd imager
```
## Setup

In the imager folder run

```
pip install -r requirements.txt
```

## Run

```
python3 main.py
```

# Create docker container

## Added user to usergroup

In the imager folder run.

```
sudo usermod -aG docker ${USER}
```

Restart the virtual machine or log out on Linux/Mac/Windows and log in again.

## Create containers

```
docker build -t imager . && docker run --restart unless-stopped --cpus 2 -d imager
docker-compose up
```