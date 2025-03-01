SELECT
    ad_date, 
    campaign_id, 
    SUM(spend) AS total_spend,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    SUM(value) AS total_value,
    SUM(spend) / SUM(clicks) AS CPC,
    1000 * SUM(spend) / SUM(impressions) AS CPM,
    ROUND(SUM(clicks)::NUMERIC / SUM(impressions), 3) AS CTR,
    ROUND((SUM(value) - SUM(spend))::NUMERIC / SUM(spend), 3) AS ROMI
FROM
    public.facebook_ads_basic_daily
WHERE 
	spend > 0 AND clicks > 0 AND impressions > 0
GROUP BY
    ad_date, 
    campaign_id
ORDER BY
    ad_date, 
    campaign_id;
  
   
SELECT
    campaign_id,
    SUM(spend) AS total_spend,
    ROUND((SUM(value) - SUM(spend))::NUMERIC / SUM(spend), 3) AS ROMI
FROM
    public.facebook_ads_basic_daily
GROUP BY
    campaign_id
HAVING
    SUM(spend) >= 500000
ORDER BY
    ROMI DESC
LIMIT 1;


