# Questions and Solutions

## Q1: Run docker with the python:3.12.8 image in an interactive mode, use the entrypoint bash.

### What's the version of pip in the image?

#### Solution:
Run the following Dockerfile:

```dockerfile
FROM python:3.12.8
ENTRYPOINT ["bash"]
```

After starting the container, in the bash shell, run the following command:

```bash
pip --version
```

#### Output:
```
24.3.1
```

---

## Q2: Given the following `docker-compose.yaml`, what is the hostname and port that pgAdmin should use to connect to the Postgres database?

```yaml
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
```

#### Solution:
- Hostname: `db` (service name).
- Port: `5432` (internal Postgres port exposed to the network).

---

## Q3: Trip Segmentation Count

### Question:
During the period of October 1st, 2019 (inclusive) and November 1st, 2019 (exclusive), how many trips happened:
1. Up to 1 mile.
2. In between 1 (exclusive) and 3 miles (inclusive).
3. In between 3 (exclusive) and 7 miles (inclusive).
4. In between 7 (exclusive) and 10 miles (inclusive).
5. Over 10 miles.

#### Solution:
Run the following SQL query:

```sql
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
```

#### Output:
- Up to 1 mile: `104830`
- Between 1 and 3 miles: `198995`
- Between 3 and 7 miles: `109642`
- Between 7 and 10 miles: `27686`
- Over 10 miles: `35201`

---

## Q4: Which was the pickup day with the longest trip distance?

#### Solution:
Run the following SQL query:

```sql
WITH longest_trip_day AS (
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
```

#### Output:
- Pickup date: `2019-10-31`
- Longest trip distance: `515.89`

---

## Q5: Which were the top pickup locations with over 13,000 in total amount (across all trips) for 2019-10-18?

#### Solution:
Run the following SQL query:

```sql
SELECT 
    z."Zone" AS pickup_zone,
    SUM(g."total_amount") AS total_revenue
FROM green_taxi_data g
LEFT JOIN zones z ON g."PULocationID" = z."LocationID"
WHERE DATE(g."lpep_pickup_datetime") = '2019-10-18'
GROUP BY z."Zone"
HAVING SUM(g."total_amount") > 13000
ORDER BY total_revenue DESC;
```

#### Output:
- East Harlem North: `18686.680`
- East Harlem South: `16797.260`
- Morningside Heights: `13029.790`

---

## Q6: For the passengers picked up in October 2019 in the zone named "East Harlem North", which was the drop-off zone that had the largest tip?

#### Solution:
Run the following SQL query:

```sql
SELECT 
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
```

#### Output:
- Drop-off zone: `JFK Airport`
- Largest tip: `87.3`


## Which of the following sequences, respectively, describes the workflow for:

    Downloading the provider plugins and setting up backend,
    Generating proposed changes and auto-executing the plan
    Remove all resources managed by terraform`

#### Solution:
  terraform init, terraform apply -auto-approve, terraform destroy

