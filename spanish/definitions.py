from collections import namedtuple


word = namedtuple("word", ["english", "spanish"])
verb = namedtuple("verb", ["english", "spanish_invinitive", "yo_conj", "tu_conj", "el_conj", "nos_conj", "vos_conj", "ustedes_conj"])




def conj_present(verb, type, pronoun):
    conjugation = ""
    if type == "ar":
        if pronoun == "yo":
            conjugation = verb[:-2] + "o"
        elif pronoun == "tu":
            conjugation = verb[:-2] + "as"
        elif pronoun == "ella" or pronoun == "el" or pronoun == "usted":
            conjugation = verb[:-2] + "a"
        elif pronoun == "nos":
            conjugation = verb[:-2] + "amos"
        elif pronoun == "vos":
            conjugation = verb[:-2] + "áis"
        elif pronoun == "ellos" or pronoun == "ellas" or pronoun == "ustedes":
            conjugation = verb[:-2] + "an"
    elif type == "ir":
        if pronoun == "yo":
            conjugation = verb[:-2] + "o"
        elif pronoun == "tu":
            conjugation = verb[:-2] + "es"
        elif pronoun == "ella" or pronoun == "el" or pronoun == "usted":
            conjugation = verb[:-2] + "e"
        elif pronoun == "nos":
            conjugation = verb[:-2] + "imos"
        elif pronoun == "vos":
            conjugation = verb[:-2] + "ís"
        elif pronoun == "ellos" or pronoun == "ellas" or pronoun == "ustedes":
            conjugation = verb[:-2] + "en"
    elif type == "ir":
        if pronoun == "yo":
            conjugation = verb[:-2] + "o"
        elif pronoun == "tu":
            conjugation = verb[:-2] + "es"
        elif pronoun == "ella" or pronoun == "el" or pronoun == "usted":
            conjugation = verb[:-2] + "e"
        elif pronoun == "nos":
            conjugation = verb[:-2] + "emos"
        elif pronoun == "vos":
            conjugation = verb[:-2] + "éis"
        elif pronoun == "ellos" or pronoun == "ellas" or pronoun == "ustedes":
            conjugation = verb[:-2] + "en"
    return conjugation




vocab_1_usefull_phrases = [
word("You ALL open the books", "Abran los libros"),
word("You all close the books", "Cierren los libros"),
word("You all write", "Escriban"),
word("You all listen", "Escuchen"),
word("You all read", "Lean"),
word("You all raise your hand", "Levanten la mano"),
word("You all look at the board", "Miren el pizarrón"),
word("You all look at the photo", "Miren la foto"),
word("Pass me the homework", "Pásenme la tarea"),
word("You all repeat", "Repitan"),
word("You all take out a pencil", "Saquen un lápiz"),
word("You all sit down", "Siéntense"),
word("How do you say", "¿Cómo se dice...?"),
word("Slower, please", "Más despacio, por favor"),
word("I don't know", "No sé"),
word("What does ... mean?", "¿Qué quiere decir...?"),
word("Repeat, please", "Repita, por favor"),
word("Change roles", "Cambien de papel"),
word("Complete the conversation", "Completa la conversación"),
word("Answer the questions", "Contesta las preguntas"),
word("Say who is speaking", "Di quién habla"),
word("Is it true or false?", "¿Es cierto o falso?"),
word("Choose the correct answer.", "Escoge la respuesta correcta"),
word("You listen", "Escucha"),
word("You explain", "Explica"),
word("You read", "Lee"),
word("Ask another student", "Pregúntale a otro(a) estudiante"),
word("Work with another student", "Trabaja con otro(a) estudiante"),
word("Work in a group of", "Trabaja en un grupo de..."),
word("Bless you", "Salud"),
word("Good", "Bueno"),
word("Bad", "Malo"),
word("Are there any questions?", "¿Hay preguntas?"),
word("Right", "Derecha"),
word("Left", "Izquierda"),
word("Do you all understand?", "¿Comprenden?"),
word("Again", "Otra vez"),
word("Give me", "Dame"),
word("Out loud", "En voz alta"),
word("How do you say ... in Spanish?", "¿Cómo se dice... en español?"),
word("Yes, I understand.", "Sí, entiendo"),
word("No, I don't understand.", "No, no entiendo"),
word("Excuse me, pardon me", "Perdón"),
word("I'm sorry", "Lo siento"),
word("Please", "Por favor"),
word("Thank you", "Gracias"),
word("You're welcome", "De nada"),
word("Can I go to the bathroom?", "¿Puedo ir al baño?"),
word("Can I go to the nurse?", "¿Puedo ir a la enfermera?"),
word("Can I speak in English?", "¿Puedo usar el inglés?"),
word("How wonderful!", "¡Qué bien!"),
word("How great!", "¡Qué bueno!"),
word("How delicious!", "¡Qué rico!"),
word("What a shame!", "¡Qué pena!"),
word("What a pity!", "¡Qué lástima!"),
word("I forgot my homework", "Me olvidé la tarea."),
word("Forgive me", "Perdóname"),
word("Apology, excuse informal", "Disculpa"),
word("Pardon me; Excuse me", "Con permiso"),
word("Apology, excuse formal", "Disculpe"),
word("Silence", "Silencio"),
word("You need to take notes", "Hay que tomar apuntes"),
word("There is no homework today.", "No hay tarea hoy."),
word("Open your laptops", "Abran sus portátiles"),
word("Be kind", "Sé amable"),
]
vocab_2_numbers = [
word("0", "cero"),
word("1", "uno"),
word("2", "dos"),
word("3", "tres"),
word("4", "cuatro"),
word("5", "cinco"),
word("6", "seis"),
word("7", "siete"),
word("8", "ocho"),
word("9", "nueve"),
word("10", "diez"),
word("11", "once"),
word("12", "doce"),
word("13", "trece"),
word("14", "catorce"),
word("15", "quince"),
word("16", "dieciséis"),
word("17", "diecisiete"),
word("18", "dieciocho"),
word("19", "diecinueve"),
word("20", "veinte"),
word("21", "veintiuno"),
word("22", "veintidós"),
word("23", "veintitrés"),
word("24", "veinticuatro"),
word("25", "veinticinco"),
word("26", "veintiséis"),
word("27", "veintisiete"),
word("28", "veintiocho"),
word("29", "veintinueve"),
word("30", "treinta"),
word("31", "treinta y uno"),
word("32", "treinta y dos"),
word("33", "treinta y tres"),
word("34", "treinta y cuatro"),
word("35", "treinta y cinco"),
word("36", "treinta y seis"),
word("37", "treinta y siete"),
word("38", "treinta y ocho"),
word("39", "treinta y nueve"),
word("40", "cuarenta"),
word("41", "cuarenta y uno"),
word("42", "cuarenta y dos"),
word("43", "cuarenta y tres"),
word("44", "cuarenta y cuatro"),
word("45", "cuarenta y cinco"),
word("46", "cuarenta y seis"),
word("47", "cuarenta y siete"),
word("48", "cuarenta y ocho"),
word("49", "cuarenta y nueve"),
word("50", "cincuenta"),
word("51", "cincuenta y uno"),
word("52", "cincuenta y dos"),
word("53", "cincuenta y tres"),
word("54", "cincuenta y cuatro"),
word("55", "cincuenta y cinco"),
word("56", "cincuenta y seis"),
word("57", "cincuenta y siete"),
word("58", "cincuenta y ocho"),
word("59", "cincuenta y nueve"),
word("60", "sesenta"),
word("61", "sesenta y uno"),
word("62", "sesenta y dos"),
word("63", "sesenta y tres"),
word("64", "sesenta y cuatro"),
word("65", "sesenta y cinco"),
word("66", "sesenta y seis"),
word("67", "sesenta y siete"),
word("68", "sesenta y ocho"),
word("69", "sesenta y nueve"),
word("70", "setenta"),
word("71", "setenta y uno"),
word("72", "setenta y dos"),
word("73", "setenta y tres"),
word("74", "setenta y cuatro"),
word("75", "setenta y cinco"),
word("76", "setenta y seis"),
word("77", "setenta y siete"),
word("78", "setenta y ocho"),
word("79", "setenta y nueve"),
word("80", "ochenta"),
word("81", "ochenta y uno"),
word("82", "ochenta y dos"),
word("83", "ochenta y tres"),
word("84", "ochenta y cuatro"),
word("85", "ochenta y cinco"),
word("86", "ochenta y seis"),
word("87", "ochenta y siete"),
word("88", "ochenta y ocho"),
word("89", "ochenta y nueve"),
word("90", "noventa"),
word("91", "noventa y uno"),
word("92", "noventa y dos"),
word("93", "noventa y tres"),
word("94", "noventa y cuatro"),
word("95", "noventa y cinco"),
word("96", "noventa y seis"),
word("97", "noventa y siete"),
word("98", "noventa y ocho"),
word("99", "noventa y nueve"),
word("100", "cien")
]
vocab_3_time = [
    word("It's one o'clock.", "Es la una."),
    word("It's two o'clock.", "Son las dos."),
    word("It's twelve o'clock.", "Son las doce."),
    word("It's midnight.", "Es la medianoche."),
    word("It's noon.", "Es el mediodía."),
    word("o'clock", "en punto"),
    word("at what time?", "¿a qué hora?"),
    word("a.m.", "de la mañana"),
    word("p.m.", "de la tarde"),
    word("p.m. (after 7)", "de la noche"),
    word("fifteen minutes", "quince minutos"),
    word("half an hour", "media hora"),
    word("minute", "el minuto"),
    word("hour", "la hora"),
    word("second", "el segundo"),
    word("day", "el día"),
    word("week", "la semana"),
    word("month", "el mes"),
    word("year", "el año"),
    word("What day is today?", "¿Qué día es hoy?"),
    word("Today is...", "Hoy es..."),
    word("tomorrow", "mañana"),
    word("yesterday", "ayer"),
    word("the day before yesterday", "anteayer"),
    word("the day after tomorrow", "pasado mañana"),
    word("Monday", "el lunes"),
    word("Tuesday", "el martes"),
    word("Wednesday", "el miércoles"),
    word("Thursday", "el jueves"),
    word("Friday", "el viernes"),
    word("Saturday", "el sábado"),
    word("Sunday", "el domingo"),
    word("January", "enero"),
    word("February", "febrero"),
    word("March", "marzo"),
    word("April", "abril"),
    word("May", "mayo"),
    word("June", "junio"),
    word("July", "julio"),
    word("August", "agosto"),
    word("September", "septiembre"),
    word("October", "octubre"),
    word("November", "noviembre"),
    word("December", "diciembre"),
    word("spring", "la primavera"),
    word("summer", "el verano"),
    word("autumn", "el otoño"),
    word("winter", "el invierno"),
    word("What is the date today?", "¿Cuál es la fecha de hoy?"),
    word("Today's date is...", "La fecha de hoy es el..."),
    word("the first (of the month)", "el primero"),
    word("the second", "el dos"),
    word("the third", "el tres"),
    word("the fourth", "el cuatro"),
    word("the fifth", "el cinco"),
    word("the sixth", "el seis"),
    word("the seventh", "el siete"),
    word("the eighth", "el ocho"),
    word("the ninth", "el nueve"),
    word("the tenth", "el diez"),
    word("the eleventh", "el once"),
    word("the twelfth", "el doce"),
    word("the thirteenth", "el trece"),
    word("the fourteenth", "el catorce"),
    word("the fifteenth", "el quince"),
    word("the sixteenth", "el dieciséis"),
    word("the seventeenth", "el diecisiete"),
    word("the eighteenth", "el dieciocho"),
    word("the nineteenth", "el diecinueve"),
    word("the twentieth", "el veinte"),
    word("the twenty-first", "el veintiuno"),
    word("the twenty-second", "el veintidós"),
    word("the twenty-third", "el veintitrés"),
    word("the twenty-fourth", "el veinticuatro"),
    word("the twenty-fifth", "el veinticinco"),
    word("the twenty-sixth", "el veintiséis"),
    word("the twenty-seventh", "el veintisiete"),
    word("the twenty-eighth", "el veintiocho"),
    word("the twenty-ninth", "el veintinueve"),
    word("the thirtieth", "el treinta"),
    word("the thirty-first", "el treinta y uno")
]
vocab_4_body_parts = [
    word("el brazo", "arm"),
    word("el cuerpo", "body"),
    word("la cara", "face"),
    word("la cabeza", "head"),
    word("el estómago", "stomach"),
    word("el hombro", "shoulder"),
    word("la pierna", "leg"),
    word("el pie", "foot"),
    word("la mano", "hand"),
    word("el dedo", "finger"),
    word("la rodilla", "knee"),
    word("la espalda", "back"),
    word("el diente", "tooth"),
    word("los dientes", "teeth"),
    word("el cuello", "neck"),
    word("el pelo", "hair"),
    word("el ojo", "eye"),
    word("los ojos", "eyes"),
    word("la oreja", "ear"),
    word("la nariz", "nose"),
    word("la boca", "mouth"),
    word("la lengua", "tongue")
]
vocab_5_class_objects = [
    word("el calendario", "the calendar"),
    word("el mapa", "the map"),
    word("el sacapuntas", "the pencil sharpener"),
    word("el lápiz", "the pencil"),
    word("el libro", "the book"),
    word("la silla", "the chair"),
    word("la mesa", "the table"),
    word("el bolígrafo, la pluma", "the pen"),
    word("el papel", "the paper"),
    word("la puerta", "the door"),
    word("la ventana", "the window"),
    word("la mochila", "the backpack"),
    word("el borrador", "the eraser"),
    word("el estudiante", "the student (male)"),
    word("la maestra o profesora", "the teacher or professor (female)"),
    word("el maestro o profesor", "the teacher or professor (male)"),
    word("la computadora", "the computer"),
    word("la bandera", "the flag"),
    word("la regla", "the ruler"),
    word("las tijeras", "the scissors"),
    word("los crayones", "the crayons"),
    word("el pegamento", "the glue"),
    word("los marcadores", "the markers"),
    word("¿Qué tienes en la escuela? Yo tengo...", "What do you have at school? I have..."),
    word("el gis, la tiza", "the chalk"),
    word("el pupitre", "the student desk"),
    word("el líquido corrector/correcto", "the whiteout"),
    word("la papelera", "the wastepaper basket"),
    word("el alfabeto/el abecedario", "the alphabet"),
    word("el altavoz", "the loudspeaker"),
    word("el teclado", "the keyboard"),
    word("el ratón", "the mouse"),
    word("la impresora", "the printer"),
    word("la grapadora", "the stapler"),
    word("la grapa", "the staple"),
    word("la calculadora", "the calculator"),
    word("la cartelera", "the bulletin board"),
    word("la cinta", "the tape"),
    word("la lámpara", "the lamp"),
    word("la luz", "the light"),
    word("la pared", "the wall"),
    word("el pincel", "the paintbrush"),
    word("la pintura", "the paint"),
    word("el piso", "the floor"),
    word("el cuaderno", "the notebook"),
    word("la libreta", "the notebook"),
    word("un cesto", "a basket"),
    word("la carpeta", "the folder"),
    word("el director", "the principal"),
    word("el cartel", "the poster"),
    word("la escuela", "the school"),
    word("el globo terrestre", "the globe"),
    word("la perforadora", "the hole puncher"),
    word("la goma de borrar", "the eraser"),
    word("la pizarra, el pizarrón", "the blackboard")
]











