WITH base_payments AS (
    SELECT
        p.user_id,
        p.game_name,
        DATE_TRUNC('month', p.payment_date::DATE)::DATE AS payment_month,
        p.revenue_amount_usd,
        u.language,
        u.has_older_device_model,
        u.age
    FROM games_payments p
    JOIN games_paid_users u ON p.user_id = u.user_id AND p.game_name = u.game_name
),
user_monthly_payments AS (
    SELECT
        user_id,
        game_name,
        payment_month,
        SUM(revenue_amount_usd) AS total_revenue,
        language,
        age,
        has_older_device_model,
        MAX(payment_month) OVER (PARTITION BY user_id) AS last_paid_month,
        MIN(payment_month) OVER (PARTITION BY user_id) AS first_paid_month,
        DATE(payment_month + INTERVAL '1' month) as next_calendar_month,
		LEAD(payment_month) OVER (PARTITION BY user_id ORDER BY payment_month) AS next_paid_month,
		LAG(payment_month) OVER (PARTITION BY user_id ORDER BY payment_month) AS previous_paid_month,
		DATE(payment_month - INTERVAL '1' month) AS previous_calendar_month,
		LAG(SUM(revenue_amount_usd)) OVER (PARTITION BY user_id ORDER BY payment_month) AS previous_paid_month_revenue
    FROM base_payments
    GROUP BY user_id, game_name, payment_month, language, age, has_older_device_model
),
final_metrics AS (
    SELECT
        user_id,
        game_name,
        payment_month,
        language,
        age,
        has_older_device_model,
        (SUM(total_revenue) * 1.0 / COUNT(DISTINCT user_id))::NUMERIC(10,2) AS ARPPU,
        COUNT(DISTINCT user_id) AS paid_users,
        COUNT(*) FILTER (WHERE payment_month = first_paid_month) AS new_paid_users,
        SUM(total_revenue) AS mrr,
        SUM(total_revenue) FILTER (WHERE payment_month = first_paid_month) AS new_mrr,
        COUNT(DISTINCT CASE WHEN next_paid_month IS NULL OR next_paid_month != next_calendar_month THEN user_id END) AS churned_users,
        SUM(CASE WHEN next_paid_month IS NULL OR next_paid_month != next_calendar_month THEN total_revenue ELSE 0 END) AS churned_revenue,
        SUM(CASE WHEN previous_paid_month = previous_calendar_month AND total_revenue > previous_paid_month_revenue
                 THEN total_revenue - previous_paid_month_revenue END) AS expansion_MRR,
        SUM(CASE WHEN previous_paid_month = previous_calendar_month AND total_revenue < previous_paid_month_revenue
                 THEN total_revenue - previous_paid_month_revenue END) AS contraction_MRR,
        SUM(CASE WHEN previous_paid_month IS DISTINCT FROM previous_calendar_month
                 AND previous_paid_month IS NOT NULL
            THEN total_revenue
        END) AS back_from_churn_mrr
    FROM user_monthly_payments
    GROUP BY user_id, game_name, payment_month, language, age, has_older_device_model
)
SELECT *
FROM final_metrics
ORDER BY payment_month;


