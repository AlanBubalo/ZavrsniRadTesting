# Python UML Engine

## Steps

- Copy your XMI file to `/models` folder
- Setup `env.py` with credentials
- Run `baserow_init.py`

Before you integrate a model in your database, you must copy your XMI file to `/models` folder and create your `env.py` file in a main directory.

## Setup `env.py` file

    URL = YOUR_URL # Use http://baserow.io if you have a database on their server
    EMAIL = YOUR_EMAIL_BASEROW_ACCOUNT
    PASSWORD = YOUR_PASSWORD_BASEROW_ACCOUNT
    GROUP_NAME = YOUR_GROUP_NAME
    DATABASE_NAME = YOUR_DATABASE_NAME
    XMI_FILE = YOUR_XMI_FILE_NAME.xmi

## Create a virtual environment and run `baserow_init.py`

    py -m venv ./env
    env\Scripts\activate
    python baserow_init.py
