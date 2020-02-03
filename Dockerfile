FROM python:3
ADD main.py /
COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip3 install -r requirements.txt
COPY . /opt/app
CMD [ "python3", "./main.py" ]
