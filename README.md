# Datos de Ciencia: NumPy con una curva de luz

Una serie de videos para aprender [NumPy](https://numpy.org/), la librería de Python para trabajar con
muchos números a la vez, usando **datos reales de un telescopio espacial** de principio a fin. Video a
video, construimos desde cero una **curva de luz**: la gráfica del brillo de una estrella a lo largo
del tiempo, en la que se ve pasar a un planeta por delante.

Este repositorio tiene todo lo necesario para seguir los videos: los notebooks, los datos y un pequeño
módulo para graficar.

## Antes de empezar

Solo necesitas **Python básico**: listas, bucles `for`, funciones. Si te falta, empieza por el video
[Introducción a Python](https://youtu.be/EZYPjmSQuQk) del canal y su notebook,
[Fundamentos de Python](https://github.com/Datos-De-Ciencia/fundamentos-de-python).

## Los datos

Vienen de [TESS](https://science.nasa.gov/mission/tess/), un telescopio espacial de la NASA que busca
planetas alrededor de otras estrellas, y cuyos datos son públicos.

- Son **1440 fotos** de la estrella **WASP-18**, de 11 × 11 píxeles cada una, tomadas cada 2 minutos
  durante 2 días. Cada píxel es un número: cuánta luz llegó a ese punto.
- La estrella tiene un planeta, [WASP-18 b](https://science.nasa.gov/exoplanet-catalog/wasp-18-b/),
  que le da una vuelta en unas 22 horas. Cada vez que pasa por delante, la estrella se ve alrededor
  de un 1 % más oscura durante unas dos horas. En estos 2 días pasa dos veces.
- Algunas fotos salieron mal y vienen vacías (`nan`), y la luz del fondo del cielo sigue incluida. No
  es un descuido: lidiar con eso también es parte de la serie.

| Archivo | Forma y tipo | Qué es |
|---|---|---|
| `data/flux_cube.npy` | `(1440, 11, 11)`, `float32` | El brillo de cada píxel en cada foto |
| `data/time.npy` | `(1440,)`, `float64` | Cuándo se tomó cada foto, en días desde la primera |
| `data/aperture_mask.npy` | `(11, 11)`, `bool` | Qué píxeles pertenecen a la estrella (28 en total) |

Los tres juntos ocupan menos de 1 MB, así que cargan al instante en cualquier computador.

## Contenido

Un notebook por video, en `notebooks/`. Se agregan a medida que se publican los videos.

| # | Tema | Notebook | Video |
|---|---|---|---|
| 1 | Por qué arrays + `np.load` | [`01-por-que-arrays.ipynb`](notebooks/01-por-que-arrays.ipynb) | Enlace próximamente |
| 2 | Forma, ejes y `dtype` | [`02-forma-ejes-dtype.ipynb`](notebooks/02-forma-ejes-dtype.ipynb) | Enlace próximamente |
| 3 | Indexación | Próximamente | Próximamente |
| 4 | Copias y vistas | Próximamente | Próximamente |
| 5 | Ufuncs y agregaciones: aparece la curva de luz | Próximamente | Próximamente |
| 6 | Broadcasting | Próximamente | Próximamente |
| 7 | Datos faltantes | Próximamente | Próximamente |
| 8 | Números aleatorios | Próximamente | Próximamente |

Al final de cada sección de cada notebook hay **prompts de profundización**: preguntas para hacerle
a tu IA de confianza y seguir aprendiendo más allá del video.

## Cómo crear el ambiente

Necesitas Python 3.12 o más reciente. Si no tienes nada instalado, estos videos del canal te guían:

- [Instalación de UV](https://youtu.be/TJor7z8g8FA?si=QT2XVKeC29dYyDts)
- [Cómo instalar Anaconda y Jupyter](https://youtu.be/YzOLOlH1jQk?si=2hFk6aAh8gCoMvuo)
- [VS Code + Jupyter Notebooks](https://youtu.be/rL1usXq4bgE?si=2b5REnUzVBMDxWfF)

### Opción 1: con UV (recomendada)

```bash
git clone https://github.com/Datos-De-Ciencia/series-numpy-curva-de-luz.git
cd series-numpy-curva-de-luz
uv sync
```

`uv sync` crea el ambiente en la carpeta `.venv` con las versiones exactas de `uv.lock`.

### Opción 2: con Conda o pip

```bash
git clone https://github.com/Datos-De-Ciencia/series-numpy-curva-de-luz.git
cd series-numpy-curva-de-luz

conda create -n numpy-curva-de-luz python=3.12
conda activate numpy-curva-de-luz
pip install -e .
```

Sin Conda, lo mismo funciona dentro de cualquier ambiente virtual de Python con `pip install -e .`.

### Comprobar que todo funciona

Desde la carpeta del repositorio.

**Con UV:**

```bash
uv run python -c "import numpy as np; print(np.load('data/flux_cube.npy').shape)"
```

**Con Conda o pip** (con el ambiente activado):

```bash
python -c "import numpy as np; print(np.load('data/flux_cube.npy').shape)"
```

En los dos casos debe imprimir `(1440, 11, 11)`.

### Abrir los notebooks

- **En VS Code:** abre la carpeta del repositorio, abre un notebook de `notebooks/` y elige como
  kernel el ambiente que acabas de crear (`.venv` o `numpy-curva-de-luz`).
- **En el navegador, con Jupyter:** el ambiente no trae Jupyter para mantenerlo liviano. Con UV,
  ábrelo sin instalarlo en el ambiente: `uv run --with jupyter jupyter lab`. Con Conda o pip:
  `pip install jupyterlab` y luego `jupyter lab`.

Los notebooks cargan los datos con rutas como `../data/flux_cube.npy`, así que hay que abrirlos desde
su carpeta `notebooks/`, sin moverlos.

## Gráficos: `plot_helpers`

La serie enseña NumPy, no a graficar, así que los gráficos vienen hechos. El ambiente instala el
módulo `plot_helpers.py`, y desde cualquier notebook basta con:

```python
from plot_helpers import plot_frame, plot_light_curve

plot_frame(cube[0])                    # una foto de la estrella
plot_frame(cube[0], mask=mask)         # ...con los píxeles de la estrella marcados
plot_frame(cube[0], highlight=(5, 5))  # ...con un píxel (fila, columna) resaltado en rojo
plot_light_curve(time, brightness)     # el brillo a lo largo del tiempo
```

## Estructura del repositorio

```
series-numpy-curva-de-luz/
├── data/               ← los datos de la serie, listos para np.load
├── notebooks/          ← un notebook por video
├── plot_helpers.py     ← gráficos listos para usar
├── prepare_data.py     ← cómo se construyeron los datos a partir del archivo original de TESS
├── verify_data.py      ← comprobaciones de los datos
├── pyproject.toml      ← dependencias (sirve para UV, pip o Conda)
└── uv.lock             ← versiones exactas para UV
```

## De dónde salen los datos (opcional)

Los `.npy` ya vienen listos; no hace falta descargar nada. Si quieres saber exactamente qué se le hizo
al archivo original, está todo en `prepare_data.py`:

- **Archivo original:** `tess2018234235059-s0002-0000000100100827-0121-s_tp.fits` (48 MB), del archivo
  público de TESS en [MAST](https://archive.stsci.edu/missions-and-data/tess). Descarga directa:
  `https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:TESS/product/tess2018234235059-s0002-0000000100100827-0121-s_tp.fits`
- **Qué se le hizo:**
  1. Se recortaron 2 días (1440 fotos) con dos pasos del planeta, para que los datos pesen poco.
  2. Se le devolvió a cada foto la luz del fondo del cielo que la misión había restado, para poder
     restarla en la serie.
  3. Las fotos que la misión marcó como no confiables se convirtieron en `nan`, en vez de borrarlas.
  4. El tiempo se cambió para que empiece en 0 y esté en días.
  5. La máscara de la estrella es la que calcula la propia misión; se guardó tal cual.

Para reconstruir los datos desde cero (descarga el archivo original):

```bash
uv sync --extra prep
uv run python prepare_data.py
uv run python verify_data.py
```

## Créditos y licencia

- Datos: misión TESS de la NASA, obtenidos del Mikulski Archive for Space Telescopes (MAST) del Space
  Telescope Science Institute. La misión TESS está financiada por el Science Mission Directorate de
  la NASA.
- Código y notebooks: [Datos de Ciencia](https://github.com/Datos-De-Ciencia), bajo la licencia
  Apache 2.0 (ver [`LICENSE`](LICENSE)).
