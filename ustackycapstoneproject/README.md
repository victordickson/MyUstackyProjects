# The Project
The project is a simple portal web application for students.  
[Hosted Link](https://ancient-shelf-24799.herokuapp.com/)  
The portal application allows students to enter their personal and academic details. Each student’s details can also be managed in the application.

## Pages
1. The landing page(home page) ("/") GET
2. The students index page ("/admin/students") GET
3. The student registration page ("/student/new") GET
4. The student details page ("/admin/students/\<id\>") GET

## Setup
1. Add a `.env` file in the project directory according to the `.env.example` file
2. Run `python -m venv venv` to setup a virtual environment
3. Run `venv\Scripts\activate` (on Windows) to activate the virtual environment
4. Run `pip install -r requirements.txt` to install all necessary packages in the virtual environment
5. In `app.py`, set `debug=True` in `app.run()` if running in development mode
6. Run `python app.py` to start up the application