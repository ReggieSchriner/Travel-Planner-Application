# soft161_milestone_2



## The tracking apps and descriptions

1. Travel Planner App - This app data from the other two apps created and allows the user to plan a trip! The user can log into their database and api using their credentials and are then given multiple options. They can advance the calandar date by one day, validate locations based on cities and airports that were already created, and can update the ratings of the venues that were created. They can also prepare itineraries for their trip.

2. Package Deal Tracker App - This app allows the user to add venues to a database, with corresponding coordinates, name, and type, as well as operators and their corresponding name and score. The app also allows the user to edit these values at any time. Also, the user can access the forecast of any venue on the forecasts screen, but forecasts only extend out up to five days. Furthermore, the app allows the user to add reviews for the venues and the operators, which are stored in the database for use in the travel planner app. Lastly, the app has a review itinerary screen where the user can choose their prefered itinerary from two options given by the travel planner app.

3. Entertainment Tracker App - This app allows users to add venues and cities to a database. The app also allows the user to edit these values at any time. Also, the user can access the forecast of any venue on the forecasts screen, but forecasts only extend out up to five days. Furthermore, the app allows the user to add reviews for the venues and the cities, which are stored in the database for use in the travel planner app. Lastly, the app has a review itinerary screen where the user can choose their prefered itinerary from two options given by the travel planner app.

## App status

1. Travel Planner App - The app is functional but is still incomplete and has bugs. While there was error handling put into place, it isn't showing up or working due to a kivy issue. There is code for updating reviews and for the validate locations page but whether they work or not is hard to determine because of the kivy issue. The itinerary screen also does not have functionality and there are no tests.

2. Package Deal Tracker App - The app is almost mostly functional, only missing the review itinerary screen, with no known bugs. The app works perfectly with the database and add/pull information as expected. The only part of the functionality that needs to be added is the review itinerary screen. Furthermore, the app has multiple test cases that test the use of the database, all of which pass. The only methods that do not have tests are the submit_score and review_itinerary methods. The test coverage can be found in the htmlcov folder inside the package_deal_tracker folder.

3. Entertainment Tracker App - The app is half functional and is not connected to the database, nor is it updated or tested.

## Instructions for running each app

1. Travel Planner App


    First, in order to use the application the user must have a MySQL server set up with their own password.

    Instructions for this can be found here: https://computing.unl.edu/faq-section/working-remotely/#node-302

    Next, create a file called 'credentials.json' in the same folder and enter the following dictionary with your 
    user credentials filled in where the varibles are writtin in italics (be sure to enter them as strings 
    sourrounded with quotations): 

    {"authority":"cse.unl.edu", "port":3306,"database":*database*,"username":*username*,"password":*password*, "weatherauthority": "api.openweathermap.org", "weatherport": "443", "apikey":*apikey*}

    Then open the app folder in PyCharm and locate the installer file. Run 
    the installer and make sure the tables and database are created. 
    
    After running the installer, creating the database, and adding your credentials, the main app can be used by running the main_travel_planner_app.py file. Then the GUI can be used to interact with and access the rest of the app. 

    In order to make the tests function, create a database called 'deals_test' by using the command: 'mysql 
    --protocol=TCP --port=3306 --user=root -p' in your terminal and then typing your password. Then type 'create
    database deals_test' to create the database so that the unit tests can run and store information.
    Then to use the unit tests, run the test_installer.py file and then the tests.py file will function as 
    expected. As you will see, all tests are passing and each test checks the functionality of the methods that 
    interact with the database by using a local databse to run the tests. The only functions that do not have a test
    are the submit_score and review_itinerary methods.

2. Package Deal Tracker App

    First, in order to use the application the user must have a MySQL server set up with their own password.
    Instructions for this can be found here: https://computing.unl.edu/faq-section/working-remotely/#node-302

    Next, create a file called 'credentials.json' in the same folder and enter the following dictionary with your user credentials filled in where the varibles are writtin in italics (be sure to enter them as strings sourrounded with quotations): 

    {"authority":"cse.unl.edu", "port":3306,"database":*databse*,"username":*username*,"password":*password*}

    Then open the app folder in PyCharm and locate the installer file (not the test installer). Run the installer and make sure the tables and database are created. This is shown by the print statements that should be given after the file is used. 
    
    After running the installer, creating the database, and adding your credentials, the main app can be used by running the main.py file. Then the GUI can be used to interact with and access the rest of the app. 

    When you run the main file, only enter your password and apikey on the credentials screen since the rest should already be prepopulated. Then you'll be taken to the main screen where you have the option to advance the calandar date by one day, validate locations based on cities and airports that were already created, or update the ratings of the venues that were created. Since this hasn't been fully fixed, things might functionw well. You should also be able to prepare itineraries but this app isn't fully functional, so it won't really work.

3. Entertainment Tracker App

    First, in order to use the application the user must have a MySQL server set up with their own password.

    Instructions for this can be found here: https://computing.unl.edu/faq-section/working-remotely/#node-302

    Next, create a file called 'credentials.json' in the same folder and enter the following dictionary with your user credentials filled in where the varibles are writtin in italics (be sure to enter them as strings sourrounded with quotations): 

    {"authority":"cse.unl.edu", "port":3306,"database":*database*,"username":*username*,"password":*password*}

    Then open the app folder in PyCharm and locate the installer file. Run the installer and make sure the tables and database are created. 
    
    After running the installer, creating the database, and adding your credentials, the main app can be used by running the main_travel_planner_app.py file. Then the GUI can be used to interact with and access the rest of the app.

