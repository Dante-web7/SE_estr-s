from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista de preguntas
preguntas = [
    "En el último mes, ¿con qué frecuencia ha estado afectado(a) por algo que ha ocurrido inesperadamente?",
    "En el último mes, ¿con qué frecuencia se ha sentido incapaz de controlar las cosas importantes en su vida?",
    "En el último mes, ¿con qué frecuencia se ha sentido nervioso(a) o estresado(a)?",
    "En el último mes, ¿con qué frecuencia ha manejado con éxito los pequeños problemas irritantes de la vida?",
    "En el último mes, ¿con qué frecuencia ha sentido que ha afrontado efectivamente los cambios importantes que han estado ocurriendo en su vida?",
    "En el último mes, ¿con qué frecuencia ha estado seguro(a) sobre su capacidad para manejar sus problemas personales?",
    "En el último mes, ¿con qué frecuencia ha sentido que las cosas le van bien?",
    "En el último mes, ¿con qué frecuencia ha sentido que no podía afrontar todas las cosas que tenía que hacer?",
    "En el último mes, ¿con qué frecuencia ha podido controlar las dificultades de su vida?",
    "En el ultimo mes, ¿con que frecuencia se ha sentido que tenia todo bajo control?",
    "En el último mes, ¿con qué frecuencia ha estado enfadado(a) porque las cosas que le han ocurrido estaban fuera de su control?",
    "En el último mes, ¿con qué frecuencia ha pensado sobre las cosas que le quedan por hacer?",
    "En el último mes, ¿con qué frecuencia ha podido controlar la forma de pasar el tiempo?",
    "En el último mes, ¿con qué frecuencia ha sentido que las dificultades se acumulan tanto que no puede superarlas?",
]

# Ítems que requieren inversión de puntuación (según las reglas de PSS-14)
items_invertir = [4, 5, 6, 7, 9, 10, 13]  # Usamos índice 1 basado en las reglas

# Lista para almacenar las respuestas del usuario
respuestas_usuario = [None] * len(preguntas)

def invertir_puntuacion(respuesta):
    # Invertir la puntuación: 0 -> 4, 1 -> 3, 2 -> 2, 3 -> 1, 4 -> 0
    return 4 - respuesta

@app.route('/') #Definimos la ruta para la pagina principal
def index():
    return render_template('index.html')

@app.route('/iniciar_test')
def iniciar_test():
    # Redirige a la primera pregunta
    return redirect(url_for('pregunta', num=1))

@app.route('/pregunta/<int:num>', methods=['GET', 'POST'])
def pregunta(num):
    if request.method == 'POST':
        # Guarda la respuesta del usuario
        respuesta = request.form.get('respuesta')
        respuestas_usuario[num - 1] = int(respuesta) if respuesta is not None else None

        # Redirige a la siguiente pregunta o muestra los resultados
        if num < len(preguntas):
            return redirect(url_for('pregunta', num=num + 1))
        else:
            return redirect(url_for('resultados'))

    return render_template('pregunta.html', num=num, pregunta=preguntas[num - 1],total_preguntas=len(preguntas))

@app.route('/resultados')
def resultados():
    # Calcula la puntuación total, invirtiendo los ítems que corresponden
    puntaje_total = 0
    for i, respuesta in enumerate(respuestas_usuario):
        if respuesta is not None:
            if i + 1 in items_invertir:
                puntaje_total += invertir_puntuacion(respuesta)
            else:
                puntaje_total += respuesta

    # Determina el nivel de estrés y la recomendación basada en el puntaje total
    if puntaje_total <= 14:
        nivel_estres = "Casi nunca o nunca está estresado."
        recomendaciones = [
            "Continúe practicando actividades relajantes.",
            "Mantenga hábitos de vida saludables.",
            "Realice ejercicios regularmente para mantener un buen estado físico y mental."
        ]
        nivel_clase = "bajo"
    elif puntaje_total <= 28:
        nivel_estres = "De vez en cuando está estresado."
        recomendaciones = [
            "Practique técnicas de relajación, como la meditación o la respiración profunda.",
            "Intente equilibrar su tiempo entre el trabajo y las actividades recreativas.",
            "Dedique tiempo a sus hobbies y pasatiempos para reducir el estrés."
        ]
        nivel_clase = "moderado"
    elif puntaje_total <= 42:
        nivel_estres = "A menudo está estresado."
        recomendaciones = [
            "Considere establecer una rutina diaria de ejercicios y relajación.",
            "Hable con amigos o familiares sobre sus preocupaciones.",
            "Evalúe la posibilidad de ajustar su carga de trabajo o sus responsabilidades diarias."
        ]
        nivel_clase = "alto"
    else:
        nivel_estres = "Muy a menudo está estresado."
        recomendaciones = [
            "Considere buscar apoyo profesional, como un terapeuta o consejero.",
            "Practique actividades de autocuidado, como el descanso adecuado y una dieta saludable.",
            "Evite el consumo excesivo de estimulantes, como la cafeína o el alcohol."
        ]
        nivel_clase = "muy-alto"

    return render_template('resultados.html', puntaje_total=puntaje_total, nivel_estres=nivel_estres, recomendaciones=recomendaciones, nivel_clase=nivel_clase)

if __name__ == '__main__':
    app.run(debug=True)

