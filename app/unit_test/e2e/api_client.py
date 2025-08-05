def get_post_test_payload(str1:str, str2: str, str3:str):
    return  {
        "primer_campo": str1,
        "segundo_campo": str2,
        "tercer_campo": str3
    }

def get_post_test_response():
    return {
        'estatus': 1,
        'mensaje': 'OK',
        'datos': {
            'valor1': 100,
            'valor2': 'Valor dado de alta correctamente'
        }
    }

def get_post_add_payload(nombre: str, comentarios: str):
    return {
        "nombre": nombre,
        "comentarios": comentarios
    }

def get_post_add_response(id: int):
    return {
        "estatus": 1,
        "mensaje": "OK",
        "datos": {
            "valor1": id,
            "valor2": "Valor dado de alta correctamente"
        }
    }

def get_method_response(id: int, mensaje: str):
    return {
        'estatus': 1,
        'mensaje': "OK",
        'datos': {
            'valor1': id,
            'valor2': mensaje,
        }
    }