FROM python:3.7-stretch

WORKDIR /data/app
COPY . .

RUN pip install -r requirements.txt
RUN pip install .

VOLUME /data/db
CMD ["./run.sh"]

