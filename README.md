# U2_ACT_02_PROBLEMARIO-SOLUCION-COMPUTADORA.
# Cálculo de Esfuerzos y Factor de Diseño en Ejes Rotatorios
Este repositorio contiene el desarrollo de un algoritmo en Python para el análisis de esfuerzos y cálculos realizado para la materia de Diseño de Elementos Mecanicos. El programa permite resolver los casos planteados en la actividad U2_ACT_02_PROBLEMARIO SOLUCIÓN COMPUTADORA.
# Caracteristicas agregadas en el repositorio
- Calculo de la sensibilidad de la muesca
- Factores de concentración de esfuerzo
- Esfuerzos normales y cortantes (medios y alternantes)
- Esfuerzos equivalentes de Von Mises
- Factores de diseño usando criterios Goodman, Soderberg, Gerber y ASME
# Tecnologías Utilizadas 
- Python 3
- numpy
- Matemáticas

import math
from tabulate import tabulate

def calcular_y_mostrar_reporte():
    """
    Algoritmo para el cálculo de ejes bajo esfuerzos combinados
    Metodología: Diseño en Ingeniería Mecánica de Shigley.
    """
    
    # 1. BASE DE DATOS DE LOS CASOS (Configurada según U2_ANEXO CASOS)
    # ------------------------------------------------------------------
    casos = {
        "TABLA 1: SOLUCIÓN DEL CASO 1": {
            'd': 1.10, 'Ma': 1260.0, 'Mm': 0.0, 'Ta': 0.0, 'Tm': 1100.0,
            'Sut': 105000.0, 'Sy': 82000.0, 'Se': 30000.0,
            'q': 0.85, 'qc': 0.88, 'Kt': 1.68, 'Kts': 1.48, 
            'Kf': 1.578, 'Kfs': 1.4224, 'criterio': 'Goodman'
        },
        "TABLA 2: SOLUCIÓN DEL CASO 2": {
            'd': 1.10, 'Ma': 1260.0, 'Mm': 0.0, 'Ta': 0.0, 'Tm': 1100.0,
            'Sut': 105000.0, 'Sy': 82000.0, 'Se': 30000.0,
            'q': 0.85, 'qc': 0.88, 'Kt': 1.68, 'Kts': 1.48,
            'Kf': 1.578, 'Kfs': 1.4224, 'criterio': 'Goodman'
        },
        "TABLA 3: SOLUCIÓN DEL CASO 3": {
            'd': 0.10, 'Ma': 70.0, 'Mm': 55.0, 'Ta': 45.0, 'Tm': 35.0,
            'Sut': 700e6, 'Sy': 560e6, 'Se': 210e6,
            'q': 'N/A', 'qc': 'N/A', 'Kt': 'N/A', 'Kts': 'N/A',
            'Kf': 2.2, 'Kfs': 1.8, 'criterio': 'Gerber'
        }
    }

    print("="*80)
    print(" REPORTE DE CÁLCULO: DISEÑO DE EJES ".center(80))
    print("="*80)

    for titulo, dts in casos.items():
        # Extracción de variables
        d, Ma, Mm, Ta, Tm = dts['d'], dts['Ma'], dts['Mm'], dts['Ta'], dts['Tm']
        Sut, Sy, Se, Kf, Kfs = dts['Sut'], dts['Sy'], dts['Se'], dts['Kf'], dts['Kfs']

        # d) Esfuerzos nominales (Flexión y Torsión) [cite: 14, 69]
        sig_a = Kf * (32 * Ma) / (math.pi * d**3)
        sig_m = Kf * (32 * Mm) / (math.pi * d**3)
        tau_a = Kfs * (16 * Ta) / (math.pi * d**3)
        tau_m = Kfs * (16 * Tm) / (math.pi * d**3)

        # e) Esfuerzos principales de Von Mises [cite: 15, 70]
        sig_a_p = math.sqrt(sig_a**2 + 3 * tau_a**2)
        sig_m_p = math.sqrt(sig_m**2 + 3 * tau_m**2)

        # f) Esfuerzo máximo de Von Mises [cite: 16, 71]
        sig_max_p = math.sqrt((sig_m + sig_a)**2 + 3 * (tau_m + tau_a)**2)

        # g) Factor de diseño de Von Mises (Fluencia) [cite: 17, 72]
        nvM = Sy / sig_max_p

        # h) Factores de diseño por fatiga [cite: 18, 73]
        n_goodman = 1 / ((sig_a_p / Se) + (sig_m_p / Sut))
        
        # Gerber (Cálculo cuadrático para Caso 3)
        A = sig_a_p / Se
        B = sig_m_p / Sut
        if B > 0:
            n_gerber = (-A + math.sqrt(A**2 + 4 * B**2)) / (2 * B**2)
        else:
            n_gerber = Se / sig_a_p

        n_soderberg = 1 / ((sig_a_p / Se) + (sig_m_p / Sy))
        n_asme = 1 / math.sqrt((sig_a_p / Se)**2 + (sig_m_p / Sy)**2)

        # Selección del criterio solicitado por el anexo
        n_final = n_goodman if dts['criterio'] == 'Goodman' else n_gerber

        # CONSTRUCCIÓN DE LA TABLA (Punto 98-100) 
        unidad = "psi" if dts['Sut'] > 1000000 or dts['Sut'] == 105000 else "Pa"
        
        tabla_resultados = [
            ["a) Sensibilidad (q, qc)", f"q={dts['q']}, qc={dts['qc']}"],
            ["b) Factores Kt, Kts", f"Kt={dts['Kt']}, Kts={dts['Kts']}"],
            ["c) Factores Kf, Kfs", f"{Kf:.3f}, {Kfs:.3f}"],
            ["d) Esf. Nominales ("+unidad+")", f"sa:{sig_a:.2e}, tm:{tau_m:.2e}"],
            ["e) Von Mises Princ. ("+unidad+")", f"sa':{sig_a_p:.2e}, sm':{sig_m_p:.2e}"],
            ["f) Von Mises Máximo", f"{sig_max_p:.2e}"],
            ["g) Factor Fluencia (nvM)", f"{nvM:.4f}"],
            ["h) Criterio "+dts['criterio'], f"{n_final:.4f}"],
            ["i) Otros (Soderberg/ASME)", f"S:{n_soderberg:.3f} | A:{n_asme:.3f}"]
        ]

        print(f"\n{titulo}")
        print(tabulate(tabla_resultados, headers=["Inciso / Concepto", "Resultado Final"], tablefmt="fancy_grid"))

if __name__ == "__main__":
    calcular_y_mostrar_reporte()
