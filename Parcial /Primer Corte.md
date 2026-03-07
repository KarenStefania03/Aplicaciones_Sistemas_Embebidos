# **Pacial Primer Corte**


## **1)Parte Concepual**

**A.¿Qué son los microcontroladores y los microprocesadores?**

**RTA:**

* Los microcontroladores son circuitos integrados programables que incluyen CPU, memoria y periféricos en un solo chip. Es compacto, eficiente y diseñado para controlas tareas especificas..
  
* Los micropocedores en el cerebro de la computadora realiza las funciones de la CPU en un chip. Es mas potente y versátil, pensando para procesar grandes volúmenes en información en sistemas complejos.

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



