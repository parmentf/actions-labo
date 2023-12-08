FROM cnrsinist/ezs-python-server:py3.9-no16-1.0.4

USER root
RUN pip install \
    backoff==2.2.1 \
    pandas==2.1.3 \
    plac==1.4.1 \
    ratelimit==2.2.1 \
    requests==2.31.0 \
    unidecode==1.3.7

USER daemon
WORKDIR /app/public
# Declare files to copy in .dockerignore
COPY . /app/public/
