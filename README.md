### User authentication permission applicaion

A user auth permission application has been built using Python, Custom Token, 
Django, Django rest framework, and drf_spectacular package for API docs. 
Here,  have 3 types of user roles like Admin, Staff, General and 
admin can set user table data access permission through api for Staff users.
admin also can set permissions for staff, who can access (for CRUD operation) 
user table specific columns via API. Staff users access user table data by API
based on their permissions.(for CRUD operation). 


### Installation
```
# Python version 3.10.8
git clone https://github.com/shoumitro-cse/user_auth_permission_api.git
cd user_auth_permission_api
cp env.example .env
python -m venv venv
source ./venv/bin/activate
pip install -r requirments.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
rm -rf static
mv staticfiles static
python manage.py runserver
```

### Sample of curl command code
```angular2html

# user register
curl -X 'POST' \
  'http://localhost:8000/auth/user-list-or-register/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFTOKEN: KX9M9ee2RgDq2k9xEWmqDpHGGFsH4EQQAnoZBK2e33LrfvOjAr4M5EsSqKd5KCvy' \
  -d '{
  "username": "shoumitro23",
  "password": "1111",
  "first_name": "shoumitro",
  "last_name": "ray",
  "email": "shoumitro23@gmail.com",
  "user_type": 1,
  "mobile": "01987543218",
  "address": "Mirpur, Dhaka."
}'

# signin
curl -X 'POST' \
  'http://localhost:8000/auth/login/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFTOKEN: KX9M9ee2RgDq2k9xEWmqDpHGGFsH4EQQAnoZBK2e33LrfvOjAr4M5EsSqKd5KCvy' \
  -d '{
  "username": "shoumitro23",
  "password": "1111"
}'

# to see user list
curl -X 'GET' 'http://localhost:8000/auth/user-list-or-register/' \
-H 'accept: application/json' \
-H 'Authorization: Token 7f843d73b3d549ba1e5b85a2c1bd1b323d4cd8e6'


# It's used for to add user with group.
curl -X 'POST' \
  'http://localhost:8000/auth/add-user-with-group/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Token 7f843d73b3d549ba1e5b85a2c1bd1b323d4cd8e6' \
  -d '{
  "user": 2,
  "group": 1
}'

```

### API docs

```
Here, It has been used as a drf_spectacular package for API docs, I think that it will be 
very helpful for frontend developers. If you would like to see special instructions for 
each api, please keep your eye on each API doc.
protocol = http, https
domain = localhost or others
port = 80, 8000 etc
{protocol}://{domain}:{port}/ (for API HTTP methods and descriptions)
{protocol}://{domain}:{port}/api/redocs/
{protocol}://{domain}:{port}/api/schema/ (for download API ymal file)
```

### API document picture
![](https://github.com/shoumitro-cse/user_auth_permission_api/blob/main/screenshot/api.png?raw=true)

### user signup
![](https://github.com/shoumitro-cse/user_auth_permission_api/blob/main/screenshot/register.png?raw=true)

### user login
![](https://github.com/shoumitro-cse/user_auth_permission_api/blob/main/screenshot/login.png?raw=true)

### for column permission
![](https://github.com/shoumitro-cse/user_auth_permission_api/blob/main/screenshot/column_perm.png?raw=true)

### for admin permission
![](https://github.com/shoumitro-cse/user_auth_permission_api/blob/main/screenshot/super_user.png?raw=true)
