# Punto 2 — Sistema de iluminación y monitoreo de temperatura con chatbot de voz

**Asignatura:** Aplicaciones en Sistemas Embebidos  
**Institución:** Fundación Universitaria Compensar  
**Docente:** Diego Alejandro Barragán Vargas  
**Miembro:** Karen Stefania Rivera Carrero, Carlos Alberto Castro Castillo, Lina Marcela Contreras Sanabria
---
## Introducción

Para este punto del laboratorio armamos un sistema donde uno le habla directamente al computador y este responde controlando luces físicas o diciéndole la temperatura que está midiendo el sensor. No hay que escribir nada, todo funciona por voz.

La dinámica es así: uno dice por ejemplo "enciende el led rojo" y en ese momento el LED físico conectado al Arduino se enciende. Si uno pregunta "¿qué temperatura hay?" el sistema lee el sensor DHT11 en ese instante y responde hablando, diciéndole el valor que midió. Es una conversación real entre el usuario y el hardware.

El DHT11 fue el sensor que usamos porque ya lo teníamos disponible y porque además de temperatura también puede medir humedad, aunque para este punto solo usamos la temperatura. Se conecta de forma digital al Arduino, a diferencia de sensores analógicos como el LM35, lo que lo hace un poco más preciso y fácil de leer una vez que se instala su librería.

La parte de voz la maneja Python con la librería speech_recognition, que captura lo que uno dice por el micrófono y lo convierte en texto. Ese texto luego se analiza buscando palabras clave para saber qué acción ejecutar, y la respuesta se genera también en audio usando pyttsx3 para que el sistema le hable de vuelta al usuario.

---
## Objetivos

- Implementar un chatbot completamente por voz, sin necesidad de escribir nada.
- Controlar dos LEDs físicos mediante comandos hablados interpretados por Python.
- Leer la temperatura en tiempo real desde el sensor DHT11 y comunicarla por audio.
- Establecer comunicación serial entre Python y Arduino para ejecutar las acciones físicas.
- Integrar reconocimiento de voz y síntesis de voz en un sistema embebido funcional.

---
## Materiales

| Componente | Cantidad | Para qué se usó |
|---|---|---|
| Arduino UNO | 1 | Microcontrolador principal |
| Sensor DHT11 | 1 | Medir temperatura y humedad |
| LED rojo | 1 | Indicador visual |
| LED verde | 1 | Indicador visual |
| Resistencias 220Ω | 2 | Proteger los LEDs |
| Resistencia 10kΩ | 1 | Pull-up para el DHT11 |
| Protoboard | 1 | Armar el circuito |
| Cables jumper | varios | Conexiones |
| Cable USB | 1 | Conectar Arduino al PC |
| PC con micrófono | 1 | Capturar los comandos de voz |

**Librerías Python utilizadas:**
```bash
pip install pyserial speechrecognition pyaudio pyttsx3
```

**Librería Arduino utilizada:**
Instalar "DHT sensor library" de Adafruit desde el gestor de librerías del IDE de Arduino.

---

## Cómo está organizado el sistema
```
┌─────────────────────────────────────────────────┐
│                   PC / Laptop                   │
│                                                 │
│   Micrófono ──► speech_recognition              │
│                      │                          │
│                      ▼                          │
│              Interpreta comando                 │
│                      │                          │
│                      ▼                          │
│   pyttsx3 ◄── Genera respuesta en voz          │
│                      │                          │
│                 pyserial (USB)                  │
└──────────────────────┼──────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│                 Arduino UNO                     │
│                                                 │
│   Pin 13 ──► LED Rojo   (220Ω ──► GND)         │
│   Pin 12 ──► LED Verde  (220Ω ──► GND)         │
│   Pin 7  ◄── DHT11 (10kΩ pull-up a 5V)        │
└─────────────────────────────────────────────────┘
```
Lo que pasa cada vez que uno habla:

1. El micrófono captura el audio y speech_recognition lo convierte en texto.
2. Python analiza ese texto buscando palabras como "enciende", "apaga" o "temperatura".
3. Dependiendo del comando, Python manda una instrucción corta al Arduino por serial.
4. Arduino ejecuta la acción: prende o apaga un LED, o lee el DHT11 y manda el dato.
5. Python recibe la respuesta y pyttsx3 se la dice al usuario en voz alta.

---
## Conexiones físicas

### LEDs

La pata larga del LED va al pin del Arduino pasando por una resistencia de 220Ω. La pata corta va a GND. Sin la resistencia el LED se quema o daña el pin.
```
Arduino
──────────────────────────────
Pin 13 ──► [220Ω] ──► (+) LED rojo  ──► (-) ──► GND
Pin 12 ──► [220Ω] ──► (+) LED verde ──► (-) ──► GND
```

### DHT11

El DHT11 tiene tres pines útiles: VCC, DATA y GND. El pin de datos necesita una resistencia de 10kΩ conectada entre él y los 5V, eso se llama resistencia pull-up y es necesaria para que la señal digital sea estable y el Arduino la lea bien. Sin esa resistencia el sensor puede dar lecturas erráticas o no funcionar.
```
Arduino
──────────────────────────────
5V     ────► Pin VCC del DHT11
GND    ────► Pin GND del DHT11
Pin 7  ◄──── Pin DATA del DHT11
             └── [10kΩ] ──► 5V  (pull-up)
```

---
## Qué hace el Arduino

Al encender, el Arduino configura los pines de los LEDs como salidas y abre la comunicación serial. Luego manda la palabra `LISTO` para avisarle a Python que ya puede empezar a mandar comandos, porque si Python arranca muy rápido y el Arduino todavía está iniciando, los primeros mensajes se pierden.

Después de eso se queda escuchando el serial. Cada vez que llega un comando:

- Con `LED_ROJO_ON` y `LED_ROJO_OFF` controla el pin 13.
- Con `LED_VERDE_ON` y `LED_VERDE_OFF` controla el pin 12.
- Con `LEDS_OFF` apaga los dos al mismo tiempo.
- Con `TEMP?` el Arduino le pide una lectura al DHT11, espera que el sensor responda y manda la temperatura de vuelta por serial. El DHT11 necesita al menos 2 segundos entre lecturas, eso ya lo maneja la librería internamente.

Si llega un comando que no reconoce, responde con `ERROR` para que Python sepa que algo salió mal.

---
## Qué hace Python

**El micrófono y el reconocimiento de voz** están manejados por speech_recognition. El programa abre el micrófono, ajusta el nivel de ruido ambiente durante medio segundo para que no confunda el ruido de fondo con voz, y luego se queda escuchando. Cuando detecta que alguien habló, manda el audio al servicio de Google Speech Recognition en español y recibe el texto de vuelta.

**La interpretación** no requiere que uno diga frases exactas. El programa busca palabras clave dentro de lo que se dijo. Si aparece "enciende" o "prende" junto con "rojo", entiende que hay que encender el LED rojo. Si aparece "temperatura" o "calor" o "frío", entiende que hay que consultar el sensor. Eso hace que la conversación sea más natural porque uno puede decirlo de distintas formas y igual funciona.

**La respuesta en voz** la genera pyttsx3, que es una librería de síntesis de voz que funciona sin internet. Cuando el sistema tiene la respuesta lista, en vez de mostrarla en pantalla la dice en voz alta por los parlantes. Por ejemplo si la temperatura es 23 grados dice "La temperatura actual es 23 grados, hace un clima agradable."

**La comunicación con Arduino** usa pyserial. Python abre el puerto serial, manda el comando como texto terminado en salto de línea, espera la respuesta y la procesa. Todo eso pasa en menos de un segundo para los LEDs, y en unos 2 o 3 segundos para la temperatura porque el DHT11 es más lento respondiendo.

---
## Cómo ponerlo a funcionar

**Paso 1 — Armar el circuito**
Conectar todo en la protoboard siguiendo el diagrama. Verificar la polaridad de los LEDs y que la resistencia de pull-up del DHT11 esté bien puesta entre el pin de datos y los 5V.

**Paso 2 — Instalar la librería del DHT11 en Arduino**
Abrir el IDE de Arduino, ir a `Herramientas → Administrar Librerías`, buscar "DHT sensor library" de Adafruit e instalarla. También va a pedir instalar "Adafruit Unified Sensor", aceptar.

**Paso 3 — Subir el código al Arduino**
Seleccionar la placa en `Herramientas → Placa → Arduino UNO` y el puerto correcto. Subir el código y verificar en el Monitor Serial que aparece `LISTO`.

**Paso 4 — Identificar el puerto serial**
En Windows se ve en el Administrador de Dispositivos bajo "Puertos COM y LPT", generalmente aparece como COM3 o COM4. En Linux o Mac correr `ls /dev/tty*` antes y después de conectar el Arduino para ver cuál apareció nuevo.

**Paso 5 — Instalar librerías de Python**
```bash
pip install pyserial speechrecognition pyaudio pyttsx3
```

**Paso 6 — Ejecutar el chatbot**
Editar el archivo `chatbot.py` y cambiar el puerto en la línea `PUERTO = 'COM3'` por el que corresponda. Luego correr:
```bash
python chatbot.py
```

El sistema va a decir en voz alta "Sistema listo, dime qué necesitas" cuando esté conectado y funcionando.

---
## Ejemplos de conversación por voz
```
Usuario dice:  "enciende el led rojo"
Sistema dice:  "Listo, el led rojo está encendido."

Usuario dice:  "qué temperatura hay"
Sistema dice:  "La temperatura actual es 24 grados, hace un clima agradable."

Usuario dice:  "apaga las luces"
Sistema dice:  "Leds apagados."

Usuario dice:  "hace calor?"
Sistema dice:  "La temperatura actual es 31 grados, está haciendo bastante calor."

Usuario dice:  "prende el verde"
Sistema dice:  "Listo, el led verde está encendido."
```

---
## Conclusiones

Trabajar con comandos de voz le da al sistema una dimensión completamente diferente a la de un proyecto típico de Arduino. En vez de presionar botones o escribir comandos, la interacción es completamente natural y eso hace que el sistema se sienta mucho más cercano a algo que uno usaría en la vida real.

El DHT11 funcionó bien para este propósito. Su precisión es de más o menos un grado centígrado, lo cual es suficiente para saber si hace frío o calor en un cuarto. Lo que sí hay que tener en cuenta es que necesita al menos 2 segundos entre lecturas, así que si el chatbot pregunta la temperatura muy seguido toca manejar esos tiempos en el código para que no de lecturas erróneas.

El reconocimiento de voz en español funcionó bastante bien en condiciones normales de ruido, aunque cuando hay mucho ruido de fondo o uno habla muy rápido a veces no entiende bien. Eso es una limitación del servicio de Google y no del código en sí.

Lo más valioso de este punto fue ver cómo tecnologías que uno normalmente ve por separado, el hardware embebido, la comunicación serial, el reconocimiento de voz y la síntesis de audio, se pueden unir en un solo sistema funcional con relativamente pocas líneas de código.

# Punto 3 — Sistema de reconocimiento de colores con visión artificial y control de LEDs

## Introducción

En este punto del laboratorio desarrollamos un sistema que usa la cámara del computador para detectar colores en tiempo real y, dependiendo del color que encuentre frente a la cámara, enciende o apaga un LED físico conectado al Arduino. Si la cámara detecta algo rojo, se enciende el LED rojo. Si detecta algo verde, se enciende el LED verde. En el momento en que el objeto desaparece del campo de visión, el LED correspondiente se apaga solo.

Todo el procesamiento de imagen lo hace Python usando OpenCV. El programa captura cada fotograma de la cámara, lo convierte al espacio de color HSV para analizar los tonos con más precisión, y busca regiones que coincidan con los rangos de color definidos. Cuando encuentra una región suficientemente grande, le avisa al Arduino por serial para que actúe sobre el hardware.

Lo que hace interesante este sistema es que el Arduino no toma ninguna decisión por su cuenta, simplemente obedece lo que Python le dice. Todo el "cerebro" del sistema está en el código de visión artificial corriendo en el computador, y el Arduino actúa como el brazo ejecutor que controla el mundo físico.

---
## Objetivos

- Usar OpenCV en Python para detectar colores específicos en tiempo real desde la cámara.
- Establecer comunicación serial entre Python y Arduino para enviar comandos según lo que se detecte.
- Controlar LEDs físicos de forma automática basándose en la detección de color.
- Entender cómo integrar visión artificial con sistemas embebidos.

---

## Materiales

| Componente | Cantidad | Para qué se usó |
|---|---|---|
| Arduino UNO | 1 | Controlar los LEDs según los comandos recibidos |
| LED rojo | 1 | Se enciende cuando la cámara detecta rojo |
| LED verde | 1 | Se enciende cuando la cámara detecta verde |
| Resistencias 220Ω | 2 | Proteger los LEDs |
| Protoboard | 1 | Armar el circuito |
| Cables jumper | varios | Conexiones |
| Cable USB | 1 | Comunicación PC ↔ Arduino y alimentación |
| PC con cámara | 1 | Capturar video y correr OpenCV |

**Librería Python necesaria:**
```bash
pip install opencv-python numpy pyserial
```

---

## Cómo está organizado el sistema
```
┌──────────────────────────────────────────────────┐
│                    PC / Laptop                   │
│                                                  │
│   Cámara ──► OpenCV captura fotograma            │
│                    │                             │
│                    ▼                             │
│          Convierte a HSV                         │
│                    │                             │
│                    ▼                             │
│   Aplica máscara de color rojo y verde           │
│                    │                             │
│                    ▼                             │
│   Busca contornos con área mayor a 800px         │
│                    │                             │
│          ┌─────────┴──────────┐                 │
│     rojo_detectado      verde_detectado          │
│          │                    │                 │
│     ROJO_ON/OFF          VERDE_ON/OFF            │
│                    │                             │
│              pyserial (USB Serial)               │
└────────────────────┼─────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────┐
│                 Arduino UNO                      │
│                                                  │
│   Pin 8 ──► LED Rojo  (220Ω ──► GND)            │
│   Pin 9 ──► LED Verde (220Ω ──► GND)            │
└──────────────────────────────────────────────────┘
```

El ciclo completo ocurre en cada fotograma de video, o sea unas 20 a 30 veces por segundo. Eso hace que la respuesta del LED sea prácticamente instantánea al mostrar u ocultar un objeto de color.

---

## Conexiones físicas

### LEDs

El LED rojo va conectado al pin 8 del Arduino y el LED verde al pin 9. Cada uno lleva una resistencia de 220Ω en serie entre el pin y el ánodo del LED para limitar la corriente. El cátodo de cada LED va directo a GND.
```
Arduino
──────────────────────────────
Pin 8  ──► [220Ω] ──► (+) LED rojo  ──► (-) ──► GND
Pin 9  ──► [220Ω] ──► (+) LED verde ──► (-) ──► GND
```

## Qué hace el código del Arduino

El Arduino es la parte más sencilla del sistema. Al encender configura los pines 8 y 9 como salidas y abre la comunicación serial a 9600 baudios. Después se queda en un ciclo infinito esperando que llegue algo por serial.

Cuando Python le manda un mensaje, el Arduino lo lee hasta encontrar el salto de línea, le quita los espacios sobrantes con `trim()` y lo compara con los cuatro comandos que conoce:

- `ROJO_ON` pone el pin 8 en HIGH y el LED rojo se enciende.
- `ROJO_OFF` pone el pin 8 en LOW y el LED rojo se apaga.
- `VERDE_ON` pone el pin 9 en HIGH y el LED verde se enciende.
- `VERDE_OFF` pone el pin 9 en LOW y el LED verde se apaga.

Nada más. El Arduino no decide nada por su cuenta, solo ejecuta lo que Python le dice.

---

## Qué hace el código de Python

**La conexión con Arduino** se abre al inicio con pyserial en el puerto COM3 a 9600 baudios. Se espera 2 segundos antes de seguir para que el Arduino termine de reiniciarse, porque cada vez que Python abre el puerto el Arduino se resetea automáticamente.

**La captura de video** usa `cv2.VideoCapture(0)` que abre la cámara principal del computador. Cada fotograma se voltea horizontalmente con `cv2.flip(frame, 1)` para que funcione como un espejo, lo que hace más intuitivo mostrar objetos frente a la cámara.

**La conversión a HSV** es el paso clave de todo el sistema. En vez de trabajar con los colores en formato BGR (el formato por defecto de OpenCV), el fotograma se convierte al espacio HSV que separa el tono del color (Hue), la saturación y el brillo en canales independientes. Eso hace que detectar un color específico sea mucho más resistente a cambios de iluminación que si se hiciera directamente en BGR.

**La detección de rojo** requiere dos rangos de HSV en vez de uno porque el rojo en el espacio HSV está partido en dos extremos del círculo cromático: valores cercanos a 0 y valores cercanos a 180. Por eso el código define `red_lower1/red_upper1` para el rango bajo y `red_lower2/red_upper2` para el rango alto, y suma las dos máscaras para cubrir todo el rojo posible.

**La detección de verde** solo necesita un rango, definido entre los valores 40 y 80 del canal Hue, que corresponde a los tonos verdes del espacio HSV.

**Los contornos** se buscan sobre cada máscara de color. Para cada contorno encontrado se calcula su área y solo se considera válido si supera los 800 píxeles. Ese filtro de área es importante porque evita que pequeños reflejos o ruido de la imagen disparen falsas detecciones. Cuando se encuentra un contorno válido, se dibuja sobre el fotograma y se escribe el nombre del color encima, lo que permite ver en tiempo real qué está detectando el sistema.

**El envío de comandos** ocurre al final de cada fotograma. Si durante ese fotograma se detectó rojo, se manda `ROJO_ON`, y si no se detectó, se manda `ROJO_OFF`. Lo mismo para el verde. Eso garantiza que los LEDs siempre reflejen exactamente lo que está viendo la cámara en ese momento, sin que sea necesario saber el estado anterior.

---

## Cómo ponerlo a funcionar

**Paso 1 — Armar el circuito**
Conectar los LEDs en los pines 8 y 9 del Arduino con sus respectivas resistencias de 220Ω. Verificar la polaridad antes de energizar.

**Paso 2 — Subir el código al Arduino**
Abrir el IDE de Arduino, seleccionar la placa y el puerto correcto en el menú Herramientas y subir el archivo `ARDUINOPUNTO3.ino`.

**Paso 3 — Verificar el puerto serial**
En Windows se identifica el puerto en el Administrador de Dispositivos bajo "Puertos COM y LPT". Si el puerto no es COM3, hay que cambiar esa línea en el archivo `PUNTO3.py`:
```python
arduino = serial.Serial('COM3', 9600, timeout=1)
```

**Paso 4 — Instalar las librerías**
```bash
pip install opencv-python numpy pyserial
```

**Paso 5 — Ejecutar el sistema**
```bash
python PUNTO3.py
```

Se abre una ventana llamada "Vision Artificial" mostrando lo que ve la cámara en tiempo real. Para cerrar el programa se presiona la tecla `ESC`.

---

## Cómo usar el sistema

Una vez corriendo el programa, basta con poner frente a la cámara un objeto de color rojo o verde y el LED correspondiente se enciende de inmediato. Cuando el objeto se retira del campo de visión, el LED se apaga solo. Se pueden detectar los dos colores al mismo tiempo si se tienen objetos de ambos colores frente a la cámara simultáneamente.

Lo que aparece en la ventana de video es el fotograma en vivo con los contornos dibujados alrededor de los objetos detectados y el nombre del color escrito encima de cada uno. Eso permite verificar que el sistema está reconociendo correctamente antes de mirar los LEDs físicos.

---

## Conclusiones

Este punto fue el más completo del laboratorio porque unió tres áreas que normalmente se trabajan por separado: visión artificial, comunicación serial y control de hardware embebido. Verlos funcionar juntos en un sistema coherente ayuda a entender cómo se construyen aplicaciones del mundo real como robots con sensores visuales o sistemas de clasificación automática en líneas de producción.

La parte más delicada fue ajustar los rangos HSV para que la detección funcionara bien con la iluminación del laboratorio. El rojo fue especialmente complicado porque está dividido en dos extremos del espacio HSV y al principio solo detectaba una parte del rango. Una vez que se entendió eso y se definieron los dos rangos separados, funcionó correctamente.

El filtro de área mínima de 800 píxeles fue una decisión importante porque sin él el sistema disparaba los LEDs por cualquier pequeño reflejo rojo o verde en la imagen. Con ese filtro solo reacciona cuando hay un objeto real de tamaño considerable frente a la cámara.

Como mejora futura sería interesante añadir más colores, detectar formas geométricas además de colores, o integrar el chatbot del punto 2 para que además de controlar los LEDs el sistema pueda responder preguntas sobre lo que está viendo la cámara.
