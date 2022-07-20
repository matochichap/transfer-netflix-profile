# transfer-netflix-profile
A bot that helps you find all the shows you watched and copies it over to another profile by adding to list of movies

Step 1: Go to Account > Profile & Parental Controls > {your profile} > Viewing activity
Step 2: Click Download all at the end of the page (You will get a csv with entries on everytime you click onto a show)
Step 3: Download ChromeDriver at https://chromedriver.chromium.org/downloads
Step 4: Fill in the required variables
Step 5: Run the code

Note:
The bot will automatically choose the first profile to add to.

If you want to add to another profile, under the profile_name variable, change to By.XPATH and get the XPATH from the netflix profile page.
Look up at here on how to do this https://stackoverflow.com/questions/3030487/is-there-a-way-to-get-the-xpath-in-google-chrome

If you don't want to add all the movies in, you can edit formatted_netflix_movies.csv in excel, comment out the format_netflix_csv and run the code.
