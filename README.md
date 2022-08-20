# MovieSieve

Desktop application developed using python-eel and svelte, which lets you filter movies from any folder of your choice, on the basis of genre.

![MovieSieve](https://github.com/mochatek/MovieSieve/blob/master/Screenshot.PNG)

## Prerequisites

- Movie name should be in the format **`Name (Year)`**
- Internet connection is required for setting up movies in a folder for the first time.

## User Manual

- Choose movie directory by clicking the `Browse 📁` button in the toolbar
- Wait till details for all the movies in the selected directory is retreived
- Once the details are fetched, movies will be listed on the left sidebar
- Click any movie to see its details
- Use the `Filter Dropdown` to filter movies by genre
- To search movies by name/year, use the `Search `
- Movies, for which details were unavailable will be in `red` color
- Click the movie to add its details manually
- Use the `Import ⬇️` button in toolbar to import data from MovieSieve(.ms) file
- Use the `Export ⬆️` button in toolbar to export data into MovieSieve(.ms) file

## Installation Guide

- Install the necessary libraries by running the command `pip install -r requirements.txt`
- cd into UI folder and install the dependancies through `npm install`
- Compile the svelte app by running the command `npm run build`
- Launch the application by running the file `MovieSieve.py`
- Refer [Eel](https://github.com/ChrisKnott/Eel) to understand the working and for packaging info.
