FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y nodejs npm python-pip virtualenv git

# Set the working directory to /build_docker
WORKDIR /build_docker

# Copy the current directory contents into the container at /app
ADD . /build_docker

# Install gui js dependencies
RUN cd app && npm i

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
# RUN virtualenv .
# RUN .virtualenv/bin/activate && pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["sh", "docker/explorer/start.sh"]
