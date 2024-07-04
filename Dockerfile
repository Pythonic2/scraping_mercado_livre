# Use Python 3.11 base image
FROM python:3.11

# Set working directory in the container
WORKDIR /app

ENV DISPLAY=:99

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# Set the default command to run your application
CMD [ "python", "main.py" ]
