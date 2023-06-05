from flask import Flask, request, jsonify, send_from_directory, session
import mysql.connector
import os
import random
from datetime import datetime

app = Flask(__name__)

secret_key = os.urandom(24).hex()
# 

app.config['SECRET_KEY'] = secret_key  # Replace with a secure secret key


# Conexion con MySQL
mydb = mysql.connector.connect(
	host="localhost",
	user="CtrlAccess",
	passwd="gadgets",
	database="iotserver"
)
mycursor = mydb.cursor()

# Define a dictionary to store account data
accounts = {}
# insert mysql
def insertMysql(sql):
    mycursor.execute(sql)
    mydb.commit()

        

# Serve static files
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Query the database to check credentials
    query = "SELECT * FROM usersSisFinan WHERE user_name = %s AND password = %s"
    values = (username, password)
    mycursor.execute(query, values)
    result = mycursor.fetchone()

    if result:
        # Redirect to home.html if login is successful
        session['username'] = username
        return jsonify({'message': 'home.html'}), 201
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# Create account endpoint
@app.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    query = "insert into clientesSisFinan set nombres = '{}', apellidos = '{}', cedula = '{}', direccion = '{}', fecha_nacimiento = '{}', telefono = '{}', correo = '{}', nacionalidad = '{}', situacion_laboral = '{}', ingresos = {}".format(data['name'],data['lastname'],data['documentId'],data['address'],data['date'],data['phone'],data['email'],data['nationality'],data['employmentSituation'],data['income'])
    insertMysql(query)
    
    query = "select id_cliente from clientesSisFinan where cedula = '{}' order by id_cliente desc limit 1".format(data['documentId'])
    
    mycursor.execute(query)
    result = mycursor.fetchall()
    id_cliente = result[0][0]
    numeroCuenta = ""

    for _ in range(3):
        numero_aleatorio = random.randint(1000, 9999)
        numeroCuenta += str(numero_aleatorio) + "-"

    numeroCuenta += str(random.randint(1000, 9999))

    query = "insert into cuentasSisFinan set numero_cuenta = '{}', tipo_cuenta = '{}', valor_actual = {}, clave = '{}', id_cliente = {}".format(numeroCuenta,"ahorros",data['initialValue'],data['password'],id_cliente)
    insertMysql(query)
    
    return jsonify({'message': "cuenta creada satisfactoriamente"}), 201

# Consult account endpoint
@app.route('/consultAccount', methods=['POST'])
def consult_account():
    data = request.get_json()
    query = "select c.nombres, c.apellidos, c.cedula, csf.tipo_cuenta, csf.estado from clientesSisFinan c, cuentasSisFinan csf where csf.numero_cuenta = '{}' and c.id_cliente = csf.id_cliente".format(data['accountNumber'])
       
    mycursor.execute(query)
    result = mycursor.fetchall()

    if result:
        nombre = result[0][0]
        apellido = result[0][1]
        documento = result[0][2]
        tipoCuenta = result[0][3]
        estadoCuenta = result[0][4]
        datos = {
            "nombre": nombre,
            "apellido": apellido,
            "documento": documento,
            "tipoCuenta": tipoCuenta,
            "estadoCuenta": estadoCuenta,
        }
        message = "success"
    else:
        message = "error"
        datos = "Numero de cuenta no existe"
        
    
    
    return jsonify({'message': message, 'data': datos}), 201

# Consign to an account
@app.route('/consign', methods=['POST'])
def consign():
    data = request.get_json()
    query = "select id_cuenta, valor_actual from cuentasSisFinan where numero_cuenta = '{}'".format(data['accountNumber'])
       
    mycursor.execute(query)
    result = mycursor.fetchall()
    
    if result:
        id_cuenta = result[0][0]
        valor_actual = float(result[0][1])
        nuevo_valor = valor_actual + float(data['valueConsign'])
        fechaActual = datetime.now()
        fecha = fechaActual.strftime("%Y-%m-%d %H:%M:%S")
        query = "UPDATE cuentasSisFinan SET valor_actual ={} WHERE numero_cuenta ='{}'".format(nuevo_valor, data['accountNumber'])
        insertMysql(query)
        comentario = str(data['name']) + ' ' + str(data['documentId']) + " ha consignado"
        query = "insert into historial_transaccionesSisFinan set id_cuenta = {}, fecha_movimiento = '{}', tipo_movimiento = '{}', cantidad = {}, valor_anterior = {}, nuevo_valor = {}, comentarios = '{}'".format(id_cuenta,fecha,"Consignacion",data['valueConsign'],valor_actual,nuevo_valor,comentario)
        insertMysql(query)

        message = "success"
        datos = "Consignacion realizada"
    else:
        message = "error"
        datos = "Hubo un error en el numero de cuenta"

    
    return jsonify({'message': message, "data":datos}), 200
    

# Withdraw from an account
@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    query = "select id_cuenta, valor_actual from cuentasSisFinan where numero_cuenta = '{}'".format(data['accountNumber'])
       
    mycursor.execute(query)
    result = mycursor.fetchall()
    
    if result:
        id_cuenta = result[0][0]
        valor_actual = float(result[0][1])
        nuevo_valor = valor_actual - float(data['valueRetirar'])
        fechaActual = datetime.now()
        fecha = fechaActual.strftime("%Y-%m-%d %H:%M:%S")
        if nuevo_valor < 0:
            message = "error"
            datos = "Saldo insuficiente"
            comentario = "Retiro fallido saldo insuficiente"
            query = "insert into historial_transaccionesSisFinan set id_cuenta = {}, fecha_movimiento = '{}', tipo_movimiento = '{}', cantidad = {}, valor_anterior = {}, nuevo_valor = {}, comentarios = '{}'".format(id_cuenta,fecha,"Retiro fallido",data['valueRetirar'],valor_actual,valor_actual,comentario)
            insertMysql(query)
        else:
            query = "UPDATE cuentasSisFinan SET valor_actual ={} WHERE numero_cuenta ='{}'".format(nuevo_valor, data['accountNumber'])
            insertMysql(query)
            comentario = "Retiro realizado por " + str(data['valueRetirar'])
            query = "insert into historial_transaccionesSisFinan set id_cuenta = {}, fecha_movimiento = '{}', tipo_movimiento = '{}', cantidad = {}, valor_anterior = {}, nuevo_valor = {}, comentarios = '{}'".format(id_cuenta,fecha,"Retiro",data['valueRetirar'],valor_actual,nuevo_valor,comentario)
            insertMysql(query)

            message = "success"
            datos = "Retiro realizado"
        
    else:
        message = "error"
        datos = "Hubo un error en el numero de cuenta"
    
    return jsonify({'message': message, 'data':datos}), 200
        
# Check balance
@app.route('/balance', methods=['POST'])
def check_balance():
    data = request.get_json()
    query = "select valor_actual from cuentasSisFinan where numero_cuenta = '{}'".format(data['accountNumber'])
       
    mycursor.execute(query)
    result = mycursor.fetchall()
    
    if result:
        valor_actual = result[0][0]
        message = "success"
        datos = valor_actual
    else:
        message = "error"
        datos = "Hubo un error en el numero de cuenta"

    return jsonify({'message': message, 'data': datos}), 200
    


if __name__ == '__main__':
    app.run(port=8080)
