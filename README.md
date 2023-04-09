
# Zingooo - Attendance Tracker

Zingooo is a web application built using Django, HTML, CSS, and JS to enable Mandsaur University students to track their attendance. Unlike other attendance tracking applications, Zingooo fetches data directly from the university database, so students simply have to enter their credentials to access their attendance record.

To accomplish this, Zingooo utilizes a request library to send a GET request to the university website with the user's login credentials. Once authenticated, the project sends another request to a different endpoint to retrieve the attendance data in JSON format. The project then processes this JSON object and displays the attendance information on the web application.

By automating the attendance tracking process, Zingooo simplifies the task of keeping track of attendance for both students and university staff. Its intuitive interface and seamless integration with the university database make it a valuable tool for ensuring accurate attendance records.





## Technologies Used

 - Django
 - Resquests(Python library) 
 - HTML
 - CSS
 - JS


## Database

The application uses MongoDB as a cloud or atlas database to store and manage the notes data.


## Getting Started

- To run this application on your local machine, you need to follow the steps given below:
To deploy this project run

```bash
  git clone https://github.com/tanveer188/zingooo.git

```
- Install dependencies
```
cd zingooo-main
pip install -r requirements.txt
```
- Configure the Database

    - Create a free account on MongoDB Atlas and set up a new cluster.
    - Create a new database in the cluster and add a new user with read and write access.
    - Update the database details in the settings.py file of the application.
- Run the application
```
python manage.py runserver
````
The application will be running on http://localhost:8000.

**Note:** Due to changes in the university's website, this project is no longer being actively maintained and may not work as intended.
