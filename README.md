## Daily Trend

The app intended to fetch the data from Google Trends api with 4 hours interval and store it into DB.
It also provides an API to get the data in Dataframe format.

### Run
First you need to configure the environment by creating `.env` file with following content.
For testing purposes you can set `INTERVAL=1` env variable as well, and it will set the interval to 1 minute, otherwise it will fetch the data with 4 hours interval
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_DB=postgres
REDIS_HOST=redis-service
DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${POSTGRES_DB}
```

To run the project please execute following command:
```bash
docker-compose up
```

### API
To test the api you can send the requests manually from command line.

* Authenticate
    ```bash
    curl --location --request POST 'http://localhost:8000/api/v1/auth/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "username": "admin",
        "password": "admin"
    }'
    ```
    You will get the response with token
    ```json
    {"token":"2693bcf93c4d9e767a97c30605fa3131745bb65c"}
    ```

* Make a request
    
    Now you need to use this token in your requests' header like this:
    ```bash
    curl --location --request GET 'http://localhost:8000/api/v1/search_interest/?keyword=vanna%20white/' \
    --header 'Authorization: Token 2693bcf93c4d9e767a97c30605fa3131745bb65c'
    ```
  
    To get all the keywords in Dataframe format send the request without keyword query parameter.

    ```bash
    curl --location --request POST 'http://localhost:8000/api/v1/search_interest/' \
    --header 'Authorization: Token 2693bcf93c4d9e767a97c30605fa3131745bb65c'
    ```

To run the tests please execute following command:
```bash
docker-compose run server python manage.py test -v 2
```
Or if the containers are already run:
```bash
docker-compose exec server python manage.py test -v 2
```

