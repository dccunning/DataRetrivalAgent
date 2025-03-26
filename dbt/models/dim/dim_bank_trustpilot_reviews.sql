{{ config(materialized="table", unique_key="review_id", sort=["review_id", "createdtimestamp"], dist="user_id") }}

SELECT
  review_id,
  user_id,
  createdtimestamp,
  stars,
  text,
  source,
  is_review_verified
FROM {{ source('digital_bank', 'dim_trustpilot_reviews') }}