# Punto 2 — Sistema de iluminación y monitoreo de temperatura con chatbot de voz

> **Asignatura:** Aplicaciones en Sistemas Embebidos  
> **Institución:** Fundación Universitaria Compensar  
> **Docente:** Diego Alejandro Barragán Vargas  

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

---

## Estructura del repositorio
```
punto2/
├── README.md
├── punto2_arduino/
│   └── punto2_arduino.ino
├── chatbot.py
└── imagenes/
    └── diagrama_conexiones.png
```

---

> Códigos de ejemplo del curso: https://github.com/dialejobv/aplicacion_sistemas_embebidos
