import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import os

from . import PLOT_DIR


def plot_productos(df):
    labels = [
        '(ID:{}) {}'.format(n[0], n[1][:10]) for n in zip(df['id'], df['nombre'])]
    print(labels)

    ax = plt.subplot(111)
    ax.bar([i for i in range(len(df['cantidad']))], height=df['cantidad'])
    ax.set_xticks([i for i in range(len(df['cantidad']))])
    ax.set_xticklabels(labels, rotation=45, rotation_mode="anchor", ha="right")
    plt.tight_layout()
    plt.show()


def grafica_productos_por_sucursal(df):
    fig = plt.figure()
    ax = plt.subplot(111)
    # Grafica vacía
    if df.shape[0] == 0:
        title = 'Artículos enviadas'
    else:
        nom_sucursal = df.iloc[0]['sucursal']
        anios = sorted([i for i in set(df['anio'])])

        # Años por categoría
        if 'categoria' in df.columns:
            categorias = set(df['categoria'])
            title = 'Artículos enviados a la sucursal\n{} (por categorías)'.format(
                nom_sucursal.title())
            plots = []
            last_plot = np.zeros(len(anios))
            for subdf in _iter_por_categorias(df):
                array_cantidad = np.array(subdf['cantidad'], dtype=int)
                plots.append(
                    ax.bar(anios, array_cantidad, bottom=last_plot))
                last_plot += array_cantidad
            ax.legend(plots, categorias)

        # Total de envíos
        else:
            title = 'Artículos enviados a la sucursal\n{}'.format(
                nom_sucursal.title())
            ax.bar(anios, df['cantidad'])

    ax.set_ylabel('Cantidad de artículos')
    ax.set_xlabel('Año')
    ax.set_xticks(range(min(anios), max(anios) + 1))

    plt.title(title)

    nombre_archivo = os.path.join(PLOT_DIR, 'grafica1.png')
    fig.savefig(nombre_archivo, dpi=150)

    return nombre_archivo


def grafica_productos_menos_vendidos(df):
    fig = plt.figure()

    anios = sorted([i for i in set(df['anio'])])
    nombres = []
    cantidad = []

    for a in anios:
        # Dataframe de un año
        subdf = df[df['anio'] == a]
        ser = subdf['cantidad_enviada']
        cantidad.append(ser[ser.index[0]])
        nombres_anio = []
        ser = subdf['id']
        nombres.append(mpatches.Patch(color='blue',
                                      label='{} - {}'.format(a, ','.join([str(n) for n in ser]))))

    plt.legend(title='ID de productos', handles=nombres)
    plt.ylabel('Cantidad Enviada')
    plt.xlabel('Año')
    plt.bar(anios, cantidad)
    plt.title('Productos menos vendidos en el tercer\ntrimestre de los años {} al año {}'.format(
        min(anios), max(anios)))
    plt.xticks(range(anios[0], anios[-1] + 1))

    nombre_archivo = os.path.join(PLOT_DIR, 'grafica3.png')
    fig.savefig(nombre_archivo, dpi=150)

    return nombre_archivo


def _iter_por_categorias(df):
    """Función auxiliar para crear dataframes por categorías. """
    nom_sucursal = df.iloc[0]['sucursal']
    categorias = set(df['categoria'])
    anios = set(df['anio'])
    for c in categorias:
        subdf = df[df['categoria'] == c]
        for a in anios:
            subanios = set([i for i in subdf['anio']])
            if a not in subanios:
                subdf = subdf.append({
                    'anio': a,
                    'categoria': c,
                    'sucursal': nom_sucursal,
                    'cantidad': 0
                }, ignore_index=True)
        yield subdf.sort_values('anio')
