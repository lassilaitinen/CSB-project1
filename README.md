# CSB-project1
Project 1 for the MOOC Cyber Security Base -course. This is a simple app where you can post noticed security threats, comment the notices and vote if the notice was good or not. It has some built in security flaws in it.

### Installation instructions:
To use this app, you need to have Django and Python installed. Note that these instructions are for Windows!

1.	Clone the project and move to the folder, where you cloned the project.
    ```
        git clone https://github.com/lassilaitinen/CSB-Project1.git
    ```
2.  Move to the folder where you cloned this application. The following is only an example!
    ```
        cd C:\[username]\secureapp
    ```
3.	Make the needed migrations with following commands:
    ```
        python manage.py makemigrations
    ```
    ```
        python manage.py migrate
    ```
4.	Start the project with following command:
    ```
        python manage.py runserver
    ```
5.	Now the application should be available at your localhost server: http://127.0.0.1:8000/secureapp (note that there is nothing without writing the ‘secureapp’ to the URL).

This application has multiple accounts to use, here is one regular user to use when logging in:

Username: LuckyLuke

Password: wildwest
