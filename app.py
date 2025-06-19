from flask import Flask, render_template, send_file, jsonify
import os
import math
import turtle
from io import BytesIO
import time

app = Flask(__name__)

# Configuración de la carpeta para guardar girasoles
GIRASOLES_FOLDER = os.path.join('static', 'girasoles')
os.makedirs(GIRASOLES_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sunflower')
def sunflower_page():
    return render_template('sunflower.html')

@app.route('/generate_sunflower')
def generate_sunflower():
    # Generar un nombre único para el archivo
    timestamp = int(time.time())
    filename = f"girasol_{timestamp}.png"
    filepath = os.path.join(GIRASOLES_FOLDER, filename)
    
    # Configurar turtle para dibujar
    turtle.bgcolor("black")
    turtle.shape("turtle")
    turtle.speed(0)
    
    # Configurar el canvas para turtle
    canvas = turtle.getcanvas()
    
    # Dibujar los pétalos
    turtle.goto(0, -40)
    turtle.pendown()
    h = 0
    for i in range(16):
        for j in range(18):
            turtle.color("yellow")
            h += 0.005
            turtle.rt(90)
            turtle.circle(150 - j * 6, 90)
            turtle.lt(90)
            turtle.circle(150 - j * 6, 90)
            turtle.rt(180)
        turtle.circle(40, 24)

    # Centro del girasol
    turtle.penup()
    turtle.goto(0, 0)
    turtle.color("black")
    turtle.fillcolor("brown")
    turtle.begin_fill()
    turtle.circle(0)
    turtle.end_fill()

    # Semillas en espiral
    phi = 137.508 * (math.pi / 180.0)
    for i in range(160 + 40):
        r = 4 * math.sqrt(i)
        theta = i * phi
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        turtle.penup()
        turtle.goto(x, y)
        turtle.setheading(i * 137.508)
        turtle.pendown()
        if i < 160:
            turtle.stamp()

    # Texto final
    turtle.penup()
    turtle.goto(0, 300)
    turtle.color("White")
    turtle.write("Te Quiero", align="center", font=("Arial", 24, "bold"))
    
    # Guardar la imagen
    canvas.postscript(file=filepath + '.eps')
    turtle.clearscreen()
    
    # Convertir EPS a PNG (requiere Ghostscript)
    os.system(f"magick convert {filepath}.eps {filepath}")
    os.remove(f"{filepath}.eps")
    
    return jsonify({'image_url': f'/static/girasoles/{filename}'})

if __name__ == '__main__':
    app.run(debug=True)
