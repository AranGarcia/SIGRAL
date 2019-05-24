import matplotlib.pyplot as plt


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
