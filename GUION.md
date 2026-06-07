# Guion Hito 4 — Dashboard Interactivo (Streamlit)

## 🎙️ Guion para grabación (apto para ElevenLabs)

Hola, soy [NOMBRE] y en este video presento el **Hito 4** del Trabajo Práctico Integrador.

El objetivo es **convertir el análisis del notebook en una interfaz interactiva**, para que un docente o gestor pueda explorar el desempeño académico sin ver código.

Desarrollamos un dashboard en **Streamlit** con tres partes principales: **filtros**, **KPIs** y **gráficos dinámicos**.

Primero, en la barra lateral tenemos los **filtros**: semana del semestre, rendimiento (performance index), nivel de estrés, horas de sueño y tasa de asistencia. Estos filtros permiten segmentar a los estudiantes y analizar comportamientos específicos.

En el centro mostramos los **KPIs**: cantidad de registros filtrados, promedio de rendimiento, porcentaje de estudiantes en riesgo y promedio de estrés. Todas estas métricas se actualizan en tiempo real cuando cambiamos los filtros.

Luego, presentamos los **gráficos**:

1) Un histograma del performance index para ver la distribución general del rendimiento.
2) Un scatter de estrés versus rendimiento con línea de tendencia, que muestra una relación negativa.
3) Un scatter de horas de sueño versus rendimiento, que muestra una relación positiva.

Finalmente, incluimos una tabla con una **vista previa** de los datos filtrados, para que el usuario pueda inspeccionar casos puntuales.

Con esta interfaz, cualquier usuario puede detectar rápidamente patrones de riesgo y tomar decisiones informadas.

Eso sería todo para el Hito 4. Gracias.

---

## 🧭 Qué mostrar y cómo interactuar (paso a paso)

1) **Abrir el dashboard**
   - Mostrar en terminal: `streamlit run app/dashboard.py`
   - Esperar que se abra la pestaña en el navegador.

2) **Explicar la barra lateral de filtros**
   - Mostrar slider de **Semana**.
   - Mostrar rango de **Performance Index**.
   - Mostrar rango de **Estrés**.
   - Mostrar rango de **Horas de sueño**.
   - Mostrar rango de **Asistencia**.

3) **Demostración de interacción**
   - Mover el filtro de **estrés** hacia valores altos.
   - Observar cómo bajan los KPIs de rendimiento y cambia la distribución.
   - Ajustar **horas de sueño** a valores bajos y mostrar impacto.

4) **Explicar los KPIs**
   - Registros filtrados
   - Promedio rendimiento
   - % en riesgo
   - Promedio estrés

5) **Recorrer los gráficos**
   - Histograma (distribución de rendimiento)
   - Estrés vs rendimiento (tendencia negativa)
   - Sueño vs rendimiento (tendencia positiva)

6) **Mostrar tabla de datos**
   - Scrollear un poco y mencionar que es útil para inspeccionar casos.

7) **Cierre**
   - Resumir que la interfaz cumple interactividad, KPIs y visualización dinámica.
   - Remarcar utilidad para decisiones pedagógicas.
