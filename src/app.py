from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://naiggo:mysql123@naiggo.mysql.pythonanywhere-services.com/naiggo$default'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

# defino la tabla
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

    def validar_fecha_cumpleanio(personas):
        fecha_actual = datetime.now()

        personas_cumplidoras = []

        for persona in personas:
            fecha_cumple = datetime.strptime(persona.fecha_nacimiento, "%Y-%m-%d")

            if (fecha_actual.day == fecha_cumple.day & fecha_actual.month == fecha_cumple.month):
                personas_cumplidoras.append(persona)

        return personas_cumplidoras

#  si hay que crear mas tablas , se hace aqui

with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
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

@app.route('/personas/cumpleactual',methods=['GET'])
def get_Personas_cumple_actual():
    personas_proximas = Persona.query.filter(Persona.dias_restantes.in_([0, 365, 366])).all()
    result = personas_schema.dump(personas_proximas)

    return jsonify(result)

@app.route('/personas/actualizardiasrestantes', methods=['POST'])
def actualizar_dias_restantes():
    personas = Persona.query.all()

    for persona in personas:
        persona.dias_restantes = persona.calcular_dias_para_cumple()

    db.session.commit()

    return personas_schema.jsonify(Persona.query.all())

# programa principal *******************************
if __name__=='__main__':
    app.run(debug=True, port=5010)    # ejecuta el servidor Flask en el puerto 5000


# A very simple Flask Hello World app for you to get started with...
@app.route('/')
def hello_world():
    return 'Hello from Flask!'