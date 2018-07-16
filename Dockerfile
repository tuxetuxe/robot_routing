FROM python:3.7-alpine

ADD requirements.txt /

RUN pip install -r requirements.txt

ADD robot_routing /robot_routing

ENTRYPOINT ["python", "robot_routing"]