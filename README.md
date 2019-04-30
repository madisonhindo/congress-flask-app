# Congressional Flask App

## What I Built
I created an app using Flask to help people learn about camapaign finance and members of Congress. Users can select a state and learn about how much money was spent in the 2018 midterms in that state. They will also see a list of representatives from that state, and they can learn more about each representative by clicking on his or her name.

## How I Built It
I started this project by using Beautiful Soup scrape [congress.gov](https://www.congress.gov/members?q=%7B%22congress%22%3A116%7D) for information about each member of Congress, which I wrote into a CSV file. Then I scraped [OpenSecrets](https://www.opensecrets.org/states/) to get information about each state and wrote it into a CSV file.

Once I finished scraping, I started creating a Flask app to display the information. I used a function to create my two CSVs into dictionaries to store the data and created a select menu using Bootstrap and Flask-WTF so users could choose a state to learn about. I created templates to display the information for states and representatives. Once the app was functional, I used Bootstrap and CSS to style it.
