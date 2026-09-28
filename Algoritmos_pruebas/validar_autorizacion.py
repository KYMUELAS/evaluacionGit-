"""
validar_autorizacion.py
------------------------
Simula la lógica del microservicio "ms-autorizaciones": decide si un
procedimiento médico puede autorizarse según el plan del afiliado y
el costo del procedimiento frente al tope de cobertura anual restante.
"""

# Tope máximo de cobertura anual según el tipo de plan del afiliado (en COP)
TOPES_COBERTURA = {
    "basico": 2_000_000,
    "intermedio": 5_000_000,
    "premium": 15_000_000,
}


def validar_autorizacion(nombre_paciente, tipo_plan, costo_procedimiento, cobertura_usada):
    # 1. Validar que el plan exista en la tabla de topes
    tipo_plan = tipo_plan.lower()
    if tipo_plan not in TOPES_COBERTURA:
        return {
            "autorizado": False,
            "motivo": f"Tipo de plan '{tipo_plan}' no reconocido.",
            "cobertura_restante": None,
        }

    tope_anual = TOPES_COBERTURA[tipo_plan]
    cobertura_disponible = tope_anual - cobertura_usada

    # 2. Validar que el paciente aún tenga cobertura disponible
    if cobertura_disponible <= 0:
        return {
            "autorizado": False,
            "motivo": f"{nombre_paciente} ya agotó la cobertura anual de su plan {tipo_plan}.",
            "cobertura_restante": 0,
        }

    # 3. Comparar el costo del procedimiento contra la cobertura disponible
    if costo_procedimiento <= cobertura_disponible:
        return {
            "autorizado": True,
            "motivo": "Procedimiento autorizado: dentro del tope de cobertura del plan.",
            "cobertura_restante": cobertura_disponible - costo_procedimiento,
        }
    else:
        faltante = costo_procedimiento - cobertura_disponible
        return {
            "autorizado": False,
            "motivo": f"Cobertura insuficiente: faltan ${faltante:,.0f} para cubrir el procedimiento.",
            "cobertura_restante": cobertura_disponible,
        }


if __name__ == "__main__":
    casos_de_prueba = [
        ("Juan Pérez", "basico", 1_500_000, 800_000),
        ("Maria Gómez", "intermedio", 4_000_000, 4_500_000),
        ("Carlos Ruiz", "premium", 6_000_000, 3_000_000),
    ]
    for nombre, plan, costo, usado in casos_de_prueba:
        print(f"{nombre} ({plan}) -> {validar_autorizacion(nombre, plan, costo, usado)}")