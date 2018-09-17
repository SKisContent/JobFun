FROM skiscontent/python3.6_matplotlib

# Set the working directory to /app
RUN mkdir /app
RUN mkdir /app/cloud_creator
WORKDIR /app

# Copy the directory contents into the container at /app/cloud_creator
ADD cloud_creator/src/cloud_creator /app/cloud_creator

COPY microservice.py /app
COPY cloud_creator/requirements.txt /app

# Need gcc to compile some python packages
RUN apt-get install gcc libc-dev

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8886 available to the world outside this container
EXPOSE 8886

# Define environment variable
#ENV SERVICE_URL "http://localhost"
#ENV REGISTRY_PORT 9000
ENV PYTHONPATH /app

# Run api_server.py when the container launches
CMD ["python", "cloud_creator/api_server.py"]