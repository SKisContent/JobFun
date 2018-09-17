FROM python:3.6

ENV PYTHONUNBUFFERED 1


# Make and set the working directory to /app, copy webapp's contents there
RUN mkdir /app
WORKDIR /app
ADD . /app/

# Need gcc to compile some python packages
RUN apt-get install gcc libc-dev

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
#ENV SERVICE_URL "http://localhost"
ENV REGISTRY_PORT 9000
ENV PYTHONPATH /app

CMD ["ls -la"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]