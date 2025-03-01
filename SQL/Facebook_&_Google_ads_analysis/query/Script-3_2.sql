
WITH facebook_data AS (
    SELECT 
        fabd.ad_date,
        fc.campaign_name,
        fa.adset_name,
        'Facebook Ads' AS media_source,
        fabd.spend,
        fabd.impressions,
        fabd.reach,
        fabd.clicks,
        fabd.leads,
        fabd.value
    FROM facebook_ads_basic_daily fabd
    INNER JOIN facebook_adset fa ON fabd.adset_id = fa.adset_id
    INNER JOIN facebook_campaign fc ON fabd.campaign_id = fc.campaign_id
), google_data AS (
    SELECT 
        g.ad_date,
        g.campaign_name,
        g.adset_name,
        'Google Ads' AS media_source,
        g.spend,
        g.impressions,
        g.reach,
        g.clicks,
        g.leads,
        g.value
    FROM google_ads_basic_daily g
) SELECT 
    ad_date,
    'Google Ads / Facebook Ads' AS media_source,
    campaign_name,
    adset_name,
    SUM(spend) AS total_spend,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    SUM(value) AS total_value
FROM (
    SELECT * FROM facebook_data
    UNION ALL
    SELECT * FROM google_data
) AS combined_ads
GROUP BY ad_date, media_source, campaign_name, adset_name
ORDER BY ad_date, media_source, campaign_name, adset_name;





