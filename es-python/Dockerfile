FROM python:3
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /src
WORKDIR /src
CMD ["python", "run.py", "streaming"]
