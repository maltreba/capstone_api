from flask import Flask, request, render_template
import pandas as pd
import sqlite3

app = Flask(__name__) 


#home root
@app.route('/')
def homepage():
    return "Welcome"

# get all media types sold by store
@app.route('/playlist')
def playlist():
    conn=sqlite3.connect("data/chinook.db")
    data=pd.read_sql_query('SELECT Name FROM playlists',conn)
    return data.to_json()

# get top 10 buyers from all over the world
@app.route('/customer/top10')
def topbuyer():
    conn=sqlite3.connect("data/chinook.db")
    querytop='''select c.FirstName, c.LastName,c.Country, sum(Total) 
    from invoices i 
    join customers c ON i.CustomerId =c.CustomerId 
    GROUP by c.CustomerId 
    limit 10'''
    data=pd.read_sql_query(querytop,conn)
    return data.to_json()

#get tracks by genre
@app.route('/album/track/<genre_name>/', methods=['GET']) 
def get_gtrack(genre_name): 
    conn=sqlite3.connect("data/chinook.db")
    querytrack=''' select t.Name Track,t.Composer Composer ,g.Name Genre
    from tracks t
    join genres g on t.GenreId =g.GenreId '''
    data = pd.read_sql_query(querytrack,conn)
    cond = data['Genre']==genre_name
    data =data[cond]
    return (data.to_json())

# mendapatkan data dengan filter nilai <value> pada kolom <column>
@app.route('/sales/<year>/<in_month>', methods=['GET']) 
def get_data_equal(in_year, in_month): 
    conn = sqlite3.connect("data/chinook.db")
    querysales='''SELECT i.*,i.UnitPrice*i.Quantity Sales, t.Name TrackName, g.Name Genre, a.Title Album,i2.InvoiceDate ,i2.BillingCity ,i2.BillingCountry
    FROM invoice_items i 
    JOIN tracks t ON i.TrackId =t.TrackId 
    JOIN genres g ON t.GenreId =g.GenreId
    JOIN albums a ON t.AlbumId =a.AlbumId
    JOIN invoices i2 on i2.InvoiceId =i.InvoiceId 
    '''
    data = pd.read_sql_query(querysales,conn, parse_dates=['InvoiceDate'])
    data['BillingCity']=data['BillingCity'].astype('category')
    data['BillingCountry']=data['BillingCountry'].astype('category')
    data['InvoiceMonth']=data['InvoiceDate'].dt.month_name().astype('category')
    data['InvoiceYear']=data['InvoiceDate'].dt.year
    conn=data['InvoiceYear']==in_year
    data=data[conn]
    data_pivot=pd.pivot_table(
                            data=data,
                            index='Genre',
                            columns=['InvoiceYear','InvoiceMonth'],
                            values='Sales',
                            aggfunc=sum)
    data_tsales=data_pivot.xs(key = in_month, level='InvoiceMonth', axis=1)
    return (data_tsales.to_json()) 


if __name__ == '__main__':
    app.run(debug=True, port=5000) 