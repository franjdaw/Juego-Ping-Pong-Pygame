# 🏓 Pong Game - Python & Pygame

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Una implementación moderna del clásico juego **Pong** desarrollada en Python utilizando Pygame. Este proyecto no solo es un juego funcional, sino también una excelente demostración de los principios de **Programación Orientada a Objetos (POO)** con encapsulamiento, herencia y polimorfismo.

## 🎮 Características del Juego

### Gameplay
- **Modo 2 jugadores** local
- **Sistema de vidas** (3 vidas por jugador)
- **Sistema de puntuación** (primer jugador en 5 puntos gana)
- **Power-ups** dinámicos que aparecen durante el juego
- **Obstáculos** estáticos y móviles
- **Pelotas especiales** con comportamientos únicos
- **Música de fondo** y efectos de sonido
- **Fuente personalizada** para una mejor experiencia visual

### Power-ups Disponibles
- 🚀 **Velocidad**: Transforma la pelota en una versión más rápida
- 📏 **Tamaño**: Aumenta el tamaño de la pelota
- ⚡ **Zigzag**: La pelota se mueve en patrón zigzag

### Obstáculos
- **Obstáculos estáticos**: Bloques fijos en el campo
- **Obstáculos móviles**: Se mueven horizontalmente aumentando la dificultad

## 🏗️ Arquitectura del Código

### Principios POO Implementados

#### 🔒 Encapsulamiento
- Cada clase gestiona sus propios atributos y métodos
- Uso de atributos privados con getters/setters
- Protección contra modificaciones no controladas

#### 🧬 Herencia
- **Entidad**: Clase base para todos los objetos del juego
- **Pelota** → **PelotaRapida**, **PelotaGrande**, **PelotaZigZag**
- **Obstaculo** → **ObstaculoMovil**

#### 🔄 Polimorfismo
- Método `dibujar()` implementado diferente en cada clase
- Lista de entidades heterogéneas gestionadas uniformemente
- Manejo dinámico de tipos sin necesidad de identificación explícita

## 📁 Estructura del Proyecto

```
juegoparejas/
├── main.py                 # Punto de entrada del juego
├── juego.py               # Clase principal Juego - gestiona estados y lógica
├── entidad.py             # Clase base Entidad
├── jugador.py             # Clase Jugador - control de palas
├── pelota.py              # Clase Pelota - física y movimiento
├── pelota_especial.py     # Clases de pelotas especiales
├── powerup.py             # Clase PowerUp - gestión de mejoras
├── obstaculo.py           # Clases de obstáculos
├── assets/                # Recursos del juego
│   ├── ASMAN.TTF         # Fuente personalizada
│   ├── sounds/
│   │   ├── musica.mp3    # Música de fondo
│   │   └── rebote.wav    # Efecto de rebote
│   └── images/           # Imágenes (si aplica)
├── README.md              # Este archivo
└── .git/                 # Control de versiones
```

## 🚀 Requisitos

- **Python 3.7+**
- **Pygame 2.0+**

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/franjdaw/Juego-Ping-Pong-Pygame.git
cd Juego-Ping-Pong-Pygame

# Instalar Pygame
pip install pygame

# O usando requirements.txt (si lo creas)
pip install -r requirements.txt
```

## 🎯 Cómo Jugar

### Iniciar el Juego
```bash
python main.py
```

### Controles
| Acción | Jugador 1 | Jugador 2 |
|--------|-----------|-----------|
| Mover Arriba | **W** | **↑** |
| Mover Abajo | **S** | **↓** |
| Iniciar Juego | **SPACE** | |
| Reiniciar | **SPACE** (en pantalla de victoria) | |

### Reglas
- Cada jugador comienza con **3 vidas**
- Pierdes una vida cuando la pelota sale por tu lado
- Primer jugador en **5 puntos** gana
- Los power-ups aparecen cada 5 segundos
- Los obstáculos aparecen cada 10 segundos

## 🎨 Características Técnicas

### Sistema de Estados
- **inicio**: Pantalla de bienvenida
- **jugando**: Partida en curso
- **victoria**: Fin del juego con ganador

### Sistema de Colisiones
- Detección precisa pelota-jugador
- Colisiones con obstáculos
- Recogida de power-ups

### Sistema de Audio
- Música de fondo en bucle
- Efectos de sonido de rebote
- Gestión automática de recursos

### Sistema Visual
- Fuente personalizada ASMAN.TTF
- Renderizado optimizado a 60 FPS
- Interfaz limpia y minimalista

## 🔧 Personalización

### Modificar Dificultad
```python
# En juego.py
self.fps = 60  # Velocidad del juego
self.powerup_timer = 300  # Frecuencia de power-ups (frames)
self.obstaculo_timer = 600  # Frecuencia de obstáculos (frames)
```

### Añadir Nuevos Power-ups
```python
# En powerup.py
class NuevoPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, "nuevo_tipo")
```

### Cambiar Colores
```python
# En juego.py - método dibujar()
color_jugador1 = (255, 120, 120)  # Rojo
color_jugador2 = (120, 170, 255)  # Azul
```

## 🐛 Solución de Problemas

### Problemas Comunes
- **"No se encuentra la fuente"**: Asegúrate que `assets/ASMAN.TTF` existe
- **"No hay sonido"**: Verifica que `assets/sounds/musica.mp3` existe
- **"Error de Pygame"**: Instala la versión compatible: `pip install pygame==2.5.2`

### Depuración
```python
# Activar modo debug en main.py
DEBUG = True  # Muestra información adicional
```

## 🤝 Contribuir

1. **Fork** el proyecto
2. Crear una rama (`git checkout -b feature/nueva-caracteristica`)
3. **Commit** los cambios (`git commit -am 'Añadir nueva característica'`)
4. **Push** a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear un **Pull Request**

### Guía de Estilo
- Seguir PEP 8 para Python
- Comentar código complejo
- Añadir tests para nuevas funcionalidades

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- **Pygame Community** - Por la excelente documentación
- **Font Author** - Por la fuente ASMAN.TTF
- **Música y efectos de sonido** - Recursos de dominio público

## 📊 Estadísticas del Proyecto

- **Líneas de código**: ~500 líneas
- **Clases**: 8 clases principales
- **Archivos**: 9 archivos Python
- **Recursos**: 3 archivos multimedia
- **Tiempo de desarrollo**: Proyecto académico

## 🌟 Características Futuras

- [ ] Modo un jugador vs IA
- [ ] Sistema de high scores
- [ ] Más power-ups y obstáculos
- [ ] Modo multijugador online
- [ ] Editor de niveles
- [ ] Temas visuales personalizables

---

**¡Diviértete jugando!** 🎮

Si te gusta el proyecto, no olvides darle ⭐ en GitHub!
