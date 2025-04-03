# final_api
Fictional Zoo API

API server: webapi.jessicaamy.com

I had to develop a database and a web API that interfaces with the database I first started with designing an ERD I created a zoo that has many zoos, an enclosure with many animals’ food which only one animal can eat and the animals. It’s a zoo style database API that zoos could use to organize information. This was my original ERD that I used to get feedback.


The feedback was from two different people in the course and was as follows.

Person 1. It isn’t obvious what type of relationships were used as the arrows didn’t have the correct end points which effected the grade of my last assignment so that was useful to know so I updated it and improved the design.

Person 2. Same as above but pointed out that the relationships weren’t described as they should have been, and it was hard to read. This is my final design that I used to create the database layout.


I applied the feedback to my second design by adding relationships I have two types of relationships one to one and one to many I wasn’t sure if I needed to put the zoo_enclosures table into the ERD. It has two tables of enclosure.id and zoo.id and linked those two as a separate table. A zoo can have multiple enclosures and each enclosure has many animals.

Why did I choose postgres and what is the difference between postgres and mongodb, I choose postgres as I understand it better then mongodb. The following differences apply to both databases.

Mongo DB is a noSQL databases and stores information in a json like fashion. It’s perfect for unstructured data that always changes. However, in my case data isn’t always changing and is structured.

PostgreSQL is a rational database it uses schemas to organize and structure data. Its perfect for my use as we can use complex queries and structured data. It also uses the standard SQL language which I’ve used in the past and in other languages such as PHP its simple and easy to understand.

Both have good integration into flask and SQL alchemy, but I went with postgres for these reasons.

A bit about the API. I wrote the API in python with flask for the web server side of things and used SQL alchemy I broke the routes down into many different functions and modified the sample a lot that we used in class to apply to my database. I had the biggest problem with the zoo part of the programming. I had to create a zoo with many enclosures, and I couldn’t get it to work I figured it out when writing it in JSON because I had to access the keys directly inside of other keys so I used one loop for the key and one loop for the value which seems to work and in my json file adding a enclosure key with enclosures. I added a few template json files to help with testing.



I used CRUD to develop the routes we needed one command to create one command to update and one command to delete. The following routers are as follows.

/zoos get, put, patch, delete

/enclosures get, put, patch, delete

/animals get, put, patch, delete,

/food get, put, patch, delete,

Then you add a number to the route if you want to modify or edit data such as zoos/1 with json information as the request.

To help with testing I created some JSON to update the information for the zoos as it was tricky for me to figure out which is what took the most time. A screen shot of a computer program

Description automatically generated

We can update it using a PUT request to zoos with the following json. For updating the other routes all that is needed is the databases keys for example with enclosure we need name species price and zoo id. To create a row in the enclosures we will use the following.


To update it we use the same information but remove the zoo ID and add an ID to the request for example to create a new zoo we just use /zoos but to update the zoo we must do /zoos/zoo_id

To run this program, we must do the following.

Create a virtual environment with the following command: python3 -m venv .venv
Change into the virtual environment: source. venv/bin/activate
Install all the dependences: pip install -r requirements.txt
Now we need to setup the database we do the following.

Create a user in postgres and then the database name in my case I made myself super user.
 CREATE USER jesso  WITH LOGIN SUPERUSER PASSWORD ‘123456’;

Create a database.
Create database zoo.

I created a few test functions to seed and initialize the database for testing. It populates the database with zoos animals and food. Init drops the table completely. I didn’t have the time but I was going to add the weather to the database from another API and update the weather my attempt at doing so was too problematic so I had to drop that idea as part of my development but might make it into newer versions of the project when I want to mess with something.

Flask db init

Flask db seed
