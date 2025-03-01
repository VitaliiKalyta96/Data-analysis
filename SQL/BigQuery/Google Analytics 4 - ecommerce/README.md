## Google Analytics 4 - ecommerce

This project about data from Google Analytics 4 and data analysis query in BigQuery. It calculates and analysises
the passage of the funnel by visitors of the eCommerce platform.

### Key features.

#### Prepared data for building reports in BI systems.
Created first query to get a table with information about events, users, and sessions in GA4. As a result of executing 
the query, we get a table that will include the following fields:

- event_timestamp - date and time of the event (data type must be timestamp);
- user_pseudo_id - anonymous user ID in GA4;
- session_id - identifier of the event session in GA4;
- event_name - event name;
- country - country of the website user;
- device_category - device category of the website user;
- source - source of the site visit;
- medium - medium of the site visit;
- campaign - the name of the website visit campaign.

The table includes only data for 2021 and data from the following events:

- Session start on the site;
- Viewing item;
- Adding a product to the cart;
- Begin of checkout;
- Adding shipping information;
- Add payment information;
- Purchase.

#### Calculation of conversions by dates and traffic channels
Created a second query to get a table with information about conversions from the beginning of the session to the purchase.
The resulting table includes the following fields:

- event_date - the date of the session start, obtained from the event_timestamp field;
- source - the source of the site visit;
- medium - medium of the site visit;
- campaign - the name of the website visit campaign;
- user_sessions_count - the number of unique sessions with unique users on the corresponding date and for the corresponding 
traffic channel;
- visit_to_cart - conversion from the beginning of the session on the site to adding a product to the cart (on the relevant 
date and for the relevant traffic channel);
- visit_to_checkout - conversion from the beginning of the session on the site to an attempt to place an order (on the 
appropriate date and for the appropriate traffic channel);
- Visit_to_purchase - conversion from the beginning of the session on the site to the purchase (on the relevant date and 
for the relevant traffic channel).

### Tools and Skills: <span style="font-weight: lighter; font-size: 0,9em;">Google Analytics 4(GA 4), SQL, BiqQuery.</span>