## Overview

This is a project provide it by Dezzex Technology Pvt Ltd to build real-time messaging app


## Getting Started

* [Fork repository][Dezzex Technology Pvt Ltd real-time messaging challenge] and clone it.

<div class="termy">

```console
$ git clone https://github.com/Mohamed-Kaizen/dezzex_technology_pvt_ltd_real_time_messaging_challenge

---> 100%
```

</div>

### Install dependence:

You need to install [python](https://www.python.org/downloads/) and [poetry](https://python-poetry.org/docs/#installation) first

<div class="termy">

```console
$ poetry install && poetry shell

---> 100%
```

</div>

### Run the server:
  
#### 1. Create .env file:

create .env in the root of the project or set your ENV add the following line into .env file or set your ENV:

    DEBUG=True  # change this in production
    ALLOWED_HOSTS=example.com, localhost, 0.0.0.0, 127.0.0.1  # change this in production
    SECRET_KEY=w86k@*ash*z)dsxsoz+o*ne*ugb08(4nu13%8!m*+2_e@@7hnx  # change this in production and never put the production key here
    DATABASE_URL=sqlite:///db.sqlite3  # Choose whatever sql database you want
    EMAIL_USER=example@example.com
    EMAIL_PASSWORD=''


#### 2. Run migrations:
<div class="termy">

```console
$ python manage.py makemigrations

---> 100%
```

</div>

<br></br/>

<div class="termy">

```console
$ python manage.py migrate

---> 100%
```

</div>

#### 3. Load fixtures:

<div class="termy">

```console
$ python manage.py loaddata users.json  chat.json

---> 100%
```

</div>


#### 4. Run the server:

<div class="termy">

```console
$ python manage.py runserver

Django version 4.2.2,
Starting ASGI/Daphne version 4.0.0 development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
</div>


Go the <a href="http://127.0.0.1:8000/admin/"  target="_blank">Admin Page</a> and login with the following credentials:

    username: mohamed
    password: 1234567899mnm


Go to  <a href="http://127.0.0.1:8000/api/docs" target="_blank">Open API UI</a> to see the API documentation


#### 5. Using the API

##### 5.1. Create user:

![Image title](/img/2023-06-09_17-46.png)

##### 5.2. Login:

![Image title](/img/2023-06-09_17-48.png)
![Image title](/img/2023-06-09_17-50.png)


##### 5.3. Create Message:

![Image title](/img/2023-06-09_17-51.png)

##### 5.4. Get Messages:

Only the user who sent the message or the user who received the message can get the message of the room

![Image title](/img/2023-06-09_17-52.png)


#### 6. Websocket

In this example we will use  <a href="https://hoppscotch.io/realtime/websocket"  target="_blank">Hoppscotch</a>

##### 6.1. Connect to websocket:

![Image title](/img/2023-06-09_17-59.png)


##### 6.2. Send your token:

![Image title](/img/2023-06-09_18-00.png)


##### 6.3. Send your message via Admin page <a href="http://127.0.0.1:8000/admin/chat/message/add"  target="_blank">Admin Page</a>:

![Image title](/img/2023-06-09_18-01.png)


##### 6.4. You will receive the message:

![Image title](/img/2023-06-09_18-02.png)


#### 7. Run the tests:

<div class="termy">

```console
$ python manage.py runserver

================= 9 passed in 0.69s ===============
```
</div>

# License: MIT


[Dezzex Technology Pvt Ltd real-time messaging challenge]: https://github.com/Mohamed-Kaizen/dezzex-technology-pvt-ltd-real-time-messaging-challenge
