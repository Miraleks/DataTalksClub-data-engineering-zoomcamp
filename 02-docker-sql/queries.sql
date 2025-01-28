' During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:

' Up to 1 mile
' In between 1 (exclusive) and 3 miles (inclusive),
' In between 3 (exclusive) and 7 miles (inclusive),
' In between 7 (exclusive) and 10 miles (inclusive),
' Over 10 miles

SELECT
    CASE
        WHEN trip_distance <= 1 THEN 'Up to 1 mile'
        WHEN trip_distance > 1 AND trip_distance <= 3 THEN 'In between 1 (exclusive) and 3 miles (inclusive)'
        WHEN trip_distance > 3 AND trip_distance <= 7 THEN 'In between 3 (exclusive) and 7 miles (inclusive)'
        WHEN trip_distance > 7 AND trip_distance <= 10 THEN 'In between 7 (exclusive) and 10 miles (inclusive)'
        ELSE 'Over 10 miles'
    END AS distance_category,
    COUNT(*) AS trip_count
FROM green_tripdata_2019_10
WHERE lpep_pickup_datetime >= '2019-10-01 00:00:00'
  AND lpep_pickup_datetime < '2019-11-01 00:00:00'
GROUP BY distance_category
ORDER BY distance_category;

' Which was the pick up day with the longest trip distance?

WITH daily_longest_trips AS (
    SELECT
        DATE(lpep_pickup_datetime) AS pickup_date,
        MAX(trip_distance) AS max_distance
    FROM green_tripdata_2019_10
    GROUP BY DATE(lpep_pickup_datetime)
)

SELECT
    pickup_date,
    max_distance
FROM daily_longest_trips
ORDER BY max_distance DESC
LIMIT 1;

' Which were the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18?

SELECT
    t.PULocationID,
    z.borough,
    z.zone,
    SUM(t.total_amount) AS total_amount
FROM
    green_tripdata_2019_10 t
JOIN
    taxi_zone_lookup z ON t.PULocationID = z.LocationID
WHERE
    DATE(t.lpep_pickup_datetime) = '2019-10-18'
GROUP BY
    t.PULocationID, z.borough, z.zone
HAVING
    SUM(t.total_amount) > 13000
ORDER BY
    total_amount DESC;

' For the passengers picked up in October 2019 in the zone named "East Harlem North" which was the drop off zone
' that had the largest tip?

SELECT
    z.zone,
    MAX(t.tip_amount) AS largest_tip
FROM
    green_tripdata_2019_10 t
JOIN
    taxi_zone_lookup z ON t.DOLocationID = z.LocationID
WHERE
    DATE(t.lpep_pickup_datetime) >= '2019-10-01'
    AND DATE(t.lpep_pickup_datetime) < '2019-11-01'
    AND z.zone = 'East Harlem North'
GROUP BY
    z.zone
ORDER BY
    largest_tip DESC
LIMIT 1;