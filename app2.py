"""
Examen Unidad III 
Autor: [Rosales Garcia Oscar]
Fecha: [29/10/2025]

Descripción:
Objetivo del examen
Desarrollar una API básica con Flask que permita:

Crear un diccionario de dispositivos de red.
Agregar nuevos dispositivos.
Modificar dispositivos existentes.
Mostrar un listado de todos los dispositivos en formato HTML, 
donde cada dispositivo se muestre en un <div> con nombre, 
descripción y características

Requisitos técnicos

Usar Flask.
Usar un diccionario como estructura principal de almacenamiento.
Implementar al menos tres rutas:

GET /dispositivos_html: muestra todos los dispositivos en HTML.
POST /dispositivos: agrega un nuevo dispositivo.
PUT /dispositivos/<id>: modifica un dispositivo existente.

Ejemplo del Diccionario de dispositivos: 
{
  "id": "router01",
  "nombre": "Router Principal",
  "descripcion": "Router de borde para salida a Internet",
  "ip": "192.168.1.1",
  "mac": "00:1A:2B:3C:4D:5E",
  "ubicacion": "Sala de servidores",
  "tipo": "Router",
  "otros": ""
}

Recuerda tener al menos 3 commits en tu repositorio. 

Para puntos extra
Puedes ocupar css para añadir puntos a tu examen, perzonalizalo con estilos como el siguiente:
<style>
    .dispositivo {
        border: 1px solid #ccc;
        padding: 10px;
        margin: 10px;
    }
</style>

Puntos extra para añador formula en el cmapo de otros
la formula es la siguente: 

último octeto de la IP * 3 + longitud del nombre del dispositivo + ":" + nombre (Cambiando los espacios por _)

"""

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# Diccionario para almacenar los dispositivos
dispositivos = {
}

# Plantilla HTML sencilla
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Dispositivos de Red</title>
</head>
<body>
    <h1>Dispositivos de Red</h1>
    
    {% for dispositivo in dispositivos %}
    <div style="border: 1px solid #ccc; margin: 10px; padding: 10px;">
        <h3>{{ dispositivo.nombre }}</h3>
        <p><strong>ID:</strong> {{ dispositivo.id }}</p>
        <p><strong>Descripción:</strong> {{ dispositivo.descripcion }}</p>
        <p><strong>IP:</strong> {{ dispositivo.ip }}</p>
        <p><strong>MAC:</strong> {{ dispositivo.mac }}</p>
        <p><strong>Ubicación:</strong> {{ dispositivo.ubicacion }}</p>
        <p><strong>Tipo:</strong> {{ dispositivo.tipo }}</p>
        {% if dispositivo.otros %}
        <p><strong>Otros:</strong> {{ dispositivo.otros }}</p>
        {% endif %}
    </div>
    {% endfor %}
</body>
</html>
"""

#Para probar que si hay respuesta
@app.route('/', methods=['GET'])
def test():
    return "Hola mundo"

#Funcion para mostrar un listado de los dispositivos
@app.route('/dispositivos', methods=['GET'])
def mostrar_dispositivos_html():
    dispositivos_lista = list(dispositivos.values())
    return render_template_string(html, dispositivos=dispositivos_lista,)

@app.route('/agregarDisp', methods=['POST'])
def agregar_dispositivo():
    datos = request.get_json()

    print("Datos recibidos", request.json)

    if not datos or 'id' not in datos:
        return jsonify({"error": "El campo 'id' es requerido"}), 400
    
    dispositivo_id = datos['id']
    
    if dispositivo_id in dispositivos:
        return jsonify({"error": f"El dispositivo con ID '{dispositivo_id}' ya existe"}), 400
    
    # Crear nuevo dispositivo
    nuevo_dispositivo = {
        "id": dispositivo_id,
        "nombre": datos.get('nombre', ''),
        "descripcion": datos.get('descripcion', ''),
        "ip": datos.get('ip', ''),
        "mac": datos.get('mac', ''),
        "ubicacion": datos.get('ubicacion', ''),
        "tipo": datos.get('tipo', 'Desconocido'),
        "otros": datos.get('otros', '')
    }
    
    dispositivos[dispositivo_id] = nuevo_dispositivo
    return jsonify({
        "mensaje": "Dispositivo agregado exitosamente",
        "dispositivo": nuevo_dispositivo
    }), 201


@app.route('/dispositivos/<dispositivo_id>', methods=['PUT'])
def modificar_dispositivo(dispositivo_id):
    datos = request.get_json()
    
    if dispositivo_id not in dispositivos:
        html = "<h1> ID no encontrada </h1>"
        return html
    
    # Actualizar campos
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
        "mensaje": "Dispositivo actualizado exitosamente",
        "dispositivo": dispositivo
    })

if __name__ == '__main__':
    app.run(debug=True)