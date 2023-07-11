from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import schedule
import time
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://naiggo:mysql123@naiggo.mysql.pythonanywhere-services.com/naiggo$default'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

# defino la tabla
class Producto(db.Model):   # la clase Producto hereda de db.Model    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    precio=db.Column(db.Integer)
    stock=db.Column(db.Integer)
    imagen=db.Column(db.String(400))
    def __init__(self,nombre,precio,stock,imagen):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.precio=precio
        self.stock=stock
        self.imagen=imagen
        
class Persona(db.Model):   # la clase Persona hereda de db.Model    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    apellido=db.Column(db.String(100))
    mail=db.Column(db.String(100))
    fecha_nacimiento=db.Column(db.String(100))
    dias_restantes=db.Column(db.Integer)
    
    def __init__(self,nombre,apellido,mail,fecha_nacimiento):
        self.nombre=nombre
        self.apellido=apellido
        self.mail=mail
        self.fecha_nacimiento=fecha_nacimiento
        self.dias_restantes=self.calcular_dias_para_cumple()
        
    def calcular_dias_para_cumple(self):
        fecha_actual = datetime.now()
        fecha_cumple = datetime.strptime(self.fecha_nacimiento, "%Y-%m-%d")
        fecha_cumple = fecha_cumple.replace(year=fecha_actual.year)

        if fecha_actual > fecha_cumple:
            fecha_cumple = fecha_cumple.replace(year=fecha_actual.year + 1)

        dias_restantes = (fecha_cumple - fecha_actual).days
        return dias_restantes

#  si hay que crear mas tablas , se hace aqui


with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','precio','stock','imagen')


producto_schema=ProductoSchema()            # El objeto producto_schema es para traer un producto
productos_schema=ProductoSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto


# crea los endpoint o rutas (json)
@app.route('/productos',methods=['GET'])
def get_Productos():
    all_productos=Producto.query.all()         # el metodo query.all() lo hereda de db.Model
    result=productos_schema.dump(all_productos)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla


@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    producto=Producto.query.get(id)
    return producto_schema.jsonify(producto)   # retorna el JSON de un producto recibido como parametro


@app.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    producto=Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)   # me devuelve un json con el registro eliminado

@app.route('/productos', methods=['POST']) # crea ruta o endpoint
def create_producto():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    imagen=request.json['imagen']
    new_producto=Producto(nombre,precio,stock,imagen)
    db.session.add(new_producto)
    db.session.commit()
    return producto_schema.jsonify(new_producto)

@app.route('/productos/<id>' ,methods=['PUT'])
def update_producto(id):
    producto=Producto.query.get(id)
 
    producto.nombre=request.json['nombre']
    producto.precio=request.json['precio']
    producto.stock=request.json['stock']
    producto.imagen=request.json['imagen']

    db.session.commit()
    return producto_schema.jsonify(producto)




class PersonaSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','apellido','mail','fecha_nacimiento', 'dias_restantes')


persona_schema=PersonaSchema()           
personas_schema=PersonaSchema(many=True)


# crea los endpoint o rutas (json)
@app.route('/personas',methods=['GET'])
def get_Personas():
    all_personas=Persona.query.all()         
    result=personas_schema.dump(all_personas)  
                                               
    return jsonify(result)                      


@app.route('/personas/<id>',methods=['GET'])
def get_persona(id):
    persona=Persona.query.get(id)
    return persona_schema.jsonify(persona)


@app.route('/personas/<id>',methods=['DELETE'])
def delete_persona(id):
    persona=Persona.query.get(id)
    db.session.delete(persona)
    db.session.commit()
    return persona_schema.jsonify(persona)

@app.route('/personas', methods=['POST'])
def create_persona():
    nombre=request.json['nombre']
    apellido=request.json['apellido']
    mail=request.json['mail']
    fecha_nacimiento=request.json['fecha_nacimiento']
    new_persona=Persona(nombre,apellido,mail,fecha_nacimiento)
    db.session.add(new_persona)
    db.session.commit()
    return persona_schema.jsonify(new_persona)

@app.route('/personas/<id>' ,methods=['PUT'])
def update_persona(id):
    persona=Persona.query.get(id)
 
    persona.nombre=request.json['nombre']
    persona.apellido=request.json['apellido']
    persona.mail=request.json['mail']
    persona.fecha_nacimiento=request.json['fecha_nacimiento']
    persona.dias_restantes=persona.calcular_dias_para_cumple()
    
    db.session.commit()
    return persona_schema.jsonify(persona) 

@app.route('/personas/proxcumple',methods=['GET'])
def get_Personas_prox_cumple():
    personas_proximas=Persona.query.with_entities(db.func.min(Persona.dias_restantes)).scalar()     
    query = Persona.query.filter(Persona.dias_restantes == personas_proximas).all()
    result = personas_schema.dump(query)
                                               
    return jsonify(result)   

# programa principal *******************************
if __name__=='__main__':
    app.run(debug=True, port=6000)    # ejecuta el servidor Flask en el puerto 5000
     
    
    def actualizar_dias_restantes():
        fecha_actual = datetime.now().date()
        personas = Persona.query.all()

        for persona in personas:
            fecha_cumple = datetime.strptime(persona.fecha_nacimiento, "%d-%m-%Y").date()
            fecha_cumple = fecha_cumple.replace(year=fecha_actual.year)

            if fecha_actual > fecha_cumple:
                fecha_cumple = fecha_cumple.replace(year=fecha_actual.year + 1)

            dias_restantes = (fecha_cumple - fecha_actual).days
            persona.dias_restantes = dias_restantes

        db.session.commit()

    schedule.every().day.at("00:00").do(actualizar_dias_restantes)

    while True:
        schedule.run_pending()
        time.sleep(1)


# A very simple Flask Hello World app for you to get started with...
@app.route('/')
def hello_world():
    return 'Hello from Flask!'