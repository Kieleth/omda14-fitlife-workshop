# Paso 0 · Guía para Luis

El alumno recibe solo import, título y texto. No hay entrada, transformación, traza ni estado ya resueltos. Las instrucciones están en [la guía de clase](../SESION1_PASO0.md).

## Conducción

1. Crear la rama juntos. Mostrar la misma carpeta antes y después de cambiar de rama.
2. Ejecutar el starter y leer el error antes de corregirlo. Esperar a que todos vean el título y el texto.
3. Cada pareja cambia el texto entre comillas. Pedir que señalen la línea y el elemento de pantalla.
4. Introducir una variable con una entrada y su salida. Antes de ejecutar, recoger predicciones en voz alta. No tratar el texto vacío como un fallo.
5. Añadir la transformación. Una persona escribe, la otra propone un caso de prueba; intercambiar los papeles al cambiar la regla.
6. Añadir print. La traza se ve en la terminal del servidor. Una impresión antes de la entrada vuelve a ejecutarse cuando se confirma un cambio: el programa se recorre de arriba abajo.
7. Recorrer la ilustración HTML después de la observación. Pedir que relacionen cada parte con su propio portátil y con las líneas escritas.
8. Hacer diff, add y commit juntos. Comprobar que se guarda su programa, no una solución descargada.

Si alguien termina antes, puede proponer otro texto de prueba, intercambiar teclado o explicar el cambio a su pareja. No necesita abrir una actividad futura. Si se atasca, comparar únicamente la pieza de la ronda actual.

## Lo que debemos comprobar

Después de corregir el import solo aparecen el título y la bienvenida. Tras añadir la entrada, una frase confirmada con Intro se muestra. La transformación cambia la salida según la regla escrita. print aparece en la terminal; st.write en el navegador. Confirmar un cambio vuelve a ejecutar la impresión inicial.

Un cambio de texto también puede confirmarse al salir del campo. Guardar código con Always rerun puede ejecutar otra vez: no prometer un recuento fijo. No enseñar session_state todavía; se introducirá cuando necesitemos conservar historial.

## Referencia al terminar

```python
import streamlit as st
print("Se ejecuta paso_0")
st.title("Hola, FitLife")
st.write("Estamos construyendo nuestra primera app.")
mensaje = st.text_input("Mensaje", "Hola, FitLife")
resultado = mensaje.upper()
st.write(resultado)
print("Entrada:", mensaje, "| Salida:", resultado)
```

Las pruebas extraen los bloques de la guía de clase y los incorporan en ese orden al starter, para comprobar la construcción real y detectar si las instrucciones dejan de encajar.

Fuentes: [entrada de texto](https://docs.streamlit.io/develop/api-reference/widgets/st.text_input), [arquitectura de Streamlit](https://docs.streamlit.io/develop/concepts/architecture/architecture).
