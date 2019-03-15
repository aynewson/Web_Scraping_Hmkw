# import necessary libraries

from flask import Flask, render_template, redirect

from flask_pymongo import PyMongo

import scrape_mars



# create instance of Flask app

app = Flask(__name__)



# Use flask_pymongo to set up mongo connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"

mongo = PyMongo(app)



# create route that renders index.html template and finds documents from mongo

@app.route("/")

def home():



    # Find data

    marsDetails = mongo.db.collection.find()



    # return template and data

    return render_template("index.html", marsDetails=marsDetails)





# Route that will trigger scrape functions

@app.route("/scrape")

def scrape():



    # Run scraped functions

    marsDetails = scrape_mars.scrape_marsDetails()



    #Deleting existing data base

    mongo.db.collection.remove()



    # Insert forecast into database

    mongo.db.collection.insert_one(marsDetails)



    # Redirect back to home page

    return redirect("/", code=302)





if __name__ == "__main__":

    app.run(debug=True)