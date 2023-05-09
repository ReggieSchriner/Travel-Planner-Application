# soft161_milestone_2



## The tracking apps and descriptions

1. Travel Planner App

2. Package Deal Tracker App - This app allows the user to add venues to a database, with corresponding coordinates, name, and type, as well as operators and their corresponding name and score. The app also allows the user to edit these values at any time. Also, the user can access the forecast of any venue on the forecasts screen, but forecasts only extend out up to five days. Furthermore, the app allows the user to add reviews for the venues and the operators, which are stored in the database for use in the travel planner app. Lastly, the app has a review itinerary screen where the user can choose their prefered itinerary from two options given by the travel planner app.

3. Entertainment Tracker App

## App status

1. Travel Planner App

2. Package Deal Tracker App - The app is almost mostly functional, only missing the review itinerary screen, with no known bugs. The app works perfectly with the database and add/pull information as expected. The only part of the functionality that needs to be added is the review itinerary screen. Furthermore, the app has multiple test cases that test the use of the database, all of which pass. The only methods that do not have tests are the submit_score and review_itinerary methods. 

3. Entertainment Tracker App

## Instructions for running each app

1. Travel Planner App

2. Package Deal Tracker App

    First, in order to use the application the user must have a MySQL server set up with their own password.
    Instructions for this can be found here: https://computing.unl.edu/faq-section/working-remotely/#node-302

    Next, create a file called 'credentials.json' in the same folder and enter the following dictionary with your 
    user credentials filled in where the varibles are surrounded with < > (be sure to enter them as strings 
    sourrounded with ""): 
    {"authority":"cse.unl.edu", "port":3306,"database":<databse>,"username":<username>,"password":<password>}.

    Then open the app folder in PyCharm and locate the installer file (not the test installer). Run 
    the installer and make sure the tables and database are created. This is shown by the print statements that 
    should be given after the file is used. 
    
    After running the installer, creating the database, and adding your credentials, the main app can be used by 
    running the main.py file. Then the GUI can be used to interact with and access the rest of the app. 

    In order to make the tests function, create a database called 'deals_test' by using the command: 'mysql 
    --protocol=TCP --port=3306 --user=root -p' in you terminal and then typing the password. Then type 'create
    database deals_test' to create the database so that the unit tests can run and store information.
    Then to use the unit tests, run the test_installer.py file and then the tests.py file will function as 
    expected. As you will see, all tests are passing and each test check the functionality of the methods that 
    interact with the database by using a local databse to run the tests.

3. Entertainment Tracker App
