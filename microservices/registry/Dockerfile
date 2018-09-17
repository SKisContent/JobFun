# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
RUN mkdir /app
RUN mkdir /app/registry
WORKDIR /app

# Copy the directory contents into the container at /app
ADD registry/src/registry /app/registry

COPY microservice.py /app
COPY registry/requirements.txt /app

# Need gcc to compile some python packages
RUN apt-get install gcc libc-dev

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80
EXPOSE 9000

# Define environment variable
#ENV REGISTRY_URL "http://localhost"
ENV REGISTRY_PORT 9000
ENV PYTHONPATH /app

# Run api_server.py when the container launches
CMD ["python", "registry/api_server.py"]