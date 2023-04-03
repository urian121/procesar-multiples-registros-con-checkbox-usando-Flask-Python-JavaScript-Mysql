from flask import Flask, render_template, jsonify
from flask import request  # Importante importar el paquete request
from connBD import *
app = Flask(__name__)


#Mi decorador Home
@app.route('/')
def inicio():
    return render_template('index.html')


#Ruta para el ejemplo 1
@app.route('/ejemplo1', methods=['GET'])
def procesar1():
    return render_template('ejemplos/ejemplo1.html')


@app.route('/procesar-ejemplo1', methods=['POST'])
def procesarExample1():
    frutas = request.form.getlist('frutas[]')
    print(', '.join(frutas))
    return 'Las Frutas seleccionadas son: ' + ', '.join(frutas)
#Fin del ejemplo 1


#Ruta para el ejemplo 2
@app.route('/ejemplo2', methods=['GET'])
def procesar2():
    return render_template('ejemplos/ejemplo2.html')

@app.route('/procesar-ejemplo2', methods=['GET','POST'])
def procesarExample2():
    frutas = request.form.getlist('frutas[]')
    data = 'Frutas seleccionadas: ' + ', '.join(frutas)
    print(data)
    status = {"message": "OK", "data": data}
    return jsonify(status), 200
#Fin del ejemplo 2


@app.route('/ejemplo3', methods=['GET'])
def procesar3():
    conexion_MySQLdb = connectionBD()  # Hago instancia a mi conexion desde la funcion
    mycursor = conexion_MySQLdb.cursor(dictionary=True)

    querySQL = ("SELECT * FROM personas WHERE activo = 1 ")
    mycursor.execute(querySQL)
    listaRegistros = mycursor.fetchall()
    mycursor.close()  # cerrrando conexion SQL
    conexion_MySQLdb.close()  # cerrando conexion de la BD
    return render_template('ejemplos/ejemplo3.html', listaRegistros=listaRegistros)





@app.route('/procesar-personas-seleccionada', methods=['GET','POST'])
def procesarCheckboxPersona():
    if request.method == 'POST':
        # dataId = request.get_json().get('ids')
        idsConsigChecked = request.json.get('ids')
        print(idsConsigChecked)
        for idconsignacion in idsConsigChecked:

            conexion_MySQLdb = connectionBD()  # Hago instancia a mi conexion desde la funcion
            cur = conexion_MySQLdb.cursor(dictionary=True)
            '''
            cur.execute('DELETE FROM personas WHERE id_persona=%s', (idconsignacion,))
            cur.execute('DELETE FROM personas WHERE id_persona IN=%s', (idconsignacion,))
            conexion_MySQLdb.commit()
            '''
    
            cur.execute("""
                UPDATE personas
                SET 
                    activo = %s
                WHERE id_persona =%s
                """, (0, idconsignacion))
            conexion_MySQLdb.commit()
            cur.close()  # cerrando conexion de la consulta sql
            conexion_MySQLdb.close()  # cerrando conexion de la BD
        return jsonify({"idsProcesados": idsConsigChecked})




@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)



if __name__ == "__main__":
    app.run(debug=True, port=8000)
