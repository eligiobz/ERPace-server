FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    apt-get install -y pandoc pandoc-data texlive texlive-latex-recommended texlive-latex-extra texlive-xetex

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
