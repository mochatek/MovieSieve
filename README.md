# MovieSieve
Desktop application developed using python-eel, which lets you filter movies from any folder of your choice, on the basis of genre.


## Prerequisites
- Movie name should be in the format `Name (Year)`
- Internet connection is required for setting up movies in a folder for the first time.

## User Manual
- Choose movie folder by clicking  `Browse`.
- Wait till the details for all the movies in the selected folder is retreived.
- `Logs` will be displayed once the process completes.
- Logs will list the movies whose details were not retrieved.
- Click on `Fix` against any movie to manually add its details.
- Movies whose details were successfully retrieved, will be listed in the main screen.
- Click on any movie from the list, to view it's details.
- Use the Genre combo box for filtering movies.

## Installation Guide
- Install the necessary libraries by running the command `pip install -r requirements.txt`
- Launch the application from the file `MovieSieve.py`
- Refer [Eel](https://github.com/ChrisKnott/Eel) to understand the working and for packaging info.

## Screenshot
![MovieSieve](https://github.com/mochatek/MovieSieve/blob/master/Screenshot.PNG)
