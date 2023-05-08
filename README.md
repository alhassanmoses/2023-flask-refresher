# A 2023 refresher of my flask framework knowledge


## Getting started

Once you have cloned the repo and created a virtual environment, take a few minutes to look through the files to familiarise yourself with the project structure. Also a `.env` file needs to be created with content for the environment variriables which can be found in `.env.example`


## Installation

Install with pip:

```
$ pip install -r requirements.txt
```
 
## Run Flask

In flask, the Default port is `5000`

Swagger documentation page:  `http://127.0.0.1:5000/swagger-ui`

### Run in Virtual Environment

```
$ flask run
```


### Run with Docker

```
$ docker build -t flask-rest-apis .

$ docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-rest-apis 
 
```

### Run with Docker (with hot-reload)

```
$ docker build -t flask-rest-apis .

$ docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-rest-apis sh -c "flask run"
 
```

### Running Migrations Manually

```
$ flask db migrate

$ flask db upgrade
 
```

## Reference

Offical Website

- [Flask](http://flask.pocoo.org/)
- [Flask Extension](http://flask.pocoo.org/extensions/)
- [flask-smorest](https://flask-smorest.readthedocs.io/en/latest/)
- [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
- [gunicorn](http://gunicorn.org/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)
- [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/)