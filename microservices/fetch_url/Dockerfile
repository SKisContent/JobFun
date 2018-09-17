FROM python:3.6

# Set the working directory to /app
RUN mkdir /app
RUN mkdir /app/fetch_url
WORKDIR /app

# Copy the directory contents into the container at /app
ADD fetch_url/src/fetch_url /app/fetch_url

COPY microservice.py /app
COPY fetch_url/requirements.txt /app

# Need gcc to compile some python packages
RUN apt-get install gcc libc-dev

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8888 available to the world outside this container
EXPOSE 8888

# Define environment variable
#ENV SERVICE_URL "http://localhost"
ENV REGISTRY_PORT 9000
ENV PYTHONPATH /app

# Run api_server.py when the container launches
CMD ["python", "fetch_url/api_server.py"]