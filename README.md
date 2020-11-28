# Maltreba API

## Brief Explanation
This is API is one one of  Algoritma's Python for Data Analysis Capstone Project. This project aims to create a simple API to fetch data from Heroku Server.
This API App provides Chinook Store’s data consolidated from worldwide stores. This API granted data to be accessed by public for education purpose only.
This API runs on python platform by using certain packages such as pandas and flask which also supported by SQLite database engine.

## Dependencies 
* Pandas
* Flask
* Gunicorn
* Requests
* Sqlite3

## Guidelines

I have deployed a simple example on : https://maltreba-api.herokuapp.com Here's the list of its endpoints:
1. **/** , method = GET

    Base Endpoint, returning welcoming template page.
    e.g.  https://maltreba-api.herokuapp.com/

2. **/playlist** , method = GET

    Return full playlist table in JSON format which provide all playlist provided by Chinook Store. e.g. https://maltreba-api.herokuapp.com/playlist
    
3. **/customer/<Country>/<sel_year>**, method = GET
    
    Return all customers based on selected Country and Year then sorted descending by their total spending. Please notice that all country must use capital letter for each word, except United States of America please use USA. e.g. https://maltreba-api.herokuapp.com/customer/USA/2009

4. **/product/<genre_name>/track**, method = GET

    Return all tracks based on selected Genre. Please use capital letter for first word such as Jazz, Blues etc. e.g. https://maltreba-api.herokuapp.com/product/Pop/track

4. **/sales/genre/<sel_year>**, method = GET

    Return number of tracks sold and their dollar amounts on selected year and group by track’s genre.  e.g. https://maltreba-api.herokuapp.com/sales/genre/2010

4. **/sales/<sel_year>**, method = GET
    
    Return total sales for each genre and month for selected year.  e.g. https://maltreba-api.herokuapp.com/sales/2010
