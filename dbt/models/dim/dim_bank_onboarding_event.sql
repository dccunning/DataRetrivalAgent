{{ config(materialized="table", unique_key="event_id", sort=["event_id", "timestamp"], dist="user_id") }}

SELECT
  event_id,
  user_id,
  timestamp,
  button_type,
  screen_name
FROM {{ source('digital_bank', 'dim_event_onboarding') }}