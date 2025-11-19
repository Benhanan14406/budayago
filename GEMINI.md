# Project Overview

This project is a Django-based web API that provides a chatbot interface for learning Javanese and Sundanese. It uses a Gemini-powered chatbot to provide responses in the selected language. The project is structured into three main Django apps: `main`, `user_profile`, and `ai_conversation`.

## Technologies Used

*   **Backend:** Django, Django REST Framework
*   **Authentication:** django-allauth, djangorestframework_simplejwt
*   **Database:** SQLite
*   **AI:** Google Gemini (via LangChain)
*   **Media:** Cloudinary

## Architecture

The project follows a standard Django architecture. The `main` app serves as the main entry point for the API, and it includes the `user_profile` and `ai_conversation` apps.

*   `user_profile`: This app manages user profiles, including their personal information and learning progress.
*   `ai_conversation`: This app provides the chatbot functionality. It uses the Gemini API to generate responses in Javanese or Sundanese, based on the user's selection.

# Building and Running

## Prerequisites

*   Python 3
*   Pip

## Installation

1.  Clone the repository.
2.  Create a virtual environment: `python -m venv env`
3.  Activate the virtual environment: `source env/bin/activate`
4.  Install the dependencies: `pip install -r requirements.txt`
5.  Create a `.env` file in the root directory and add the following environment variables:

    ```
    GOOGLE_CLIENT_ID=<your-google-client-id>
    GOOGLE_CLIENT_SECRET=<your-google-client-secret>
    GEMINI_API_KEY=<your-gemini-api-key>
    CLOUDINARY_NAME=<your-cloudinary-name>
    CLOUDINARY_API_KEY=<your-cloudinary-api-key>
    CLOUDINARY_API_SECRET=<your-cloudinary-api-secret>
    ```

## Running the Project

1.  Apply the database migrations: `python manage.py migrate`
2.  Run the development server: `python manage.py runserver`

The API will be available at `http://localhost:8000/api/`.

# Development Conventions

## Coding Style

The project follows the standard Python PEP 8 coding style.

## Testing

The project includes a `tests.py` file in each app, but there are no tests written yet.

## Contribution Guidelines

There are no contribution guidelines specified in the project.
