from flask import Flask, request, render_template
import pandas as pd
import sqlite3

app = Flask(__name__) 

 
#home root
@app.route('/')
def homepage():
    return render_template('index.html')

# get all media types sold by store
@app.route('/playlist')
def playlist():
    conn=sqlite3.connect("data/chinook.db")
    data=pd.read_sql_query('SELECT Name FROM playlists',conn)
    return data.to_json()

# get sales filter by year dan country
@app.route('/customer/<country>/<sel_year>')
def topbuyer(country, sel_year):
    conn=sqlite3.connect("data/chinook.db")
    querytop='''select c.FirstName, c.LastName,c.Country,  strftime('%Y', i.InvoiceDate) Year,sum(i.Total) Total
    from invoices i 
    join customers c ON i.CustomerId =c.CustomerId 
    GROUP by c.CustomerId 
    '''
    data=pd.read_sql_query(querytop,conn)
    condition1=data['Year']==sel_year
    condition2=data['Country']==country
    data=data[condition1&condition2]
    return data.to_json()

#get tracks by genre
@app.route('/product/track/<genre_name>', methods=['GET']) 
def get_gtrack(genre_name): 
    conn=sqlite3.connect("data/chinook.db")
    querytrack=''' select t.Name Track,t.Composer Composer ,g.Name Genre
    from tracks t
    join genres g on t.GenreId =g.GenreId '''
    data = pd.read_sql_query(querytrack,conn)
    data = data[data['Genre']==genre_name]
    return (data.to_json())

# mendapatkan data dengan filter nilai <value> pada kolom <column>
@app.route('/sales/<inp_year>', methods=['GET']) 
def get_data_equal(inp_year): 
    conn = sqlite3.connect("data/chinook.db")
    querysales='''SELECT i.*,i.UnitPrice*i.Quantity Sales, t.Name TrackName, g.Name Genre, a.Title Album,i2.InvoiceDate,strftime('%Y', i2.InvoiceDate) Year ,i2.BillingCity ,i2.BillingCountry
    FROM invoice_items i 
    JOIN tracks t ON i.TrackId =t.TrackId 
    JOIN genres g ON t.GenreId =g.GenreId
    JOIN albums a ON t.AlbumId =a.AlbumId
    JOIN invoices i2 on i2.InvoiceId =i.InvoiceId 
    '''
    data = pd.read_sql_query(querysales,conn,parse_dates=['InvoiceDate'])
    data[['Genre','BillingCity','BillingCountry']]=data[['Genre','BillingCity','BillingCountry']].astype('category')
    data['InvoiceMonth']=data['InvoiceDate'].dt.month.astype('str')
    data_pivot=pd.pivot_table(  data=data,
                            index='Genre',
                            columns=['Year','InvoiceMonth'],
                            values='Sales',
                            aggfunc=sum)
    data_tsales=data_pivot.xs(key = inp_year, level='Year', axis=1)
    data_tsales=data_tsales.fillna(0)
    data_tsales
    return (data_tsales.to_json()) 


if __name__ == '__main__':
    app.run(debug=True, port=5000) 
