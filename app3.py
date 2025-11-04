from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# Diccionario para almacenar los dispositivos
dispositivos = {
}

html = """
<html>
    <head>
        <tittle>Dispositivos de red</tittle>
    </head>
    <body>
        <h1> Dispositivos de red </h1>

        {% for dispositivo in dispositivos %}
        <div style="border: 1px solid #ccc; margin: 10px">
            <h3>{{ dispositivo.nombre }}</h3>
            <p><strong>ID:</strong> {{ dispositivo.id }}</p>
            <p><strong>Descripcion:</strong> {{ dispositivo.descripcion }}</p>
            <p><strong>Ip:</strong> {{ dispositivo.ip }}</p>
            <p><strong>Mac:</strong> {{ dispositivo.mac }}</p>
            <p><strong>Ubicacion:</strong> {{ dispositivo.ubicacion }}</p>
            <p><strong>Tipo:</strong> {{dispositivo.tipo}}</p>
            <p><strong>Otros:</strong> {{dispositivo.otros}}</p>
        </div>
        {% endfor %}
    </body>
</html>

"""

#Funcion para mostrar listado
@app.route('/dispositivos', methods=['GET'])
def mostrar_dispo():
    dispositivo_lista = list(dispositivos.values())
    return render_template_string(html, dispositivos=dispositivo_lista)

@app.route('/agregarDisp', methods=['POST'])
def agregar_disp():
    datos = request.get_json()

    print("Datos recibidos: ", request.json)

    dispositivo_id = datos['id']

    if dispositivo_id in dispositivos:
        return jsonify({"error": f"El dispositivo con ID '{dispositivo_id}' ya existe"}), 400

    #crear un nuevo dispositivo
    nuevo_dispositivo = {
        "id": datos.get('id', ''),
        "nombre": datos.get('nombre', ''),
        "descripcion": datos.get('descripcion', ''),
        "ip": datos.get('ip', ''),
        "mac": datos.get('mac', ''),
        "ubicacion": datos.get('ubicacion', ''),
        "tipo": datos.get('tipo', ''),
        "otros": datos.get('otros', '')
    }

    dispositivo_id = datos['id']

    dispositivos[dispositivo_id] = nuevo_dispositivo

    return jsonify({
        "mensaje": "Dispositivo añadido",
        "dispositivo": nuevo_dispositivo
    })

@app.route('/dispositivos/<dispositivo_id>', methods=['PUT'])
def modificar(dispositivo_id):
    datos = request.get_json()

    if dispositivo_id not in dispositivos:
        html = "<h1> Id no encontrada </h1>"
        return html
    
    dispositivo = dispositivos[dispositivo_id]

    if 'nombre' in datos:
        dispositivo['nombre'] = datos['nombre']
    if 'descripcion' in datos:
        dispositivo['descripcion'] = datos['descripcion']
    if 'ip' in datos:
        dispositivo['ip'] = datos['ip']
    if 'mac' in datos:
        dispositivo['mac'] = datos['mac']
    if 'ubicacion' in datos:
        dispositivo['ubicacion'] = datos['ubicacion']
    if 'tipo' in datos:
        dispositivo['tipo'] = datos['tipo']
    if 'otros' in datos: 
        dispositivo['otros'] = datos['otros']
    
    return jsonify({
        "mensaje": "Dispositivo actualizado",
        "dispositivo": dispositivo
    })

if __name__ == '__main__':
    app.run(debug=True)