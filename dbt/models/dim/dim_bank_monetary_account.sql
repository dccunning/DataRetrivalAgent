{{ config(materialized="table", unique_key="id", sort=["id", "created_on"], dist="user_id") }}

SELECT
  id,
  user_id,
  created_on,
  currency,
  status,
  type,
  balance,
  description,
  iban_country
FROM {{ source('digital_bank', 'dim_monetary_account') }}