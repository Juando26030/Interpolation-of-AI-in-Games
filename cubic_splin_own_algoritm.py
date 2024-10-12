import numpy as np
import matplotlib.pyplot as plt


def tridiagonal_solve(a, b, c, d):
    n = len(d)
    x = np.zeros(n)
    for i in range(1, n):
        m = a[i - 1] / b[i - 1]
        b[i] -= m * c[i - 1]
        d[i] -= m * d[i - 1]
    x[-1] = d[-1] / b[-1]
    for i in range(n - 2, -1, -1):
        x[i] = (d[i] - c[i] * x[i + 1]) / b[i]
    return x


def cubic_spline(x, y):
    n = len(x)
    h = np.diff(x)
    a = np.zeros(n - 1)
    b = np.zeros(n)
    c = np.zeros(n - 1)
    d = np.zeros(n)

    # Configurar el sistema tridiagonal
    for i in range(1, n - 1):
        b[i] = 2 * (h[i - 1] + h[i])
        a[i - 1] = h[i - 1]
        c[i] = h[i]
        d[i] = 3 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])

    # Condiciones de frontera natural
    b[0] = b[-1] = 1

    # Resolver el sistema tridiagonal
    k = tridiagonal_solve(a, b, c, d)

    def spline(t):
        i = np.searchsorted(x, t) - 1
        i = np.clip(i, 0, n - 2)
        dx = t - x[i]
        return (
                y[i] +
                k[i] * dx +
                (3 * (y[i + 1] - y[i]) / h[i]**2 - (k[i + 1] + 2 * k[i]) / h[i]) * dx**2 +
                (2 * (y[i] - y[i + 1]) / h[i]**3 + (k[i + 1] + k[i]) / h[i]**2) * dx**3
        )

    return spline


# Datos originales
years = np.array(
    [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
     2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])
ai_systems = np.array(
    [4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, np.nan, 6, 6, 6, 6, 6, 6, 6, np.nan, 6, 7, 9, 13, 16, np.nan, 27, 34, 37,
     41, 45, np.nan, 45])

# Filtrar los datos no nulos
mask = ~np.isnan(ai_systems)
years_known = years[mask]
ai_systems_known = ai_systems[mask]

# Crear la interpolación con splines cúbicas personalizadas
spline_func = cubic_spline(years_known, ai_systems_known)

# Generar puntos para una curva suave
years_smooth = np.linspace(years.min(), years.max(), 500)
ai_systems_smooth = np.array([spline_func(t) for t in years_smooth])

# Calcular los valores interpolados para los años originales
ai_systems_interpolated = np.array([spline_func(t) for t in years])

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
    plt.annotate(f'{value:.2f}', (year, value), textcoords="offset points", xytext=(0, 10), ha='center')

plt.show()

# Imprimir los valores interpolados para los años faltantes
missing_years = years[~mask]
interpolated_values = ai_systems_interpolated[~mask]
print("\nValores interpolados para los años faltantes:")
for year, value in zip(missing_years, interpolated_values):
    print(f"Año {year}: {value:.2f}")