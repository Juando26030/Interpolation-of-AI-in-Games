import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

# Datos originales completos
years = [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
systems = [4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 9, 13, 16, 24, 27, 34, 37, 41, 45, 45, 45]

# Datos para interpolación (excluyendo los años que queremos predecir)
interp_years = [y for y in years if y not in [2003, 2011, 2017, 2023]]
interp_systems = [s for y, s in zip(years, systems) if y not in [2003, 2011, 2017, 2023]]

# Crear el spline cúbico
cs = CubicSpline(interp_years, interp_systems)

# Generar años completos para la interpolación
all_years = np.arange(1990, 2025)
interpolated_systems = cs(all_years)

# Graficar resultados
plt.figure(figsize=(12, 6))
plt.plot(all_years, interpolated_systems, label='Interpolación', color='r')
plt.scatter(years, systems, label='Datos originales', color='b')
plt.xlabel('Año')
plt.ylabel('Número acumulativo de sistemas de IA')
plt.title('Interpolación por Splines Cúbicas de Sistemas de IA en Videojuegos')
plt.legend()
plt.grid(True)

# Calcular y mostrar errores para los años faltantes
missing_years = [2003, 2011, 2017, 2023]
original_values = [6, 6, 24, 45]
errors = []

for year, original in zip(missing_years, original_values):
    interpolated_value = cs(year)
    error = abs(original - interpolated_value)
    errors.append(error)
    plt.text(year, interpolated_value, f'{year}: {interpolated_value:.2f}\nError: {error:.2f}',
             verticalalignment='bottom', horizontalalignment='center')

plt.show()

# Imprimir valores interpolados y errores para los años faltantes
print("Valores interpolados y errores para los años faltantes:")
for year, original, interpolated, error in zip(missing_years, original_values, cs(missing_years), errors):
    print(f"{year}: Original: {original}, Interpolado: {interpolated:.2f}, Error: {error:.2f}")

# Calcular error medio absoluto
mae = np.mean(errors)
print(f"\nError Medio Absoluto: {mae:.2f}")