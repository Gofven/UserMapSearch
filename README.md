# Simple Django Ninja MapSearch API
This repository consists of a simple API to create users and find users based on a bounding box.

## Installation
By default, the repository is set to DEBUG=True for testing purposes. This can be overridden by creating a .env 
file that overrides it (see .env.example)

### Docker Compose
Install docker compose here: https://hub.docker.com/welcome

To set up the project through docker compose, run `docker compose up -d` within this directory.
There is no need for any additional fields if the .env.example defaults are agreeable.
A DJANGO_SECRET key will be generated automatically into a .env file within the container.
Changes to `backend` and `mapsearch` folder will be reflected on the container.
If you wish to change anything outside of these folders, add the `--build` flag to the docker compose command
e.g. `docker compose up --build -d`.

## API Test Guide
### Creating User
To access the APIs to test, by default, it's located at http://127.0.0.1:8000/api/docs.
To create a user, use `/api/r   egister` and supply with any email and password (e.g. `a@a.se` for testing).
Then, access the API key using `/api/login`.

To authorize the user, at the top right of the page there is an 'Authorize' tab, 
fill in the key you got from the `/api/login` API.

### Setting user location
To set the location for the currently authorized user, use `/api/map/location/update`.
The API takes in `latitude` and `longitude` of the user, which corresponds to the
coordinates using SRID 4326 (WGS84) using floating point numbers e.g. `0.5537452`.


### Getting users within a Bounding Box
To get all users within a bounding box, use the `/api/user/list` API. 
It takes in `min_latitude`, `min_longitude`, `max_latitude` and `max_longitude`, as well as pagination fields and `user_id`.
The latitude and longitude fields are similiar to what's written above, note that it explicitly needs the 
`min_latitude` to be smaller than `max_latitude` and the same for `min_longitude` and `max_longitude`.

