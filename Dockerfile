FROM python:3.12
WORKDIR /DigiVote
COPY setup.sh /DigiVote/setup.sh
RUN chmod +x /DigiVote/setup.sh
COPY . .
RUN pip install -e .
EXPOSE 8000
ENTRYPOINT [ "/DigiVote/setup.sh" ]
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
