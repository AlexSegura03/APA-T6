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

        if match.group('ampm'):
            if 'tarde' in match.group('ampm') or 'noche' in match.group('ampm'):
                if h < 12:
                    h += 12
            elif 'mañana' in match.group('ampm') and h == 12:
                h = 0

        # Control de minutos mayores de 59 (corrección simple)
        if m >= 60:
            h += m // 60
            m = m % 60

        return f'{h:02d}:{m:02d}'

    def reemplazos_especiales(text):
        # Casos tipo "4 y media de la tarde"
        text = re.sub(r'(\b\d{1,2})\s+y\s+media(?:\s+de\s+la\s+(mañana|tarde|noche))?',
                      lambda m: f'{int(m.group(1)) + (12 if m.group(2) in ("tarde", "noche") and int(m.group(1)) < 12 else 0):02d}:30',
                      text, flags=re.IGNORECASE)
        # Casos tipo "5 menos cuarto"
        text = re.sub(r'(\d{1,2})\s+menos\s+cuarto',
                      lambda m: f'{(int(m.group(1)) - 1) % 24:02d}:45',
                      text, flags=re.IGNORECASE)
        return text

    # Expresión regular principal
    patron = re.compile(
        r'(?P<h>\d{1,2})\s*(h|:)?\s*(?P<m>\d{1,2})?\s*(m|min|en punto)?(?:\s+de\s+la\s+(?P<ampm>mañana|tarde|noche))?',
        flags=re.IGNORECASE
    )

    with open(ficHoras, 'rt', encoding='utf-8') as f:
        lineas = f.readlines()

        nuevas_lineas = []
    for linia in lineas:
        linia = reemplazos_especiales(linia)
        nueva = patron.sub(normaliza, linia)
        if not nueva.endswith('\n'):
            nueva += '\n'
        nuevas_lineas.append(nueva)

    with open(ficHoras, 'wt', encoding='utf-8') as f:
        f.writelines(nuevas_lineas)
