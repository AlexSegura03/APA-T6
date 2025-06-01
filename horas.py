'''
    Sexta tarea de APA - Expresiones regulares 
    Nombre y apellidos: Àlex Segura Medina

    Análisis de expresiones horarias
'''

import re

def normalizaHoras(ficHoras):
    """
    Convierte expresiones horarias informales del fichero a formato HH:MM (de 00:00 a 23:59).
    Sobrescribe el fichero con las horas normalizadas.
    """
    def normaliza(match):
        h = int(match.group('h'))
        m = match.group('m')
        m = int(m) if m else 0
        ampm = match.group('ampm')

        # Detectar errores: minutos mal formateados, horas inválidas
        if m >= 60 or h >= 24 or (ampm == 'tarde' and h < 12 and h >= 12):
            return match.group(0)  # dejar sin modificar

        if ampm:
            if ampm in ['tarde', 'noche'] and h < 12:
                h += 12
            elif ampm == 'mañana' and h == 12:
                h = 0
            elif ampm == 'noche' and h == 12:
                h = 0

        return f'{h:02d}:{m:02d}'

    def reemplaza_otros_formatos(texto):
        # 1. 'x y media de la tarde'
        texto = re.sub(
            r'(?<!\d)(\d{1,2})\s+y\s+media\s+de\s+la\s+(mañana|tarde|noche)',
            lambda m: f"{int(m.group(1)) + (12 if m.group(2) in ['tarde', 'noche'] and int(m.group(1)) < 12 else 0):02d}:30",
            texto
        )

        # 2. 'x menos cuarto'
        texto = re.sub(
            r'(?<!\d)(\d{1,2})\s+menos\s+cuarto',
            lambda m: f"{(int(m.group(1)) - 1) % 24:02d}:45",
            texto
        )

        # 3. 'x en punto'
        texto = re.sub(
            r'(?<!\d)(\d{1,2})\s+en\s+punto',
            lambda m: f"{int(m.group(1)):02d}:00",
            texto
        )

        # 4. '12 de la noche'
        texto = re.sub(
            r'12\s+de\s+la\s+noche',
            '00:00',
            texto
        )

        return texto

    # Patrón principal para 'hh', 'hh:mm', 'hhhm', etc.
    patron = re.compile(
        r'(?<!\d)(?P<h>\d{1,2})\s*(h|:)?\s*(?P<m>\d{1,2})?\s*(m|min)?(?:\s+de\s+la\s+(?P<ampm>mañana|tarde|noche))?',
        flags=re.IGNORECASE
    )

    with open(ficHoras, 'rt', encoding='utf-8') as f:
        lineas = f.readlines()

    nuevas_lineas = []
    for linea in lineas:
        original = linea
        linea = reemplaza_otros_formatos(linea)
        linea = patron.sub(normaliza, linea)

        if not linea.endswith('\n'):
            linea += '\n'
        nuevas_lineas.append(linea)

    with open(ficHoras, 'wt', encoding='utf-8') as f:
        f.writelines(nuevas_lineas)
