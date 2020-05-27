# FSND: Capstone Project

Content :
1.motivation
2.Getting started
3.APi documentation
4.Authentication

## Motivation :

This is the last project of the Udacity-Full-Stack-Nanodegree Course, where I was challenged to use all of the concepts and the skills taught in the courses to build an API from start to finish and host it.

## Getting started :

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Running the server

From within the `./backend` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Documentation

### GET /movies :

#### - General:

Returns an object that contains list of movies and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://zizucapstone.herokuapp.com/movies

{
"movies": [
{
"id": 2,
"release_date": "01/01/2000",
"title": "the mask "
}
],
"success": true
}

### GET /movies :

#### - General:

Returns an object that contains list of actors and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://zizucapstone.herokuapp.com/actors

{
"actors": [
{
"age": "28",
"gender": "man",
"id": 2,
"name": "azzeddine"
}
],
"success": true
}

### POST /MOVIE :

#### - General:

Returns an object that contains created movie and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://zizucapstone.herokuapp.com/movies

{
"movie_created": {
"id": 3,
"release_date": "01/01/2000",
"title": "ok"
},
"success": true
}

### POST /ACTOR :

#### - General:

Returns an object that contains created actor and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://zizucapstone.herokuapp.com/actors

{
"actor_created": {
"age": "28",
"gender": "man",
"id": 2,
"name": "azzeddine"
},
"success": true
}

### PATCH /MOVIE :

#### - General:

Returns an object that contains updated movie and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://zizucapstone.herokuapp.com/movies/{id}

{
"success": true,
"updated_movie": {
"id": 3,
"release_date": "01/01/2000",
"title": "batman"
}
}

### PATCH /ACTOR :

#### - General:

Returns an object that contains updated actor and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://zizucapstone.herokuapp.com/actors/{id}

{
"success": true,
"updated_actor": {
"age": "99",
"gender": "man",
"id": 2,
"name": "zizu"
}
}

### DELETE /MOVIE :

#### - General:

Returns an object that contains deleted movie id and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://zizucapstone.herokuapp.com/movies/{id}

{
"deleted_id": 2,
"success": true
}

### DELETE /ACTOR :

#### - General:

Returns an object that contains deleted actor id and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://zizucapstone.herokuapp.com/actors/{id}

{
"deleted_id": 2,
"success": true
}

## Roles:

### Casting Assistant

- Can view actors and movies

### Casting Director

- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies

### xecutive Producer

- All permissions a Casting Director has and…
- Add or delete a movie from the database
