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

## Technologies Used
DigiVote uses multiple modern technologies:
- Django (modern web framework written in python)
- Bootstrap (modern front-end CSS framework)
- Sqlite (simple file based database)

## Setup and Installation
To install DigiVote, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/LiamSpatola/DigiVote
cd digivote
```

2. Create a Python Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependancies
```bash
pip install -e .
```

4. Set Up Environment Variables
<br>Create a file `.env` in the root directory with this content (replacing the values with your own ones):
```env
DJANGO_SECRET_KEY='your-secret-key'
DJANGO_TIMEZONE='Australia/Sydney'
```
#### NOTE: Ensure you keep your secret key secret, and choose something secure as your key.

5. Change to the Project Directory
```bash
cd digivote
```

7. Run Database Migrations
```bash
python3 manage.py migrate # On Windows use `py manage.py migrate`
```

7. Create An Admin User
```bash
python3 manage.py createsuperuser # On Windows use `py manage.py createsuperuser`
```

8. Run the Development Server
```bash
python3 manage.py runserver # On Windows use `py manage.py runserver`
```

#### NOTE: Use a proper server for production. The development server is not intended for production use.

## Usage
To use DigiVote:

1. Navigate to `localhost:8000/admin` and sign in
2. Create users and polls
3. Navigate to `localhost:8000` and sign in
4. Click on `Polls` in the navbar
5. Either click on the `Details` link next to each poll, or press `Vote` to vote in each poll.
6. To close a poll, navigate to `localhost:8000/admin` and sign in, then modify the poll you want to close and uncheck the `Poll Closed` box.
7. To delete a poll, navigate to `localhost:8000/admin` and sign in, then select the poll you want to delete and press `Delete`.

## Contributing
We welcome contributions to DigiVote. Please make sure, if you do decide to contribute, that you adhere to PEP8 standards.

## Licensing
DigiVote is licensed under the GNU GPLv3. The full text of the license is available in the `LICENSE` file or [here](https://www.gnu.org/licenses/gpl-3.0.txt).
