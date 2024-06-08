To run the program:
- Edit src/app.py with the correct database information for your specific database
- In terminal run: python src/app.py
- The app is running

The application is also running on a server right now which you can view by going to:
- https://alex.bils.space/

'Drop all tables' will delete the table with mushrooms.

You can then create the table and insert data again with 'Create Table'

'Show Dataset' displays the table of all mushrooms in the dataset.

In the section 'Input Mushroom Information' you can describe a mushroom.

'Cap Diameter' is a floating point (with a margin of +/- 0.5)
'Cap Shape' takes strings of either [bell, conical, convex, flat, sunken, spherical, others] (with either capital letters or not)
'Cap Surface' takes string of either [fibrous, grooves, scaly, smooth, shiny, leathery, silky, sticky, wrinkled, fleshy] (with either capital letters or not).
'Cap Color' takes string of either [brown, buff, gray, green, pink, purple, red, white, yellow, blue, orange, black]
'Stem Height' is a floating point (with a margin of +/- 0.5)
'Stem Width' is a floating point (with a margin of +/- 0.5).

After submitting you will get a table of mushrooms fitting this description.

The column class will tell you if the mushroom is poisonous (p) or edible (e).

The database operations like insert and delete is handled as buttons when the server is running. 
The Regex part is for the input form of strings to make it less lenient. Where you can, try and input the following data:
- 15.2
- Convex
- grooves
- oRaNge
- 17
- 17

and you should see two rows left after the filtering
