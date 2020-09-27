FROM python:2.7
ARG project_name='connect_4_game'

WORKDIR /app/django/{project_name}

ADD ./requirements.txt requirements.txt
RUN cat requirements.txt | xargs -n 1 pip install
RUN echo $(pwd)

ADD . .
CMD ['./gunicorn.bash']


