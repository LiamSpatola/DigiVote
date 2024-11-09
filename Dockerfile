FROM python:3.13-alpine

WORKDIR /DigiVote

COPY docker-entrypoint.sh /DigiVote/docker-entrypoint.sh

RUN chmod +x /DigiVote/docker-entrypoint.sh

COPY . .

RUN pip install --upgrade pip

RUN pip install -e .

EXPOSE 8000

ENTRYPOINT [ "/bin/sh", "/DigiVote/docker-entrypoint.sh" ]

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
