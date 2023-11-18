'''Para la creacion del api utilizaremos el formato de paciente nuevo, el cual se identificara con id
el cual sera unico para cada uno, y utilizando el modelo de prediccion '''
import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Cargar el modelo al inicio de la aplicación
model = joblib.load('modelo_riesgo_cardiaco.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener datos del cuerpo de la solicitud POST
        data = request.get_json(force=True)

        # Realizar la predicción utilizando el modelo cargado
        result = predict_heart_disease(model, data)

        # Devolver el resultado como JSON
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
