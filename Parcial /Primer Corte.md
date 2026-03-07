<h1 align="center"> Pacial Primer Corte

# **1)Parte Concepual**

**A.¿Qué son los microcontroladores y los microprocesadores?**

**RTA:**

* Los microcontroladores son circuitos integrados programables que incluyen CPU, memoria y periféricos en un solo chip. Es compacto, eficiente y diseñado para controlas tareas especificas..
  
* Los micropocedores en el cerebro de la computadora realiza las funciones de la CPU en un chip. Es mas potente y versátil, pensando para procesar grandes volúmenes en información en sistemas complejos.

*  <img width="621" height="205" alt="image" src="https://github.com/user-attachments/assets/f4cc688e-50ad-4b33-91cd-87e792a3fa72" />


------
    
**B.Define la arquitectura Von Neumann y la Arquitectura de Harvar además: Exponer sus características ventajas y diferencias.**

**RTA:**

| Característica | Von Neumann | Harvard |
|---|---|---|
| Memoria | Usa la misma memoria para datos e instrucciones | Separa físicamente la memoria de datos y la de instrucciones |
| Procesamiento | Procesa una instrucción a la vez (secuencial) | Permite acceder simultáneamente a datos e instrucciones |
| Uso típico | PCs clásicos y sistemas de propósito general | Sistemas embebidos |
| Ventaja | Simplicidad en el diseño | Mayor velocidad y eficiencia |
| Desventaja | Cuello de botella al compartir bus de datos e instrucciones | Más compleja de implementar |
| Definición | Misma memoria para datos y programas. Secuencialidad: la CPU procesa una instrucción a la vez. | Utiliza un sistema de almacenamiento separado físicamente para las instrucciones y para los datos.|

------

**C.¿Qué son los procesadores tipos RISC y tipo CISC?**

**RTA:**

* CISC (Computadora de Conjunto de Instrucciones Complejas): Opera con numerosas instrucciones complejas, lo que le confiere versatilidad, aunque resulta más costoso y consume más energía. Un procesador capaz de manejar una amplia variedad de instrucciones se clasifica como CISC.

* RISC (Computadora de Conjunto de Instrucciones Reducidas): Trabaja con un número limitado de instrucciones simples, lo que simplifica la programación y optimiza la eficiencia. Cuando un procesador está diseñado para manejar pocas instrucciones… se le denomina RISC.

  <img width="259" height="194" alt="image" src="https://github.com/user-attachments/assets/b60aaff3-c570-4eee-bbd3-d9eced1360ad" />


-----

**D.¿Qué es ARM (Advanced RISC Machine)?**

**RTA:**

* ARM (Advanced RISC Machine): Es una serie de arquitecturas basadas en el concepto RISC, diseñadas para optimizar el consumo energético y ofrecer buen desempeño en equipos con recursos limitados.
  
Es la opción predominante en teléfonos móviles, dispositivos IoT y sistemas embebidos.

Entre sus propiedades destacan: instrucciones sencillas, bajo consumo de energía, variedad de perfiles (como Cortex A, R y M), compatibilidad con 64 bits y la integración de tecnologías como big.LITTLE.

Consiste en una gama de arquitecturas de procesadores fundamentadas en el enfoque RIS pensadas para maximizar la eficiencia energética y el rendimiento.

------

**E.¿Cuál es la arquitectura de Arduino? y ¿Qué características tiene?**

**RTA:**

| Característica | Arquitectura de Arduino (ATmega328P – Arduino Uno) |
|---|---|
| Tipo de arquitectura | Basada en arquitectura AVR tipo Harvard |
| Memoria y buses | Usa memorias y buses independientes para datos e instrucciones |
| Pines | Los pines pueden configurarse como entradas o salidas según lo requiera el usuario |
| Multitarea | Permite una multitarea sencilla |
| Reprogramación | Puede reprogramarse gracias al bootloader |
| Voltaje de operación | Funciona con voltajes de 7 a 12V |
| Corriente por pin | 20 mA recomendados por pin (máxima absoluta 40 mA) |
| Descripción | El microcontrolador admite ser reprogramado mediante el bootloader. Las entradas y salidas pueden adaptarse a las necesidades del usuario. |

-------

**F.¿Cuál es la arquitectura del pic 16f887 y sus principales características?**

**RTA:**

* Microcontroladores PIC

Los **microcontroladores PIC** forman parte de una familia de dispositivos basados en arquitectura **RISC (Reduced Instruction Set Computer)**, diseñados para ser eficientes, rápidos y de bajo consumo energético.


* Arquitectura

| Componente | Descripción |
|---|---|
| Memoria Flash | Memoria programable utilizada para almacenar los programas |
| RAM | Memoria utilizada para almacenar datos temporales durante la ejecución |
| EEPROM | Permite almacenar datos de forma permanente |
| Periféricos integrados | Incluye temporizadores, conversores ADC y módulos PWM |
| Tecnologías de bajo consumo | Implementa mecanismos para reducir el consumo energético |
| Unidad de procesamiento | Cuenta con contador de programa, ALU y buses diferenciados |


* Características principales

| Característica | Descripción |
|---|---|
| Bajo consumo energético | Diseñados para aplicaciones que requieren eficiencia energética |
| Versatilidad | Amplia gama de modelos para diferentes aplicaciones |
| Memoria de programa | Utiliza memoria **Flash** para almacenar los programas |


-----
-----

# **2)Parte de Diseño**

## Sistema de Reconocimiento de Herramientas y Monitoreo de Movimiento

Este proyecto propone un sistema basado en **visión por computadora** para identificar herramientas de laboratorio y analizar la velocidad de movimiento de personas utilizando **MediaPipe y aprendizaje automático**.

---

## 1. Base de datos de imágenes de herramientas

Para entrenar el sistema de reconocimiento se debe crear una base de datos de imágenes de herramientas.

#### Proceso

- Tomar **fotografías de cada herramienta del laboratorio** desde distintas perspectivas.
- **Estandarizar las imágenes**:
  - Misma resolución
  - Fondo homogéneo
- Guardar las imágenes en una **base de datos estructurada** como:
  - SQLite
  - PostgreSQL

#### Información almacenada

Cada imagen debe incluir etiquetas como:

| Campo | Descripción |
|---|---|
| Nombre | Nombre de la herramienta |
| Tipo | Tipo o categoría de herramienta |
| Función | Uso o aplicación principal |

#### Herramientas recomendadas

- **Google Colab**
- **TensorFlow Dataset**

Estas herramientas permiten organizar las imágenes y entrenar modelos de aprendizaje automático.

---

## 2. Sistema de clasificación con MediaPipe

El sistema utilizará **MediaPipe** para reconocer herramientas mediante visión por computadora.

#### Funciones principales

- Reconocimiento de objetos.
- Entrenamiento del modelo usando la base de datos de imágenes.

#### Flujo del sistema

| Etapa | Descripción |
|---|---|
| Entrada | Capturas en tiempo real desde cámara o video |
| Procesamiento | Detección de objetos mediante *bounding boxes* con MediaPipe |
| Salida | Nombre de la herramienta identificada y nivel de confianza |

---

## 3. Detección de velocidad de personas

El sistema también puede analizar el movimiento de personas utilizando **MediaPipe Pose**.

#### Proceso

- Identificación de **articulaciones del cuerpo humano**.
- Cálculo del cambio de posición en el tiempo:


- Definición de **umbrales de velocidad** para distinguir entre:
  - Movimiento normal
  - Movimiento rápido

### Resultado

- Generación de **alertas automáticas** cuando se supera el límite de velocidad definido.

---

## 4. Implementación en plataforma web o móvil

El sistema puede implementarse en aplicaciones web o móviles.

### Backend

Frameworks recomendados:

- Flask
- Django

Funciones:
- Procesamiento de datos
- Ejecución del modelo
- Envío de resultados al cliente

### Frontend

Para la interfaz web se pueden utilizar:

- React
- Vue.js

### Aplicación móvil

Opciones recomendadas:

- Flutter
- React Native

Estas aplicaciones se conectan al **backend** para obtener los resultados del sistema.

---

## 5. Visualización del sistema

La interfaz puede incluir:

-  Panel con las herramientas detectadas  
-  Indicador de velocidad de las personas  
-  Alertas emitidas en tiempo real

------------------------
-------------------------


# 3)Parte Empirica


### **A.Importar librerías**

```python
import cv2
import mediapipe as mp
```

* **cv2**: Librería OpenCV usada para trabajar con imágenes y video.
* **mediapipe**: Librería usada para detectar y rastrear manos.

---

### **B.Acceder al módulo de detección de manos**

```python
mp_hands = mp.solutions.hands
```

Se accede al módulo de **detección de manos** de MediaPipe.

---

### **C.Configuración del detector de manos**

```python
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
```

Parámetros:

* **static_image_mode=False**
  Indica que se trabajará con video en tiempo real.

* **max_num_hands=2**
  Número máximo de manos que el sistema puede detectar.

* **min_detection_confidence=0.7**
  Nivel mínimo de confianza para detectar una mano.

* **min_tracking_confidence=0.7**
  Nivel mínimo de confianza para el seguimiento de la mano.

---

### **E.Abrir la cámara**

```python
cap = cv2.VideoCapture(0)
```

Abre la cámara web del computador.

El número **0** indica la cámara principal.

---

### **F.Identificadores del pulgar**

```python
thumb_ids = [1,2,3,4]
```

MediaPipe detecta **21 puntos en la mano**.
Aquí se seleccionan los puntos correspondientes al **pulgar**.

---

### **G.Bucle principal**

```python
while True:
```

Crea un bucle infinito para procesar continuamente los frames de la cámara.

---

### **H.Leer frame de la cámara**

```python
ret, frame = cap.read()
```

* **ret**: indica si la lectura fue exitosa.
* **frame**: imagen capturada de la cámara.

---

### **I.Voltear la imagen**

```python
frame = cv2.flip(frame,1)
```

Invierte la imagen horizontalmente para que funcione como un espejo.

---

### **J.Convertir la imagen a RGB**

```python
rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
```

OpenCV usa formato **BGR**, mientras que MediaPipe utiliza **RGB**, por lo que es necesario convertir la imagen.

---

### **K.Procesar la imagen**

```python
results = hands.process(rgb)
```

MediaPipe analiza la imagen para detectar manos.

---

### **L.Verificar si se detectaron manos**

```python
if results.multi_hand_landmarks:
```

Si se detecta una o más manos, se obtienen los puntos de referencia.

---

### **M.Recorrer cada mano detectada**

```python
for hand in results.multi_hand_landmarks:
```

Permite trabajar con cada mano detectada en la imagen.

---

### **N. Obtener dimensiones de la imagen**

```python
h, w, c = frame.shape
```

* **h**: altura
* **w**: ancho
* **c**: canales de color

---

### **Ñ.Crear lista de puntos**

```python
puntos = []
```

Lista para almacenar las coordenadas del pulgar.

---

### **O.Recorrer los puntos de la mano**

```python
for id,lm in enumerate(hand.landmark):
```

Recorre los **21 puntos** detectados por MediaPipe.

---

### **P.Filtrar los puntos del pulgar**

```python
if id in thumb_ids:
```

Selecciona únicamente los puntos correspondientes al pulgar.

---

### **Q.Convertir coordenadas**

```python
cx, cy = int(lm.x*w), int(lm.y*h)
```

Convierte las coordenadas normalizadas (0 a 1) a coordenadas reales en píxeles.

---

### **R.Guardar los puntos**

```python
puntos.append((cx,cy))
```

Se guardan las coordenadas del pulgar en la lista.

---

### **S.Dibujar los puntos**

```python
cv2.circle(frame,(cx,cy),7,(0,255,0),-1)
```

Dibuja un círculo verde en cada punto detectado.

---

### **T. Conectar los puntos del pulgar**

```python
if len(puntos)==4:
```

Verifica que los 4 puntos del pulgar estén detectados.

---

### U.Dibujar líneas**

```python
cv2.line(frame,puntos[0],puntos[1],(0,255,0),3)
cv2.line(frame,puntos[1],puntos[2],(0,255,0),3)
cv2.line(frame,puntos[2],puntos[3],(0,255,0),3)
```

Dibuja líneas entre los puntos para visualizar el pulgar.

---

### **V.Mostrar el video**

```python
cv2.imshow("Pulgares Detectados",frame)
```

Muestra el video con las detecciones.

---

### **W.Salir del programa**

```python
if cv2.waitKey(1) & 0xFF == 27:
    break
```

Presionar **ESC** para cerrar el programa.

---

### **X.Liberar la cámara**

```python
cap.release()
```

Libera el acceso a la cámara.

---

### **Y.Cerrar ventanas**

```python
cv2.destroyAllWindows()
```

Cierra todas las ventanas abiertas por OpenCV.
