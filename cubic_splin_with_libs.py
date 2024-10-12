import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Datos originales
years = np.array([1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])
ai_systems = np.array([4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, np.nan, 6, 6, 6, 6, 6, 6, 6, np.nan, 6, 7, 9, 13, 16, np.nan, 27, 34, 37, 41, 45, np.nan, 45])

# Filtrar los datos no nulos
mask = ~np.isnan(ai_systems)
years_known = years[mask]
ai_systems_known = ai_systems[mask]

# Crear la interpolación con splines cúbicas
cs = CubicSpline(years_known, ai_systems_known)

# Generar puntos para una curva suave
years_smooth = np.linspace(years.min(), years.max(), 500)
ai_systems_smooth = cs(years_smooth)

# Calcular los valores interpolados para los años originales
ai_systems_interpolated = cs(years)

# Crear la gráfica
plt.figure(figsize=(12, 6))
plt.scatter(years_known, ai_systems_known, color='blue', label='Datos conocidos')
plt.plot(years_smooth, ai_systems_smooth, color='red', label='Interpolación por splines cúbicas')
plt.scatter(years[~mask], ai_systems_interpolated[~mask], color='green', label='Valores interpolados')

plt.xlabel('Año')
plt.ylabel('Número acumulativo de sistemas de IA')
plt.title('Interpolación por Splines Cúbicas de Sistemas de IA en Videojuegos (1990-2024)')
plt.legend()
plt.grid(True)

# Mostrar los valores interpolados
for year, value in zip(years[~mask], ai_systems_interpolated[~mask]):
    plt.annotate(f'{value:.2f}', (year, value), textcoords="offset points", xytext=(0,10), ha='center')

plt.show()

# Imprimir los valores interpolados para los años faltantes
missing_years = years[~mask]
interpolated_values = ai_systems_interpolated[~mask]
print("\nValores interpolados para los años faltantes:")
for year, value in zip(missing_years, interpolated_values):
    print(f"Año {year}: {value:.2f}")