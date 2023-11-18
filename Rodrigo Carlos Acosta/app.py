from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Cargar el modelo al inicio de la aplicación
model = joblib.load('modelo_riesgo_cardiaco.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener datos del cuerpo de la solicitud POST
        data = request.json

        # Convertir los datos a un DataFrame de pandas (ajusta las columnas según tu modelo)
        features = pd.DataFrame(data, index=[0])
       
        # Realizar la predicción
        prediction = model.predict(features)

        msg = ""

        if prediction[0] == 1:
            msg = 'Tiene riesgo de ataque cardíaco'
        else:
            msg = 'No tiene riesgo de ataque cardíaco'

        # Retornar la respuesta
        return jsonify({'prediccion': msg})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)