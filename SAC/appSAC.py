
from flask import Flask,render_template, request,redirect,url_for,flash
from flask_mysqldb import MySQL
from numpy import DataSource
import xlwt



app=Flask(__name__)


#Mysql Connection
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] ='datos123'
app.config['MYSQL_DB'] ='cliente'

mysql= MySQL(app)

#Guardar datos seetings
app.secret_key='mysecretkey'
@app.route('/')  # 
def Index():
    
    return render_template('index.html')  # cada vez que el usuario visite la ruta inicial


@app.route('/data', methods=['POST'])
def data():
    if request.method=='POST':
        
        NumeroCC= request.form.get('NumeroCedula')
        print("Numero de Cedula es " +NumeroCC)
        cur=mysql.connection.cursor()
        #sql_query="select * form clientes_informacion where Numero_Doc = (%s) "
        cur.execute( "SELECT * FROM clientes_informacion WHERE Numero_Doc LIKE %s", [NumeroCC] )
        #cur.execute(sql_query,NumeroCC)
        #cur.execute('SELECT * FROM clientes_informacion  (%s) ',(NumeroCC,))
        mysql.connection.commit()
        datos=cur.fetchall()
        print(datos)
       

    return render_template('index.html',contacts=datos) 

app.route('/download',methods=['POST'])
def download_report():
    if request.method=='POST':
        workbook=xlwt.Workbook()
        sh=workbook.add_sheet('Reporte informacion cliente')
        sh.write(0,0,'Documento')
        sh.write(0,1,'Nombre')
        sh.write(0,2,'Apellido')
        sh.write(0,2,'Correo')
        sh.write(0,2,'Celular')
        NumeroCC= request.form.get('NumeroCedula')
        cur=mysql.connection.cursor()
            #sql_query="select * form clientes_informacion where Numero_Doc = (%s) "
        cur.execute( "SELECT * FROM clientes_informacion WHERE Numero_Doc LIKE %s", [NumeroCC] )
        #cur.execute(sql_query,NumeroCC)
        #cur.execute('SELECT * FROM clientes_informacion  (%s) ',(NumeroCC,))
        mysql.connection.commit()
        datos=cur.fetchall()
        id=0
        for row in datos:
            sh.write(id+1,0,row(1))
            id+=1
    return render_template('index.html',contacts=datos)


    
if __name__=='__main__':
    app.run(port=300,debug =True)   #iniciar un servidor
