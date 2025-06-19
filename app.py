from flask import Flask, render_template_string, jsonify
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

# HTML templates como strings
INDEX_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>¡Feliz día!</title>
<style>
    body {
        margin: 0;
        overflow: hidden;
        background-color: #d8bfd8;
        height: 100vh;
        width: 100vw;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        font-family: 'Arial', sans-serif;
    }
    
    /* Estilo del menú */
    .menu {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 100;
    }
    
    .menu-button {
        background: linear-gradient(135deg, #ff69b4, #ff1493);
        color: white;
        border: none;
        padding: 15px 20px;
        border-radius: 25px;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);
        transition: all 0.3s ease;
    }
    
    .menu-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 105, 180, 0.4);
    }
    
    .menu-dropdown {
        position: absolute;
        top: 100%;
        right: 0;
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        overflow: hidden;
        opacity: 0;
        transform: translateY(-10px);
        transition: all 0.3s ease;
        pointer-events: none;
        min-width: 200px;
    }
    
    .menu-dropdown.active {
        opacity: 1;
        transform: translateY(5px);
        pointer-events: all;
    }
    
    .menu-item {
        display: block;
        padding: 15px 20px;
        text-decoration: none;
        color: #333;
        transition: background-color 0.3s ease;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .menu-item:hover {
        background-color: #ff69b4;
        color: white;
    }
    
    .menu-item:last-child {
        border-bottom: none;
    }
    
    .confetti {
        position: fixed;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1;
        width: 100%;
        height: 100%;
        pointer-events: none;
    }
    .loader {
        position: fixed;
        top: 0; left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: black;
        z-index: 10;
    }
    .loader .spinner {
        border: 8px solid rgba(255, 255, 255, 0.1);
        border-top: 8px solid white;
        border-radius: 50%;
        width: 80px; height: 80px;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .fade-out {
        animation: fadeOut 1s forwards;
    }
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    h1 {
        font-size: 5rem;
        color: #ff69b4;
        text-align: center;
        position: relative;
        z-index: 2;
        text-shadow: 4px 4px 8px rgba(0, 0, 0, 0.4);
        font-weight: bold;
        overflow: hidden;
        visibility: hidden;
        margin-bottom: 5px;
    }
    h1 span {
        display: inline-block;
        opacity: 0;
    }

    .music-player {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #333;
        color: #fff;
        text-align: center;
        padding: 10px;
        z-index: 5;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .music-player button {
        background-color: #ff69b4;
        border: none;
        color: white;
        padding: 10px;
        margin: 0 5px;
        cursor: pointer;
        font-size: 16px;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .music-player button:hover {
        background-color: #ff85a2;
        box-shadow: 0 0 10px #ff69b4, 0 0 20px #ff69b4, 0 0 30px #ff69b4;
    }
    .now-playing {
        margin-left: 10px;
        font-size: 16px;
    }

    .birthday-message {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
        padding: 20px;
        border-radius: 10px;
        color: #fff;
        font-family: 'Brush Script MT', cursive;
        font-size: 1.5rem;
        text-align: center;
        opacity: 0;
        transform: translateY(20px);
        z-index: 2;
    }

    @keyframes slideUpFadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .message-visible {
        animation: slideUpFadeIn 1s ease-out forwards;
    }

    .balloon {
        position: absolute;
        bottom: -150px;
        width: 40px;
        height: 50px;
        border-radius: 50%;
        background-color: red;
        z-index: 0;
    }

    .balloon::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        width: 2px;
        height: 20px;
        background-color: #555;
        transform: translateX(-50%);
    }

    .emoji {
        position: fixed;
        font-size: 2.5rem;
        z-index: 2;
    }

    .emoji.top-left {
        top: 10px;
        left: 10px;
    }

    .emoji.top-right {
        top: 10px;
        right: 10px;
    }

    .emoji.bottom-left {
        bottom: 10px;
        left: 10px;
    }

    .emoji.bottom-right {
        bottom: 10px;
        right: 10px;
    }
    
    .loader-text {
        color: white;
        font-size: 1.5rem;
        margin-top: 20px;
        text-align: center;
    }
    
    #birthdayImage {
        opacity: 0;
        transform: translateY(20px);
        z-index: 2;
        width: 300px;
        height: auto;
        margin-bottom: 0px;
    }
</style>
</head>
<body>
<!-- Menú -->
<div class="menu">
    <button class="menu-button" onclick="toggleMenu()">☰ Menú</button>
    <div class="menu-dropdown" id="menuDropdown">
        <a href="#" class="menu-item" onclick="closeMenu()">🏠 Inicio</a>
        <a href="/sunflower" class="menu-item">🌻 Girasol Especial</a>
        <a href="#" class="menu-item" onclick="showMoreMessages()">💝 Más Mensajes</a>
        <a href="#" class="menu-item" onclick="showGallery()">📸 Galería</a>
    </div>
</div>

<div class="loader" id="loader">
    <div class="spinner"></div>
    <div class="loader-text">Preparando tu sorpresa...</div>
</div>
<div class="confetti" id="confetti"></div>
<h1 id="birthdayTitle">
    <span>¡</span><span>F</span><span>E</span><span>L</span><span>I</span><span>Z</span><span> </span>
    <span>C</span><span>U</span><span>M</span><span>P</span><span>L</span><span>E</span><span>A</span><span>Ñ</span><span>O</span><span>S</span><span>!</span>
</h1>

<div id="birthdayImage">🎂</div>

<div class="birthday-message" id="birthdayMessage">
    Que este nuevo año de vida esté lleno de bendiciones, amor y alegría. Que Dios te guíe y proteja siempre.<br>
    "El Señor te bendiga y te guarde; el Señor haga resplandecer su rostro sobre ti, y tenga de ti misericordia."<br>
    <strong>- Números 6:24-25</strong>
</div>

<div class="music-player">
    <button onclick="prevSong()">⏮️</button>
    <button onclick="togglePlayPause()">⏯️</button>
    <button onclick="nextSong()">⏭️</button>
    <div class="now-playing" id="nowPlaying">🎵 Música de Cumpleaños</div>
    <audio id="audioPlayer"></audio>
</div>

<div class="emoji top-left">🎉</div>
<div class="emoji top-right">🎂</div>
<div class="emoji bottom-left">🎁</div>
<div class="emoji bottom-right">🎈</div>

<script>
    // Función para toggle del menú
    function toggleMenu() {
        const dropdown = document.getElementById('menuDropdown');
        dropdown.classList.toggle('active');
    }
    
    function closeMenu() {
        document.getElementById('menuDropdown').classList.remove('active');
    }
    
    function showMoreMessages() {
        alert('¡Aquí podrás ver más mensajes especiales muy pronto! 💝');
        closeMenu();
    }
    
    function showGallery() {
        alert('¡Galería de fotos próximamente! 📸');
        closeMenu();
    }
    
    // Cerrar menú al hacer clic fuera
    document.addEventListener('click', function(event) {
        const menu = document.querySelector('.menu');
        if (!menu.contains(event.target)) {
            closeMenu();
        }
    });

    // Confetti Animation
    function createConfetti() {
        for (let i = 0; i < 50; i++) {
            let confetti = document.createElement('div');
            confetti.style.position = 'absolute';
            confetti.style.width = `${Math.random() * 10 + 5}px`;
            confetti.style.height = `${Math.random() * 10 + 5}px`;
            confetti.style.backgroundColor = `hsl(${Math.random() * 360}, 100%, 50%)`;
            confetti.style.left = `${Math.random() * window.innerWidth}px`;
            confetti.style.top = `${-50}px`;
            confetti.style.pointerEvents = 'none';
            confetti.style.zIndex = '1';
            document.body.appendChild(confetti);

            // Animate confetti falling
            let fallSpeed = Math.random() * 3 + 2;
            let horizontalSpeed = Math.random() * 2 - 1;
            let rotation = 0;
            
            function animateConfetti() {
                let currentTop = parseFloat(confetti.style.top);
                let currentLeft = parseFloat(confetti.style.left);
                
                if (currentTop < window.innerHeight + 50) {
                    confetti.style.top = (currentTop + fallSpeed) + 'px';
                    confetti.style.left = (currentLeft + horizontalSpeed) + 'px';
                    confetti.style.transform = `rotate(${rotation}deg)`;
                    rotation += 5;
                    requestAnimationFrame(animateConfetti);
                } else {
                    confetti.remove();
                }
            }
            
            requestAnimationFrame(animateConfetti);
        }
    }

    setInterval(createConfetti, 1000);

    setTimeout(() => {
        document.getElementById('loader').classList.add('fade-out');
        setTimeout(() => {
            document.getElementById('loader').style.display = 'none';
            document.getElementById('birthdayTitle').style.visibility = 'visible';
            animateTitle();
        }, 1000);
    }, 3000);

    function animateTitle() {
        const spans = document.querySelectorAll('#birthdayTitle span');
        spans.forEach((span, index) => {
            setTimeout(() => {
                span.style.opacity = '1';
                span.style.transform = 'translateY(0)';
                span.style.transition = 'all 0.5s ease';
            }, index * 100);
        });
        
        setTimeout(() => {
            const image = document.getElementById('birthdayImage');
            image.style.opacity = '1';
            image.style.transform = 'translateY(0)';
            image.style.transition = 'all 1s ease';
            
            document.getElementById('birthdayMessage').classList.add('message-visible');
            animateBalloons();
        }, 2000);
    }

    function animateBalloons() {
        const colors = ['#ff69b4', '#ff4500', '#ffa500', '#ff6347', '#ff1493', '#ffd700'];
        for (let i = 0; i < 20; i++) {
            let balloon = document.createElement('div');
            balloon.classList.add('balloon');
            balloon.style.left = `${Math.random() * 100}vw`;
            balloon.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            document.body.appendChild(balloon);

            let speed = Math.random() * 2 + 1;
            function animateBalloon() {
                let currentBottom = parseFloat(balloon.style.bottom) || -150;
                if (currentBottom < window.innerHeight + 100) {
                    balloon.style.bottom = (currentBottom + speed) + 'px';
                    requestAnimationFrame(animateBalloon);
                } else {
                    balloon.remove();
                }
            }
            
            setTimeout(() => {
                requestAnimationFrame(animateBalloon);
            }, Math.random() * 2000);
        }
    }

    // Music player functionality (simplified)
    let isPlaying = false;
    let currentSong = 0;
    const songs = ['🎵 Cumpleaños Feliz', '🎶 Las Mañanitas', '🎵 Happy Birthday'];

    function togglePlayPause() {
        isPlaying = !isPlaying;
        document.getElementById('nowPlaying').textContent = 
            isPlaying ? `🎵 Reproduciendo: ${songs[currentSong]}` : '⏸️ Pausado';
    }

    function prevSong() {
        currentSong = (currentSong - 1 + songs.length) % songs.length;
        document.getElementById('nowPlaying').textContent = `🎵 ${songs[currentSong]}`;
    }

    function nextSong() {
        currentSong = (currentSong + 1) % songs.length;
        document.getElementById('nowPlaying').textContent = `🎵 ${songs[currentSong]}`;
    }
</script>
</body>
</html>'''

SUNFLOWER_HTML = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌻 Girasol Especial</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            font-family: 'Arial', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
            to { text-shadow: 2px 2px 20px rgba(255,215,0,0.8); }
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: #FFD700;
            margin-bottom: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            max-width: 800px;
            width: 100%;
            text-align: center;
        }
        
        .generate-btn {
            background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 1.2rem;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .generate-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        
        .generate-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        #sunflowerImage {
            max-width: 100%;
            height: auto;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            margin-bottom: 20px;
            opacity: 0;
            transform: scale(0.8);
            transition: all 0.5s ease;
        }
        
        #sunflowerImage.show {
            opacity: 1;
            transform: scale(1);
        }
        
        .loading {
            display: none;
            margin: 20px 0;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #FFD700;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .message {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin-top: 20px;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        
        .back-btn {
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(255,255,255,0.2);
            color: white;
            border: 2px solid white;
            padding: 10px 20px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        
        .back-btn:hover {
            background: white;
            color: #2a5298;
            transform: translateY(-2px);
        }
        
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }
        
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: #FFD700;
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); opacity: 0; }
            50% { transform: translateY(-100px); opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="particles" id="particles"></div>
    
    <a href="/" class="back-btn">← Volver al Inicio</a>
    
    <div class="header">
        <h1>🌻 Girasol Especial 🌻</h1>
        <p class="subtitle">Un regalo único creado con amor matemático</p>
    </div>
    
    <div class="container">
        <button class="generate-btn" onclick="generateSunflower()" id="generateBtn">
            ✨ Crear Mi Girasol ✨
        </button>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Cultivando tu girasol especial...</p>
        </div>
        
        <img id="sunflowerImage" alt="Girasol Especial" style="display: none;">
        
        <div class="message">
            <h3>💖 Mensaje Especial 💖</h3>
            <p>Este girasol ha sido creado especialmente para ti usando la belleza de las matemáticas. 
            Cada semilla está posicionada siguiendo la secuencia de Fibonacci y el ángulo dorado, 
            creando la espiral perfecta que vemos en la naturaleza.</p>
            <p><strong>Como este girasol siempre busca la luz del sol, 
            que tu vida siempre encuentre la felicidad y el amor. ¡Feliz Cumpleaños! 🎉</strong></p>
        </div>
    </div>

    <script>
        // Crear partículas flotantes
        function createParticles() {
            const container = document.getElementById('particles');
            for (let i = 0; i < 20; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 6 + 's';
                particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
                container.appendChild(particle);
            }
        }
        
        function generateSunflower() {
            const btn = document.getElementById('generateBtn');
            const loading = document.getElementById('loading');
            const image = document.getElementById('sunflowerImage');
            
            // Mostrar loading
            btn.disabled = true;
            loading.style.display = 'block';
            image.style.display = 'none';
            image.classList.remove('show');
            
            // Generar girasol
            fetch('/generate_sunflower')
                .then(response => response.text())
                .then(data => {
                    loading.style.display = 'none';
                    image.src = data;
                    image.style.display = 'block';
                    setTimeout(() => {
                        image.classList.add('show');
                    }, 100);
                    btn.disabled = false;
                    btn.textContent = '🌻 Crear Otro Girasol 🌻';
                })
                .catch(error => {
                    console.error('Error:', error);
                    loading.style.display = 'none';
                    btn.disabled = false;
                    alert('Error al crear el girasol. Por favor, intenta de nuevo.');
                });
        }
        
        // Inicializar partículas
        createParticles();
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(INDEX_HTML)

@app.route('/sunflower')
def sunflower():
    return render_template_string(SUNFLOWER_HTML)

@app.route('/generate_sunflower')
def generate_sunflower():
    try:
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
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
