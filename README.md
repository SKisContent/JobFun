JobFun is a learning project involving microservices, messaging, maybe some react, and anything else that seems interesting or relevant. It also offers some fun tools for people who're looking for work. The first one takes URLs for job postings on Dice.com and converts the Job Description text to word clouds.

The back end is comprised of a Django server that is the API Gateway, a microservice that acts as a registry for other microservices, and the services themselves. It's not ready for prime time, but if you're just starting out learning about micro-services, it's got everything you need to set up and get running. Then you can expand and refine on your own.

This project is currently written so that everything can be run locally or one machine. The live production scenario would involve deploying on multiple servers or containers, etc. It's possible to do without a lot of code modification. 


Requirements
------------

* Python 3.x
* virtualenv
* git (optional)
* depending on what's already installed, you may need to install more libraries, gcc, etc. I had to install the following: gcc, python3-dev, python3-tk


Getting started
---------------

+ Download this project or clone it from here.
```
git clone https://github.com/SKisContent/JobFun.git
```
+ Create a new virtual environment (you may need to install it.)

```bash
$ cd JobFun
$ virtualenv -p python3 venv
$ . venv/bin/activate
```

+ Install the Python requirements.

```bash
$ pip install -r requirements.txt
```

+ Run the Django migrations 

```bash
$ ./manage.py migrate
```

+ Start the registry
```bash
export PYTHONPATH=`pwd`/microservices
python microservices/registry/api_server.py &
```

+ Start the microservices. The order doesn't matter, as it shouldn't. Switch them around for yourself and see.
```bash
export PYTHONPATH=`pwd`/microservices
python microservices/cloud_creator/api_server.py &
python microservices/dice_scraper/api_server.py &
python microservices/fetch_url/api_server.py &
```

+ Start the Django server and go to: [localhost:8000](http://localhost:8000)


```bash
$ ./manage.py runserver
```

#Is it working?

It's always the big question. You can try out some of the microservices just from the command line. For example:
```bash
curl -i -d "html=<html><body><div id='jobdescSec'>This is fun</div></body></html>" http://localhost:8887/api/v1/words
```
It should respond with:
```text
{"data": "This is fun"}
```
