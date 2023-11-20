from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore




# Inicializar Firebase Admin con tus credenciales
cred = credentials.Certificate('credenciales.json')
firebase_admin.initialize_app(cred)

# Obtener referencia a la base de datos
db = firestore.client()

app = Flask(__name__)

# Cargar el modelo al inicio de la aplicación
model = joblib.load('modelo_riesgo_cardiaco.joblib')

from openai import OpenAI

from openai import OpenAI

def generar_recomendacion(datos_usuario):
    try:
        # Configuración de la API Key
        client = OpenAI(api_key='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')

        # Uso optimizado de max_tokens
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Generar recomendaciones breves de salud para un paciente con estos datos: {datos_usuario}"
                }
            ],
            model="gpt-3.5-turbo",
            max_tokens=30  # Reducido para minimizar costos
        )

        # Extracción y devolución del texto generado
        return chat_completion['choices'][0]['message']['content'].strip()
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
        print(data)
        # Realizar la predicción
        prediction = model.predict(features)
        # Convertir la predicción a una respuesta legible
        prediction_label = 'Riesgo de ataque cardíaco' if prediction[0] == 1 else 'Sin riesgo de ataque cardíaco'
        prediction_value = int(prediction[0])
        recomendacion = generar_recomendacion(data)
        print(recomendacion)
        # Guardar en Firebase
        doc_ref = db.collection('predictions').document()
        # Guardar en Firebase junto con la predicción
        doc_ref.set({
            'nombre_usuario': nombre_usuario,
            'prediction': prediction_value,
            'prediction_label': prediction_label,
            'recomendacion': recomendacion  
            })
        #Enviar la respuesta al usuari
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
        # Consulta a Firebase
        predictions = db.collection('predictions').where('nombre_usuario', '==', nombre_usuario).get()
        if predictions:
            # Suponiendo que solo quieres la última predicción
            ultima_prediccion = predictions[-1].to_dict()
            return render_template('resultados_consulta.html', resultado=ultima_prediccion)
        else:
            return render_template('resultados_consulta.html', resultado={'error': 'No se encontraron resultados para el usuario'})
    except Exception as e:
        return render_template('resultados_consulta.html', resultado={'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)