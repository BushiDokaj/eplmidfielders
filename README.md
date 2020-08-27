Welcome to my analysis of the best Premier League midfielders!

I wanted to do a project where I combine data analytics and my love of soccer. So I decided
to create this site.

The website:
The site has two main pages:
- a profile page where each players individual data is displayed in tables with some summary statistics
- a visualization dashboard where players are compared using graphs

The code:
The most interesting part of this project (in my opinion) is the code in the data folder.

data_collection.py - here I used Selenium and BeatifulSoup to scrape data from the Premier League website
adn pandas to store that data in csv files.

data_aggregate.py - here I use pandas to clean, process, and manipulate the data to create the data, statistics and data frames I need to power the site

data_visualizations.py - here I use bokeh to create nice interactive graphs that display player data for easy comparison

The rest of the code is mainly standard flask dev and front-end stuff.

Thanks for visiting!