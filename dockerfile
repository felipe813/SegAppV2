FROM ubuntu:latest
  
MAINTAINER Andres Sanchez <andresfelipesanchezcruz@gmail.com>

# Update and Install python packages

RUN apt update && apt -y dist-upgrade \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# Copy project to folder

RUN  mkdir -p /SegApp
COPY . /SegApp

WORKDIR /SegApp

# Activate virtual environment

RUN pip3 install -r requirements.txt


# expose port
EXPOSE 8000/tcp

# Test
CMD ["python3","manage.py","test"]

CMD ["python3","manage.py","runserver","0.0.0.0:8013"]