SELECT ad_date, spend, clicks, spend / clicks as spend_per_clicks
FROM public.facebook_ads_basic_daily
WHERE clicks > 0
ORDER By ad_date DESC;