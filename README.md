# Sales Reports

### Requirements
1. python3,
2.     pip3 install -r requirements.txt
### Task-1 :
1. ● Created an Entity for the user model using AbstractBaseUser class and a custom 
user manager using BaseUserManager
 
2. ● Now implement login and registration API with DRF
1.  `{{base_url}}/user/register/`<br>
   Required: <br> full_name,<br> email ,<br>,password, <br> retype_password
2.  `{{base_url}}/user/login/`<br>
Required: <br>
email,<br>password


### Task-2 :
1. ● Create a REST API for data insertion and manipulation
2. fetch & insert sales  <br> `{{base_url}}/api/sales/` <br>
 Insert Required:
    order_id,<br>
ship_date,<br>
ship_mode,<br>
customer_id,<br>
customer_name,<br>
segment,<br>
country,<br>
city,<br>
state,<br>
postal_code,<br>
region,<br>
product_id,<br>
category,<br>
sub_category,<br>
product_name,<br>
sales,<br>
3.  update & delete sales <br> `{{base_url}}/api/sales/<pk>/` 
3. Generate Sales Report: <br>
`{{base_url}}/api/sales/report/`
<br> <b>you'll get a sales pdf file </b>

4. Created an API that will generate a PDF report from the given dataset. The report
include the below information:
<br>
○  Total number of orders count per year
<br>
○ Total count of distinct customers
<br>
○ Top 3 customers who have ordered the most with their total amount of
transactions.
<br>
○ Customer Transactions per Year (from the beginning year to last year)
<br>
○ Most selling items sub-category names
<br>
○ Region basis sales performance pie chart
<br>
○ Sales performance line chart over the years
<br>
1. Fully dynamic  Sales report . You can check by inserting & removing data

### Demo Images

<img src="demo_images/first_page.png">
<img src="demo_images/second.png">
<img src="demo_images/last_page.png">

<br>

### last step: 
1. You don't need to migration & migrate

2.     python3 manage.py runserver

3. If you want to access admin panel
then you use  `{{base_url}}/admin`

4.     
       email:admin@gmail.com
       password:123
### -----------Done------------
