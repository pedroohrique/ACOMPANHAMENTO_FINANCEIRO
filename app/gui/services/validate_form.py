from datetime import datetime

def validar_formulaio(array):
    campos_obrigatorios = {
        "dt_gasto": lambda x: datetime.strptime(x, '%d/%m/%Y') <= datetime.today(),
        "valor": lambda x: x.replace('.', '', 1).isdigit(),
        "desc": lambda x: len(x.strip()) > 3,
        "desc_categoria": lambda x: x is not None,
        "desc_local": lambda x: len(x.strip()) > 3,
        "forma_pagamento": lambda x: x is not None,
        "flag_parcelamento": lambda x: x is not None and str(x).strip().upper() in ("S", "N"),
        "qt_parcelas": lambda x: x.isdigit() and int(x) >= 0
        }

    erros = []
    
    for campo in campos_obrigatorios:
        if campo not in array:
            erros.append(f"Campo obrigatório faltando: {campo}")
            
    for campo, valor in array.items():
        if campo in campos_obrigatorios and not campos_obrigatorios[campo](str(valor)):
            erros.append(f"Valor inválido para {campo}: {valor}")
    
    if erros:
        raise ValueError("\n".join(erros))
    
    return True