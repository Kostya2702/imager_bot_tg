# Telegram bot based @screenshot_bot on Python for an interview.


## Download

If you've Git installed, clone this repo as shown below, otherwise download as ZIP file.

```bash
git clone https://github.com/Kostya2702/imager_bot_tg.git imager
cd imager
```

## Prerequisite

Create .env file with your environments variables:

- TOKEN - bot token
- ADMIN_ID - your user id in Telegram
- PG_USER - database owner
- PG_PASS - user database password
- PG_HOST - database host (localhost/host docker container)

## Setup

In the imager folder run

```
pip install -r requirements.txt
```

Initialize table in database if not already created

```
python3 db_definition.py
```

## Run

```
python3 main.py
```

# Create docker container

## Added user to usergroup

In the imager folder run command below for run docker without sudo.

```
sudo usermod -aG docker ${USER}
```

Restart the virtual machine or log out on Linux/Mac/Windows and log in again.

## Create containers

```
docker-compose up
```
