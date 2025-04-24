# Eventure

Eventure is an event-registration app built with Django. Administrators can create and delete events, view event reports, and view user reports. Registrants can create accounts, register for events, cancel their registrations, and track the events they are attending.

## Features

- User authentication (sign-up, log-in, log-out)
- Two user roles: **Administrator** and **Registrant**
- Administrators can create, edit, and delete events
- Registrants can register and unregister for events
- “My Events” page for registrants
- Event and user reports for administrators
- MySQL database support via a `.env` file
- Responsive UI built with Tailwind CSS

## Installation

1. **Clone the repository**

   ```bash
   https://github.com/anexinwilson/anexin.wilson-256A03.git
   cd eventureproject 
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   ```

   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**

   Create a file named `.env` in the project root:

   ```ini
   DB_NAME=your_database_name
   DB_USER=your_mysql_user
   DB_PASSWORD=mysql_password
   DB_HOST=mysql_host
   DB_PORT=25060
   ```

   *Note*: You can skip the `.env` file and use SQLite for local testing.

# SQLite Configuration in `settings.py`

To use SQLite instead of MySQL for local testing in your Django project, follow these steps in `eventureproject/eventure/settings.py`:

1. **Comment out the MySQL database configuration**:

   ```python
   # DATABASES = {
   #     'default': {
   #         'ENGINE': 'django.db.backends.mysql',
   #         'NAME': config('DB_NAME'),
   #         'USER': config('DB_USER'),
   #         'PASSWORD': config('DB_PASSWORD'),
   #         'HOST': config('DB_HOST'),
   #         'PORT': config('DB_PORT'),
   #         'OPTIONS': {
   #             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
   #         }
   #     }
   # }
   ```

2. **Uncomment the SQLite database configuration**:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }
   ```

6. **Apply migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create an administrator account (optional)**

   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000` in your browser.

## Usage

### Administrators
- Sign in to create, edit, or delete events
- View reports of all events or registrants for a single event
- View a list of all users

### Registrants
- Sign up for an account
- View available events and register/unregister
- See a list of their own registered events

