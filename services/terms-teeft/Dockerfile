FROM cnrsinist/ezs-python-server:py3.9-no16-1.0.4

RUN npm install @ezs/teeft@2.3.1 && \
    npm install @ezs/strings@1.0.3

USER daemon
WORKDIR /app/public
# Declare files to copy in .dockerignore
COPY . /app/public/
