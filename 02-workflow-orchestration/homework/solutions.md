# Workflow Orchestration, Kestra, and ETL Pipelines Quiz

## Q1. Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e., the output file `yellow_tripdata_2020-12.csv` of the extract task)?

- [x] 128.3 MB
- [ ] 134.5 MB
- [ ] 364.7 MB
- [ ] 692.6 MB

**A1.** The file size can be verified by checking the output file of the extract task in Kestra flow execution. **128.3 MB**

---

## Q2. What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?

- [ ] `{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv`
- [x] `green_tripdata_2020-04.csv`
- [ ] `green_tripdata_04_2020.csv`
- [ ] `green_tripdata_2020.csv`

**A2.** The output variable follows the pattern `{taxi}_tripdata_{year}-{month}.csv`, which when rendered with the given inputs becomes **green_tripdata_2020-04.csv**.

---

## Q3. How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?

- [ ] 13,537,299
- [x] 24,648,499
- [ ] 18,324,219
- [ ] 29,430,127

**A3.** The following SQL query retrieves the count:

```sql
SELECT COUNT(*) as total_rows
FROM yellow_tripdata
WHERE filename LIKE 'yellow_tripdata_2020-__.csv';
```

The result is **24,648,499**.

---

## Q4. How many rows are there for the Green Taxi data for all CSV files in the year 2020?

- [ ] 5,327,301
- [ ] 936,199
- [x] 1,734,051
- [ ] 1,342,034

**A4.** The following SQL query retrieves the count:

```sql
SELECT COUNT(*) as total_rows
FROM green_tripdata
WHERE filename LIKE 'green_tripdata_2020-__.csv';
```

The result is **1,734,051**.

---

## Q5. How many rows are there for the Yellow Taxi data for the March 2021 CSV file?

- [ ] 1,428,092
- [ ] 706,911
- [x] 1,925,152
- [ ] 2,561,031

**A5.** The following SQL query retrieves the count:

```sql
SELECT COUNT(*) as total_rows
FROM yellow_tripdata
WHERE filename LIKE 'yellow_tripdata_2021-03.csv';
```

The result is **1,925,152**.

---

## Q6. How would you configure the timezone to New York in a Schedule trigger?

- [ ] Add a timezone property set to `EST` in the Schedule trigger configuration
- [x] Add a timezone property set to `America/New_York` in the Schedule trigger configuration
- [ ] Add a timezone property set to `UTC-5` in the Schedule trigger configuration
- [ ] Add a location property set to `New_York` in the Schedule trigger configuration

**A6.** The timezone configuration uses the IANA timezone format, hence **"America/New_York"** is the proper identifier for New York's timezone.
