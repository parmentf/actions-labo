FROM cnrsinist/ezs-python-server:py3.9-no20-1.0.2

USER pn
WORKDIR /app/public
RUN npm install @ezs/teeft@2.3.1 && \
    npm install @ezs/strings@1.0.3
# Declare files to copy in .dockerignore
COPY . /app/public/
