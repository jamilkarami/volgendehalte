FROM python:3.12
COPY ./requirements.txt /vhalte/requirements.txt
WORKDIR /vhalte
RUN pip install -r requirements.txt
COPY . /vhalte

ENTRYPOINT [ "python" ]
CMD [ "main.py" ]