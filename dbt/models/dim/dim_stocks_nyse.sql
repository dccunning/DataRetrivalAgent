{{ config(materialized="table", unique_key="symbol", sort=["symbol"], dist="symbol") }}

SELECT
  symbol,
  company_name,
  sector,
  industry,
  beta,
  price,
  last_annual_dividend,
  volume,
  country,
  is_etf,
  is_fund,
  is_actively_trading
FROM {{ source('stocks', 'nyse_stocks') }}