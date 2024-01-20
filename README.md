# My Wellness Workbook

## Deployed 🚀 ([Check it out!](https://mywellnessworkbook-3fc307266e24.herokuapp.com/))
https://mywellnessworkbook-3fc307266e24.herokuapp.com/

## About the Project
My Wellness Workbook is an interactive web application designed to assist users in tracking their daily habits and maintaining a personal journal. Built using the Django framework and Bootstrap for the frontend, this application offers a dynamic experience with real-time updates facilitated through AJAX.

## Features
- **User Authentication**: Secure sign-up, sign-in, and profile management using Django's built-in authentication system.
- **Habit Tracking**: Users can create, track, and visualize their daily habits and progress.
- **Journaling**: A personal space for users to journal their thoughts and reflect on their daily activities.
- **Dynamic Updates**: Real-time updates to habit tracking and journal entries without page reloads.
- **Responsive Design**: A mobile-friendly interface that adapts to various screen sizes for accessibility on any device.

## Technologies Used
- Python
- Django
- HTML
- CSS
- JavaScript
- AJAX
- PostgreSQL
- Heroku

## Getting Started
To get a local copy up and running, follow these simple steps.

### Prerequisites
- Python 3
- pip
- Virtualenv (optional)

### Installation
1. Clone the repository and navigate to it:
   ```sh
   git clone https://github.com/ahmetcucar/wellness-workbook.git
   cd wellness-workbook

2. Create a virtual environment:
   ```sh
   virtualenv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:
   ```sh
   pip install -r requirements.txt

### Running the Application
1. Make migrations and create a database:
   ```sh
   python manage.py makemigrations
   python manage.py migrate

2. Start the development server:
   ```sh
   python manage.py runserver
   Open your browser and navigate to http://127.0.0.1:8000/


## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Ahmet Ucar - ahmetcucar@outlook.com

Project Link: https://github.com/ahmetcucar/wellness-workbook

