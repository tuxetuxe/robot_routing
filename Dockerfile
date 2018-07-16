FROM python:2.7-alpine3.6

ADD requirements.txt /

RUN pip install -r requirements.txt

ADD robot_routing /robot_routing

ENTRYPOINT ["python", "robot_routing"]