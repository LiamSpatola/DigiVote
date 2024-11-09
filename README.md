# DigiVote
A django application for conducting elections and holding votes digitally with ease.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Licensing](#license)

## Features
DigiVote comes with the following features:
- User authentication (log in/log out)
- Admin panel for managing polls and users
- Multiple polls with custom choices
- Clean UI built with Bootstrap
- Security systems to prevent voting multiple times
- Intuitive and simple navigation systems
- Ability to toggle the visibility of polls
- System to print voting receipts for proof of voting
- Open and close dates on polls to configure polls before they occur
- User registration
- Elections with instant runoff voting

## Technologies Used
DigiVote uses multiple modern technologies:
- Django (modern web framework written in python)
- Bootstrap (modern front-end CSS framework)
- Sqlite (simple file based database)
- Docker (containerization service)

## Setup and Installation
To install DigiVote, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/LiamSpatola/DigiVote
cd digivote
```

2. Create a Python Virtual Environment
```bash
python3 -m venv venv # On Windows use `py -m venv venv`
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip3 install -e . # On windows use `pip install -e .`
```

4. Set Up Environment Variables
<br>Create a file `.env` in the root directory with this content (replacing the values with your own ones):
```env
DJANGO_SECRET_KEY="your-secret-key"
DJANGO_TIMEZONE="Australia/Sydney"
AUTOMATICALLY_APPROVE_REGISTRATIONS="true"
DJANGO_HOSTNAME=127.0.0.1
```
#### NOTE: Ensure you keep your secret key secret, and choose something secure as your key.
#### NOTE: The `AUTOMATICALLY_APPROVE_REGISTRATIONS` variable determines whether users will require admin approval to sign up. If you set it to `true`, users will be automatically signed up without admin approval. If you set it to `false`, an admin will need to change the user to `Active` in the admin panel by clicking on the user and checking the box next to `Active` in the admin panel.

5. Change to the Project Directory
```bash
cd digivote
```

6. Create a db.sqlite3 file in a new directory `data`
```bash
mkdir data
touch db.sqlite3 # On Windows use `type nul > db.sqlite3`
```

7. Run Database Migrations
```bash
python3 manage.py migrate # On Windows use `py manage.py migrate`
```

8. Create An Admin User
```bash
python3 manage.py createsuperuser # On Windows use `py manage.py createsuperuser`
```

9. Run the Development Server
```bash
python3 manage.py runserver # On Windows use `py manage.py runserver`
```

#### NOTE: Use a proper server for production. The development server is not intended for production use.

### Docker Installation
If you wish to install using docker, use the following command, replacing the necessary portions:
```docker
docker run -e DJANGO_SUPERUSER_USERNAME=admin \
           -e DJANGO_SUPERUSER_PASSWORD=admin \
           -e DJANGO_SUPERUSER_EMAIL=admin@admin.com \
           -e DJANGO_SECRET_KEY=super-secret-key \
           -e DJANGO_TIMEZONE=UTC \
           -e AUTOMATICALLY_APPROVE_REGISTRATIONS=false \
           -e DJANGO_HOSTNAME=localhost \
           -v ./digivote:/DigiVote/digivote/data \
           -p 8000:8000 \
           -it -d \
           --name digivote \
           liamspatola/digivote
```

Or the following docker compose file, again replacing the necessary portions:
```yaml
services:
  digivote:
    image: liamspatola/digivote
    ports:
      - 8000:8000
    environment:
      - DJANGO_SUPERUSER_USERNAME: admin
      - DJANGO_SUPERUSER_EMAIL: admin@admin.com
      - DJANGO_SUPERUSER_PASSWORD: admin
      - DJANGO_SECRET_KEY: super-secret-key
      - DJANGO_TIMEZONE: UTC
      - AUTOMATICALLY_APPROVE_REGISTRATIONS: false
      - DJANGO_HOSTNAME: localhost
    volumes:
      - digivote:/DigiVote/digivote/data
volumes:
  digivote:
```

The docker repository can be found here: [https://hub.docker.com/r/liamspatola/digivote](https://hub.docker.com/r/liamspatola/digivote).

## Usage
### Creating polls and elections
[Click to view the tutorial](https://scribehow.com/embed/Creating_Polls_and_Elections_in_the_Admin_Panel__x6ES7eIhSMOxlkwsFbl7Kg)

### Register as a new user
[Click to view the tutorial](https://scribehow.com/embed/How_to_Register_a_User_in_DigiVote__wiBxmyAZQKS6tcGq9zLDrA)

### Voting
[Click to view the tutorial](https://scribehow.com/embed/How_To_Vote_Using_The_DigiVote_System__P1falNahRpmVNTa5zeMnZA)

## Contributing
We welcome contributions to DigiVote. Please make sure, if you do decide to contribute, that you adhere to PEP8 standards.

## Licensing
DigiVote is licensed under the GNU GPLv3. The full text of the license is available in the `LICENSE` file or [here](https://www.gnu.org/licenses/gpl-3.0.txt).
