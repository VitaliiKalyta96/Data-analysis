WITH unified_ads_data AS (
    SELECT
        ad_date,
        url_parameters,
        COALESCE(spend, 0) AS spend,
        COALESCE(impressions, 0) AS impressions,
        COALESCE(reach, 0) AS reach,
        COALESCE(clicks, 0) AS clicks,
        COALESCE(leads, 0) AS leads,
        COALESCE(value, 0) AS value
    FROM facebook_ads_basic_daily
    UNION ALL
    SELECT
        ad_date,
        url_parameters,
        COALESCE(spend, 0) AS spend,
        COALESCE(impressions, 0) AS impressions,
        COALESCE(reach, 0) AS reach,
        COALESCE(clicks, 0) AS clicks,
        COALESCE(leads, 0) AS leads,
        COALESCE(value, 0) AS value
    FROM google_ads_basic_daily
),
processed_data AS (
    SELECT
        ad_date,
        LOWER(
            CASE
                WHEN SUBSTRING(url_parameters FROM 'utm_campaign=([^&]+)') = 'nan'
                THEN NULL
                ELSE SUBSTRING(url_parameters FROM 'utm_campaign=([^&]+)')
            END
        ) AS utm_campaign,
        SUM(spend) AS total_spend,
        SUM(impressions) AS total_impressions,
        SUM(clicks) AS total_clicks,
        SUM(value) AS total_value,
        CASE
            WHEN SUM(impressions) > 0 THEN ROUND(SUM(clicks)::NUMERIC / SUM(impressions), 3)
            ELSE 0
        END AS CTR,
        CASE
            WHEN SUM(clicks) > 0 THEN SUM(spend) / SUM(clicks)
            ELSE 0
        END AS CPC,
        CASE
            WHEN SUM(impressions) > 0 THEN 1000 * SUM(spend) / SUM(impressions)
            ELSE 0
        END AS CPM,
        CASE
            WHEN SUM(spend) > 0 THEN ROUND((SUM(value) - SUM(spend))::NUMERIC / SUM(spend), 3)
            ELSE 0
        END AS ROMI
    FROM unified_ads_data
    GROUP BY ad_date, LOWER(
        CASE
            WHEN SUBSTRING(url_parameters FROM 'utm_campaign=([^&]+)') = 'nan'
            THEN NULL
            ELSE SUBSTRING(url_parameters FROM 'utm_campaign=([^&]+)')
        END
    )
),
monthly_data AS (
    SELECT
        DATE_TRUNC('month', ad_date)::DATE AS ad_month,
        utm_campaign,
        SUM(total_spend) AS total_spend,
        SUM(total_impressions) AS total_impressions,
        SUM(total_clicks) AS total_clicks,
        SUM(total_value) AS total_value,
        CASE
            WHEN SUM(total_impressions) > 0 THEN ROUND(SUM(total_clicks)::NUMERIC / SUM(total_impressions), 3)
            ELSE 0
        END AS CTR,
        CASE
            WHEN SUM(total_clicks) > 0 THEN SUM(total_spend) / SUM(total_clicks)
            ELSE 0
        END AS CPC,
        CASE
            WHEN SUM(total_impressions) > 0 THEN 1000 * SUM(total_spend) / SUM(total_impressions)
            ELSE 0
        END AS CPM,
        CASE
            WHEN SUM(total_spend) > 0 THEN ROUND((SUM(total_value) - SUM(total_spend))::NUMERIC / SUM(total_spend), 3)
            ELSE 0
        END AS ROMI
    FROM processed_data
    GROUP BY DATE_TRUNC('month', ad_date), utm_campaign
),
final_data AS (
    SELECT
        ad_month,
        utm_campaign,
        total_spend,
        total_impressions,
        total_clicks,
        total_value,
        CTR,
        CPC,
        CPM,
        ROMI,
        ROUND(
            (CPM - LAG(CPM) OVER (PARTITION BY utm_campaign ORDER BY ad_month)) 
            / NULLIF(LAG(CPM) OVER (PARTITION BY utm_campaign ORDER BY ad_month), 0) * 100, 2
        ) AS CPM_diff_percent,
        ROUND(
            (CTR - LAG(CTR) OVER (PARTITION BY utm_campaign ORDER BY ad_month)) 
            / NULLIF(LAG(CTR) OVER (PARTITION BY utm_campaign ORDER BY ad_month), 0) * 100, 2
        ) AS CTR_diff_percent,
        ROUND(
            (ROMI - LAG(ROMI) OVER (PARTITION BY utm_campaign ORDER BY ad_month)) 
            / NULLIF(LAG(ROMI) OVER (PARTITION BY utm_campaign ORDER BY ad_month), 0) * 100, 2
        ) AS ROMI_diff_percent
    FROM monthly_data
)
SELECT *
FROM final_data;
