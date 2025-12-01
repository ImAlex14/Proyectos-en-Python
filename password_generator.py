import random, secrets
import re
import string

data_types = ["caps", "numbers", "symbols"]
data_separators = r'[,\s;/&\+]+'

def separate_choices(s, allowed):
    if not s:
        return []
    if re.search(data_separators, s): # busca si hay separadores en la cadena
        parts = re.split(data_separators, s) # divide la cadena en las diferentes expresiones segun los separadores
        return [p for p in (p.strip() for p in parts) if p] 
        # elimina todos los espacios vacios al principio y final de todas las expresiones, asi como tambien aquellas expresiones vacias
    
    # No hay separadores -> intentar greedy match por tokens permitidos
    """
    En caso de que no hayan separadores usamos greedy match por tokens para que a partir de un indice un motor de busqueda intenta que un cuantificador
    coincida con la coincidencia mas larga, es decir la mayor cantidad de tokens (letras). 
    """
    allowed_sorted = sorted(allowed, key=len, reverse=True)
    parts = []
    pos = 0
    n = len(s)
    while pos < n:
        matched = False
        for token in allowed_sorted:
            if s.startswith(token, pos):
                parts.append(token)
                pos += len(token)
                matched = True
                break
        if not matched:
            # fallback: tomar el resto como token único (se detectará como inválido luego)
            parts.append(s[pos:])
            break
    return parts
    
def validate(choices, allowed):
    clean_choices = separate_choices(choices, data_types)
    chset = set(clean_choices)
    valid_set = set(allowed)
    invalid = chset.difference(allowed)
    valid = chset.intersection(allowed)
    return invalid, valid


str_size = int(input("How many caracters do you want? "))
data_input = input(f"Write {data_types} or a combination of them ")
clean_input = data_input.strip().lower()
invalid, valid = validate(clean_input, data_types)

if invalid:
    print(f"invalid choice, please write one or more of options {data_types} using {data_separators} to separate each one")
else:
    charset = []
    letras = []
    charset.append(string.ascii_lowercase)
    if "caps" in valid:
        charset.append(string.ascii_uppercase)
    if "numbers" in valid:
        charset.append(string.digits)
    if "symbols" in valid:
        charset.append(string.punctuation)
    for _ in range(str_size):
        letras.append(random.choice(random.choice(charset))) # usamos secrets choice para tener entropia criptografica y hacer mas aleatorios los resultados
    result = "".join(letras)
    print(result)
