FROM python:3.8

WORKDIR /app

# install chromium driver
RUN apt-get -y update
RUN apt-get install -y chromium chromium-driver

# set display port to avoid crash
ENV DISPLAY=:99

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app
CMD ["python", "./main.py", "--headless", "--fast", "--privacy"]
