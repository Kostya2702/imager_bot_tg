FROM python:3.8.10

ARG USER_ID
ARG GROUP_ID

RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user
USER user

# Create app directory
# RUN mkdir /usr/src/app
WORKDIR /usr/src/app
# RUN apt-get update && \
#       apt-get -y install sudo
RUN pip install --upgrade pip


# RUN pip install pip-run --user
# RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
# USER docker
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# ENV PYTHONUNBUFFERED 1
COPY . .
CMD ["python3", "main.py"]
