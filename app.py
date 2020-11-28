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
@app.route('/customer/<Country>/<sel_year>')
def topbuyer(Country, sel_year):
    conn=sqlite3.connect("data/chinook.db")
    querytop='''select c.FirstName, c.LastName,c.City, c.Country Country,  strftime('%Y', i.InvoiceDate) Year,sum(i.Total) Total
    from invoices i 
    join customers c ON i.CustomerId =c.CustomerId 
    GROUP by c.CustomerId, c.FirstName, c.LastName,c.Country,Year
    '''
    data=pd.read_sql_query(querytop,conn)
    condition1=data['Year']==str(sel_year)
    condition2=data['Country']==Country
    data=data[condition1&condition2].sort_values(by='Total', ascending=False)
    return data.to_json()

#get tracks by genre
@app.route('/product/<Genre_name>/track', methods=['GET']) 
def get_gtrack(Genre_name): 
    conn=sqlite3.connect("data/chinook.db")
    querytrack=''' select t.Name Track,t.Composer Composer, t.Milliseconds, t.Bytes, g.Name Genre
    from tracks t
    join genres g on t.GenreId =g.GenreId '''
    data = pd.read_sql_query(querytrack,conn)
    data = data[data['Genre']==Genre_name]
    return (data.to_json())

#get Total Sales by Genre and Year
@app.route('/sales/genre/<sel_year>', methods=['GET']) 
def sales_genre(sel_year): 
    conn=sqlite3.connect("data/chinook.db")
    querysales2=''' 
    select t.Name Track, g.Name Genre,  strftime('%Y', i.InvoiceDate) Year, ii.UnitPrice *ii.Quantity Total
    from invoice_items ii 
    left join tracks t ON ii.TrackId =t.TrackId 
    left join genres g on t.GenreId =g.GenreId 
    left join invoices i on ii.InvoiceId =i.InvoiceId 
    '''
    data = pd.read_sql_query(querysales2,conn)
    cond1 = data['Year']==str(sel_year)
    data = data[cond1]
    data = data.groupby('Genre').agg({'Track':'count', 'Total': 'sum'})
    return (data.to_json())


# get total sales multi index (year and month ) and genre in index
@app.route('/sales/<sel_year>', methods=['GET']) 
def sales_year(sel_year): 
    conn = sqlite3.connect("data/chinook.db")
    querysales='''SELECT i.*,i.UnitPrice*i.Quantity Sales, t.Name TrackName, g.Name Genre, a.Title Album,i2.InvoiceDate,strftime('%Y', i2.InvoiceDate) Year ,i2.BillingCity ,i2.BillingCountry
    FROM invoice_items i 
    JOIN tracks t ON i.TrackId =t.TrackId 
    JOIN genres g ON t.GenreId =g.GenreId
    JOIN albums a ON t.AlbumId =a.AlbumId
    JOIN invoices i2 on i2.InvoiceId =i.InvoiceId 
    ''' ##
    data = pd.read_sql_query(querysales,conn,parse_dates=['InvoiceDate'])
    data[['Genre','BillingCity','BillingCountry']]=data[['Genre','BillingCity','BillingCountry']].astype('category')
    data['InvoiceMonth']=data['InvoiceDate'].dt.month.astype('str')   
    data_pivot=pd.pivot_table(  data=data,
                            index='Genre',
                            columns=['Year','InvoiceMonth'],
                            values='Sales',
                            aggfunc=sum)
    data_tsales=data_pivot.xs(key = sel_year, level='Year', axis=1)
    data_tsales=data_tsales.fillna(0)
    data_tsales
    return (data_tsales.to_json()) 


if __name__ == '__main__':
    app.run(debug=True, port=5000) 