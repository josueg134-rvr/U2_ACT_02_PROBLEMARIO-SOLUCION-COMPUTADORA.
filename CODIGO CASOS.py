import math
from tabulate import tabulate

def calcular_y_mostrar_reporte():
    """
    Algoritmo para el cálculo de ejes bajo esfuerzos combinados
    Metodología: Diseño en Ingeniería Mecánica de Shigley.
    """
    
    # 1. BASE DE DATOS DE LOS CASOS
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
            'q': 0.82, 'qc': 0.85, 'Kt': 1.60, 'Kts': 1.35, 
            'Kf': 1.492, 'Kfs': 1.2975, 'criterio': 'Goodman'
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
        d, Ma, Mm, Ta, Tm = dts['d'], dts['Ma'], dts['Mm'], dts['Ta'], dts['Tm']
        Sut, Sy, Se, Kf, Kfs = dts['Sut'], dts['Sy'], dts['Se'], dts['Kf'], dts['Kfs']

        sig_a = Kf * (32 * Ma) / (math.pi * d**3)
        sig_m = Kf * (32 * Mm) / (math.pi * d**3)
        tau_a = Kfs * (16 * Ta) / (math.pi * d**3)
        tau_m = Kfs * (16 * Tm) / (math.pi * d**3)

        sig_a_p = math.sqrt(sig_a**2 + 3 * tau_a**2)
        sig_m_p = math.sqrt(sig_m**2 + 3 * tau_m**2)
        sig_max_p = math.sqrt((sig_m + sig_a)**2 + 3 * (tau_m + tau_a)**2)

        nvM = Sy / sig_max_p
        n_goodman = 1 / ((sig_a_p / Se) + (sig_m_p / Sut))
        
        A, B = sig_a_p / Se, sig_m_p / Sut
        n_gerber = ((-A + math.sqrt(A**2 + 4 * B**2)) / (2 * B**2)) if B > 0 else Se / sig_a_p

        n_soderberg = 1 / ((sig_a_p / Se) + (sig_m_p / Sy))
        n_asme = 1 / math.sqrt((sig_a_p / Se)**2 + (sig_m_p / Sy)**2)

        n_final = n_goodman if dts['criterio'] == 'Goodman' else n_gerber
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
