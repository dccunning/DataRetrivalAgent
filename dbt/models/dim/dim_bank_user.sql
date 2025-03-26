{{ config(materialized="table", unique_key="id", sort=["id", "updated_date"], dist="id") }}

SELECT
  id,
  type,
  EXTRACT(YEAR FROM age(created_date, date_of_birth)) AS age,
  status,
  created_date,
  updated_date,
  country
FROM {{ source('digital_bank', 'dim_user') }}

