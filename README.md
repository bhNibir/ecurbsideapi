<div id="top"></div>

<br />
<div align="center">
  <h1 align="center">
  <strong>
  Ecurbside API
 </strong> </h1>

  <p align="center">
    Medical Treatment Review and Rating GraphQL API!
    <br />
    <br />
    <a href="https://ecurbsideapi.fly.dev/graphql/"><strong>» Live Demo </strong></a> ||
    <a href="https://github.com/bhNibir/ecurbsideui/"><strong>» Ecurbside UI</strong></a>
    <br />
    <br/>

1. Admin login info https://ecurbsideapi.fly.dev/admin

   ```sh
   username: admin
   password: password
   ```
  </p>
</div>

## Description

A GraphQL API For Ecurbside UI <a href="https://github.com/bhNibir/ecurbsideui/"><strong>» Ecurbside UI</strong></a>


<br/>

## Built With

<br/>

- Django
- Graphene django

<br/>
<br/>

## Getting Started

Setting up the project locally.
To get a local copy up and running follow these simple example steps.


### Installation

<br/>

1. Clone the repo
   ```sh
   git clone https://github.com/bhNibir/ecurbsideapi.git
   ```
2. Go to project root folder and Install Django packages

   ```sh
   pip install -r requirements.txt
   ```

3. make .env file and add variables `ecurbsideapi/.env` 
   ```python
    SITE_NAME = TestSite.com
    FRONTEND_DOMAIN = 127.0.0.1:3000
    SECRET_KEY = Secret-key
    EMAIL_HOST_USER = your@gmail.com
    EMAIL_HOST_PASSWORD = password
   ```

4. run devlopment sever
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

<br/>