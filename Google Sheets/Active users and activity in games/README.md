## Active users and activity in games

This project is dedicated to analyzing variability and calculating product engagement metrics. Linear regression is used 
to predict the values. Functions and dates were calculated in Google Sheets, graphs, pivot tables, and tables for cohort 
analysis were created.

### Key features:

In the file on the sheets, “active users” is defined for the age of users:
1. The average age.
2. Standard deviation (standard deviation).
3. Median.
4. Interquartile range.
5. 10th percentile of age.
6. 90th percentile of age.

Calculated DAU, WAU and stickiness of users. DAU and WAU were forecasted.

📊 4 charts have been built:

✅ A chart with data from the “active users” page. This is a horizontal bar chart that displays the number of users for 
each language.

✅ A chart with data from the “active users” page. This is a pie chart that shows the breakdown of users by 
has_older_device_model.

✅ A chart with data from the “WAU” page, with weeks on the horizontal axis and two vertical axes: WAU and DAU/WAU. 
WAU is visualized by bars, and DAU/WAU by a line.

✅ A chart with data from the WAU page, which contains weeks on the horizontal axis and WAU values on the vertical axis. 
A linear trendline has been added to this chart.

Calculated text functions and dates in Google Sheets. A pivot table is created.
1. In the “activity” email, game_activity_name is divided into two parts: the name of the game and the name of the activity.
2. 8 activity names are combined into 5 activity types and the activity type is displayed in a separate column in the 
“activity” sheet. I used the VLOOKUP function.
3. On the “activity” sheet, created a column with the user's language and fill it in. The data from the “active users” 
sheet is used.
4. On the “activity” sheet, created three columns that are derived from the “activity_date” column:

   a. Activity month - the month of activity, i.e. the month in which the activity_date is included.

   b. First activity month - the first month of activity for each user. The MINIFS function is used here.

   c. Activity month number - the activity month number. That is, how many months have passed from the First activity month 
      to Activity month.

5. Created a new sheet “Cohort analysis” with a pivot table that uses data from the “activity” sheet.
6. The pivot table displays the Activity month number in the rows and the number of unique users as a value.
7. The number of users in each month of activity is visualized. A line chart is created with a horizontal axis - 
Activity month number and a vertical axis - the number of users who have the corresponding month number.

Created two tables for cohort analysis. Conditional formatting (gradient) is applied to both tables to highlight the 
largest and smallest values. You can filter the data in the tables using slices.

📂 [File on Google Sheets](https://docs.google.com/spreadsheets/d/1YfVSkavR4RxPsHpB5Tzvlmpi2nYPuIQZDU80jtwomTs/edit?gid=0#gid=0)
Link on file on Google Sheets.

### Tools and Skills:: <span style="font-weight: lighter; font-size: 0.9em;">Google Sheets, Files(CSV format), Charts/Graphs, Pivot tables, Analytical skills.</span>