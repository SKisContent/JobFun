# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
RUN mkdir /app
RUN mkdir /app/dice_scraper
WORKDIR /app

# Copy the directory contents into the container at /app
ADD dice_scraper/src/dice_scraper /app/dice_scraper

COPY microservice.py /app
COPY dice_scraper/requirements.txt /app

# Need gcc to compile some python packages
RUN apt-get install gcc libc-dev

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80
EXPOSE 8887

# Define environment variable
#ENV SERVICE_URL "http://localhost"
ENV REGISTRY_PORT 9000
ENV PYTHONPATH /app

# Run api_server.py when the container launches
CMD ["python", "dice_scraper/api_server.py"]