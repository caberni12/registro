
from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Ruta del archivo Excel (ubicación del driver cargado)
EXCEL_FILE = '/mnt/data/pedidos.xlsx'

# Verificar si el archivo Excel existe; si no, crearlo con columnas iniciales
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['nombre', 'direccion', 'telefono', 'observaciones', 'total'])
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/registrar', methods=['POST'])
def registrar_pedido():
    try:
        # Obtener datos del formulario
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        observaciones = request.form.get('observaciones', '')  # Puede estar vacío
        total = request.form['total']

        # Leer el archivo Excel existente
        df = pd.read_excel(EXCEL_FILE)

        # Agregar los nuevos datos como una fila
        nueva_fila = {
            'nombre': nombre,
            'direccion': direccion,
            'telefono': telefono,
            'observaciones': observaciones,
            'total': float(total)
        }
        df = df.append(nueva_fila, ignore_index=True)

        # Guardar los cambios en el archivo Excel
        df.to_excel(EXCEL_FILE, index=False)

        return jsonify({'message': 'Pedido registrado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
