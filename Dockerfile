FROM python:3.12-alpine
WORKDIR /DigiVote
COPY docker-entrypoint.sh /DigiVote/docker-entrypoint.sh
RUN chmod +x /DigiVote/docker-entrypoint.sh
COPY . .
RUN pip install -e .
EXPOSE 8000
ENTRYPOINT [ "bash", "/DigiVote/docker-entrypoint.sh" ]
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
