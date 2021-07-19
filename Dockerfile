FROM python:3.7

WORKDIR /nasbench
RUN git clone https://github.com/Jason-Choi-SKKU/nasbench-flask-api.git ./
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080

CMD python ./app.py