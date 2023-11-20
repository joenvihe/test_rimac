from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from openai import OpenAI
import pybreaker

# Crear un circuit breaker Debido a que necesitamos el acceso a internet para un openai key
# para evitar futuros fallos
breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=10)

# Inicializamos el Firebase Admin  con las credenciales brindadas por la aplicacion
cred = credentials.Certificate('credenciales.json')
firebase_admin.initialize_app(cred)

# Obtener referencia a la base de datos
db = firestore.client()
#Iniciamos framework flask
app = Flask(__name__)

# Cargar el modelo de aprendisaje realizado en el jupiter con base en el problema brindado
model = joblib.load('modelo_riesgo_cardiaco.joblib')
#Generamos la recomendacion que nos brindara el openai en base a los datos que seran ingresados
def generar_recomendacion(datos_usuario):
    try:
        # Configuración de la API Key
        client = OpenAI(api_key='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')
        #Generamos el prompt para pedir recomiendaciones basados en la data que nos brindan
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Generar recomendaciones  de maximo 30 palabras diferentes  y breves de salud para un paciente con  {datos_usuario}"
                }
            ],
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=30
        )

        # Extracción y devolución del texto generado
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error al generar recomendación: {e}")
        return None




@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        #Nombre de usuario inicial
        nombre_usuario = request.form['nombre_usuario']
        # Validar y obtener datos del formulario
        data = {
            'Age': int(request.form['Age']),
            'Sex': request.form['Sex'],
            'ChestPainType': request.form['ChestPainType'],
            'RestingBP': int(request.form['RestingBP']),
            'Cholesterol': int(request.form['Cholesterol']),
            'FastingBS': int(request.form['FastingBS']),
            'RestingECG': request.form['RestingECG'],
            'MaxHR': int(request.form['MaxHR']),
            'ExerciseAngina': request.form['ExerciseAngina'],
            'Oldpeak': float(request.form['Oldpeak']),
            'ST_Slope': request.form['ST_Slope']
        }

        
        # Validar que todos los campos necesarios estén presentes
        required_fields = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']
        if not all(field in data for field in required_fields):
            raise ValueError("Todos los campos son requeridos")
        
        # Convertir los datos a un DataFrame de pandas
        features = pd.DataFrame([data])
        
        # Realizar la predicción
        prediction = model.predict(features)
        # Convertir la predicción a una respuesta legible
        prediction_label = 'Riesgo de enfermedad cardíaca' if prediction[0] == 1 else 'Sin riesgo de enfermedad cardíaca'
        prediction_value = int(prediction[0])
        recomendacion = generar_recomendacion(prediction_label)
    
        # Guardar en Firebase que se encuentra en la nube para mantener a los usuarios
        doc_ref = db.collection('predictions').document()
        # Guardar en Firebase junto con la predicción
        doc_ref.set({
            'nombre_usuario': nombre_usuario,
            'prediction': prediction_value,
            'prediction_label': prediction_label,
            'recomendacion': recomendacion  
            })
        #Enviar la respuesta al usuario
        return render_template('result.html', result={'prediction_label': prediction_label})
    except Exception as e:
        # Registrar el error
        print(f"Error al procesar la solicitud: {e}")
        # Enviar una respuesta de error
        return jsonify({'error': f"Error al procesar la solicitud: {e}"}), 400
    
@app.route('/consultar_resultados', methods=['POST'])
def consultar_resultados():
    try:
        nombre_usuario = request.form['nombreUsuarioConsulta']
        usuario_existente = db.collection('usuarios').document(nombre_usuario).get().exists
        if usuario_existente:
            return 'Usuario ya registrado', 400 
        else:
        # Consulta a Firebase
            predictions = db.collection('predictions').where('nombre_usuario', '==', nombre_usuario).get()
            if predictions:
            # Coloca la prediccion que en este caso seria la unica que hay o la ultima
             ultima_prediccion = predictions[-1].to_dict()
             return render_template('resultados_consulta.html', resultado=ultima_prediccion)
            else:
             return render_template('resultados_consulta.html', resultado={'error': 'No se encontraron resultados para el usuario'})
    except Exception as e:
        return render_template('resultados_consulta.html', resultado={'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)