# BigQuery Setup

For this homework, we will be using the Yellow Taxi Trip Records for January 2024 - June 2024, NOT the entire year of data, Parquet Files from the New York City Taxi Data.

## Create External Table
```sql
CREATE OR REPLACE EXTERNAL TABLE `dtc-de-course-448917.nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://sri_dezoomcamp_hw3_2025/yellow_tripdata_2024-*.parquet']
);
```

## Create a Non-Partitioned Table from External Table
```sql
CREATE OR REPLACE TABLE `dtc-de-course-448917.nytaxi.external_yellow_tripdata_non_partitioned` AS
SELECT * FROM `dtc-de-course-448917.nytaxi.external_yellow_tripdata`;
```

## Create a Partitioned and Clustered Table (Question 5)
```sql
CREATE OR REPLACE TABLE `dtc-de-course-448917.nytaxi.external_yellow_tripdata_partitioned_clustered`
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `dtc-de-course-448917.nytaxi.external_yellow_tripdata`;
```

## Questions and Answers

### Question 1: What is count of records for the 2024 Yellow Taxi Data?

- 65,623
- 840,402
- **20,332,093** ✅
- 85,431,289

```sql
SELECT count(*) FROM `dtc-de-course-448917.nytaxi.external_yellow_tripdata`;
```

### Question 2: Estimated Data Read for Distinct PULocationIDs Query

- **0 MB for the External Table and 155.12 MB for the Materialized Table** ✅
- 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- 2.14 GB for the External Table and 0MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table

```sql
SELECT DISTINCT(count(PULocationID)) FROM `dtc-de-course-448917.nytaxi.external_yellow_tripdata_non_partitioned`;
-- 155.12 MB

SELECT DISTINCT(count(PULocationID)) FROM `dtc-de-course-448917.nytaxi.external_yellow_tripdata`;
-- 0 MB
```

### Question 3: Why Are the Estimated Bytes Different for Selecting One vs Two Columns?

- **BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.** ✅
- BigQuery duplicates data across multiple storage partitions...
- BigQuery automatically caches the first queried column...
- When selecting multiple columns, BigQuery performs an implicit join...

```sql
SELECT PULocationID FROM `dtc-de-course-448917.nytaxi.external_yellow_tripdata_non_partitioned`;
-- 155.12 MB

SELECT PULocationID, DOLocationID FROM `dtc-de-course-448917.nytaxi.external_yellow_tripdata_non_partitioned`;
-- 465.36 MB
```

### Question 4: How Many Records Have a Fare Amount of 0?

- 128,210
- 546,578
- 20,188,016
- **8,333** ✅

```sql
SELECT count(*) FROM `dtc-de-course-448917.nytaxi.external_yellow_tripdata_non_partitioned` WHERE fare_amount = 0;
```

### Question 5: Best Strategy for Optimized Table for Filtering on `tpep_dropoff_datetime` and Ordering by `VendorID`

- **Partition by tpep_dropoff_datetime and Cluster on VendorID** ✅
- Cluster on tpep_dropoff_datetime and Cluster on VendorID
- Cluster on tpep_dropoff_datetime Partition by VendorID
- Partition by tpep_dropoff_datetime and Partition by VendorID

 > **Explanation**:Queries will always filter by tpep_dropoff_datetime and order by VendorID, the best approach is to partition the table by tpep_dropoff_datetime and cluster it by VendorID

### Question 6: Estimated Bytes for Distinct VendorID Query (March 1-15, 2024)

- 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
- **310.24 MB for non-partitioned table and 26.84 MB for the partitioned table** ✅
- 5.87 MB for non-partitioned table and 0 MB for the partitioned table
- 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table

```sql
SELECT DISTINCT VendorID
FROM `dtc-de-course-448917.nytaxi.external_yellow_tripdata_non_partitioned`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15'
ORDER BY VendorID;
-- 310.24 MB

SELECT DISTINCT VendorID
FROM `dtc-de-course-448917.nytaxi.external_yellow_tripdata_partitioned_clustered`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15'
ORDER BY VendorID;
-- 26.86 MB
```

### Question 7: Where is the Data Stored in the External Table?

- Big Query
- Container Registry
- **GCP Bucket** ✅
- Big Table

### Question 8: Is it Best Practice to Always Cluster Your Data?

- **False** ✅
- True

> **Explanation**: Unless most queries include filtering or ordering, clustering will introduce unnecessary overhead.