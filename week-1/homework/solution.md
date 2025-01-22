
Q1: Run docker with the python:3.12.8 image in an interactive mode, use the entrypoint bash.

What's the version of pip in the image?
A1: run the docker file with the commands 
    FROM python:3.12.8
    ENTRYPOINT ["bash"]
    in the bash shell run the comman pip --version
    24.3.1


Q2: Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data

A2: Hostname is DB since it is the service name and services talk to  
    each other on the network using it. Port is 5432 since it is the internal port exposing Postgres service.

Q3: Question 3. Trip Segmentation Count

During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:

    Up to 1 mile
    In between 1 (exclusive) and 3 miles (inclusive),
    In between 3 (exclusive) and 7 miles (inclusive),
    In between 7 (exclusive) and 10 miles (inclusive),
    Over 10 miles


A3: Run the docker compose yaml file and then run the injest data

 SELECT 
    SUM(CASE 
        WHEN trip_distance <= 1 THEN 1
        ELSE 0
    END) AS up_to_1_mile,
    SUM(CASE 
        WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1
        ELSE 0
    END) AS between_1_and_3_miles,
    SUM(CASE 
        WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1
        ELSE 0
    END) AS between_3_and_7_miles,
    SUM(CASE 
        WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1
        ELSE 0
    END) AS between_7_and_10_miles,
    SUM(CASE 
        WHEN trip_distance > 10 THEN 1
        ELSE 0
    END) AS over_10_miles
FROM green_taxi_data
WHERE lpep_pickup_datetime >= '2019-10-01 00:00:00'
  AND lpep_pickup_datetime < '2019-11-01 00:00:00';

  upto 1 mile: 104830
  between 1 and 3 miles: 198995
  between 3 and 7 miles: 109642
  between 7 and 10 miles: 27686
  uver 10 miles: 35201

Q4:  Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.  

A4: WITH longest_trip_day AS (
    SELECT 
        DATE(lpep_pickup_datetime) AS pickup_day,
        MAX(trip_distance) AS max_trip_distance
    FROM green_taxi_data
    GROUP BY DATE(lpep_pickup_datetime)
     )
    SELECT 
    pickup_day,
    max_trip_distance
    FROM longest_trip_day
    ORDER BY max_trip_distance DESC
    LIMIT 1;

    pickup date: 31-10-2019
    longest_trip_distance: 515.89

Q5: Which were the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18?

A5: SELECT 
    z."Zone" AS pickup_zone,
    SUM(g."total_amount") AS total_revenue
FROM green_taxi_data g
LEFT JOIN zones z ON g."PULocationID" = z."LocationID"
WHERE DATE(g."lpep_pickup_datetime") = '2019-10-18'
GROUP BY z."Zone"
HAVING SUM(g."total_amount") > 13000
ORDER BY total_revenue DESC;

East Harlem North - 18686.680
East Harlem South - 16797.260
Morningside Heights - 13029.790

Q6: For the passengers picked up in October 2019 in the zone named "East Harlem North" which was the drop off zone that had the largest tip?

A6: SELECT 
    z_dropoff."Zone" AS dropoff_zone,
    MAX(g."tip_amount") AS largest_tip
FROM green_taxi_data g
JOIN zones z_pickup ON g."PULocationID" = z_pickup."LocationID"
JOIN zones z_dropoff ON g."DOLocationID" = z_dropoff."LocationID"
WHERE z_pickup."Zone" = 'East Harlem North'
  AND g."lpep_pickup_datetime" BETWEEN '2019-10-01' AND '2019-11-01'
GROUP BY z_dropoff."Zone"
ORDER BY largest_tip DESC
LIMIT 1;

JFK Airport - 87.3