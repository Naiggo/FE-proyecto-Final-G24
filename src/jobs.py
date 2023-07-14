import requests
import smtplib
from app import Persona
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class UtilsMail():
    def __init__(self, urlGet="https://naiggo.pythonanywhere.com/personas/cumpleactual"):
        self.urlGet = urlGet

    def send_greetings_email(self, personas):
        # Configurar el servidor SMTP
        smtp_host = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'losmuchachos.codoacodo@gmail.com'
        smtp_password = 'uaitjaewydnqnqtf'

        for persona in personas:
            # Crear el mensaje de correo electrónico
            subject = '¡Feliz cumpleaños y aniversario de bodas!'
            message = f'Estimado/a {persona.nombre},\n\nEn este día especial, queremos desearte un feliz cumpleaños en nombre de todo el equipo de Los Muchachos. Que este nuevo año de vida esté lleno de éxitos, alegrías y oportunidades para alcanzar tus metas.\n\n¡Feliz cumpleaños y que tengas un día maravilloso!\n\nAtentamente, Los Muchachos!'
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = persona.mail
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            # Enviar el correo electrónico
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)

    def calcular_dias_para_cumple(self, fecha_nacimiento):
        fecha_actual = datetime.now()
        fecha_cumple = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
        fecha_cumple = fecha_cumple.replace(year=fecha_actual.year)

        if fecha_actual > fecha_cumple:
            fecha_cumple = fecha_cumple.replace(year=fecha_actual.year + 1)

        dias_restantes = (fecha_cumple - fecha_actual).days
        return dias_restantes

    def persona_mapper(self, item):
        persona = Persona(
            item['nombre'],
            item['apellido'],
            item['mail'],
            item['fecha_nacimiento']
            )
        persona.id=item['id'],
        return persona

    def validar_fecha_cumpleanio(self, personas):
        fecha_actual = datetime.now()
        personas_cumplidoras = []

        for persona in personas:
            fecha_cumple = datetime.strptime(persona.fecha_nacimiento, "%Y-%m-%d")

            if fecha_actual.day == fecha_cumple.day and fecha_actual.month == fecha_cumple.month:
                personas_cumplidoras.append(persona)

        return personas_cumplidoras

# Realiza el job 1
url = 'https://naiggo.pythonanywhere.com/personas/actualizardiasrestantes'
response = requests.post(url)

if response.status_code != 200:
    # La solicitud no fue exitosa, manejar el error apropiadamente
    print('Error al realizar la solicitud:', response.status_code)
else:
    # Realiza el job 2
    utils = UtilsMail()

    response = requests.get(utils.urlGet)

    if response.status_code != 200:
        # La solicitud no fue exitosa, manejar el error apropiadamente
        print('Error al realizar la solicitud:', response.status_code)
    else:
        data = response.json()

        lista_personas = [utils.persona_mapper(item) for item in data]

        if len(lista_personas) > 0:
            personas_cumplidoras = utils.validar_fecha_cumpleanio(lista_personas)

            if len(personas_cumplidoras) > 0:
                utils.send_greetings_email(personas_cumplidoras)