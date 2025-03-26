{{ config(materialized="table", unique_key="id", sort=["id", "date"], dist="user_id") }}

SELECT
  id,
  invoice_id,
  user_id,
  date,
  billing_product,
  description,
  type,
  amount,
  currency,
  billing_type
FROM {{ source('digital_bank', 'dim_invoice_item') }}