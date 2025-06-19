from flask import Flask, render_template, send_file
import matplotlib
matplotlib.use('Agg')  # Usar backend no interactivo
import matplotlib.pyplot as plt
import numpy as np
import math
import io
import base64
from matplotlib.patches import Circle
import matplotlib.patches as patches

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sunflower')
def sunflower():
    return render_template('sunflower.html')

@app.route('/generate_sunflower')
def generate_sunflower():
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_xlim(-200, 200)
    ax.set_ylim(-200, 200)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    
    # Dibujar pétalos
    petal_colors = ['#FFD700', '#FFA500', '#FFFF00', '#FF8C00']
    
    for i in range(16):
        angle = i * (360 / 16) * math.pi / 180
        for j in range(12):
            # Crear pétalos elípticos
            petal_x = (80 - j * 4) * math.cos(angle)
            petal_y = (80 - j * 4) * math.sin(angle)
            
            ellipse = patches.Ellipse((petal_x, petal_y), 
                                    width=20 + j * 2, 
                                    height=8 + j,
                                    angle=math.degrees(angle),
                                    facecolor=petal_colors[j % len(petal_colors)],
                                    edgecolor='orange',
                                    alpha=0.8)
            ax.add_patch(ellipse)
    
    # Centro del girasol (semillas en espiral)
    phi = 137.508 * (math.pi / 180.0)  # Ángulo dorado
    
    for i in range(200):
        r = 2 * math.sqrt(i)
        theta = i * phi
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        
        # Gradiente de colores para las semillas
        if i < 50:
            color = '#8B4513'  # Marrón
        elif i < 100:
            color = '#A0522D'  # Marrón claro
        elif i < 150:
            color = '#D2691E'  # Chocolate
        else:
            color = '#CD853F'  # Tan
            
        circle = Circle((x, y), radius=2.5, 
                       facecolor=color, 
                       edgecolor='black',
                       linewidth=0.5)
        ax.add_patch(circle)
    
    # Texto "Te Quiero"
    ax.text(0, 150, 'Te Quiero ❤️', 
            fontsize=24, 
            fontweight='bold',
            color='white',
            ha='center',
            va='center',
            bbox=dict(boxstyle="round,pad=0.5", 
                     facecolor='pink', 
                     alpha=0.8))
    
    # Convertir a imagen base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', 
                bbox_inches='tight', 
                facecolor='black',
                dpi=150)
    img_buffer.seek(0)
    
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close(fig)  # Cerrar figura para liberar memoria
    
    return f'data:image/png;base64,{img_str}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
