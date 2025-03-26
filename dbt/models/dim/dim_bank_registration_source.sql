{{ config(materialized="table", unique_key="id", sort=["id", "first_login_timestamp"], dist="user_id") }}

SELECT
  id,
  user_id,
  first_login_timestamp,
  source,
  app_os
FROM {{ source('digital_bank', 'dim_registration_source') }}