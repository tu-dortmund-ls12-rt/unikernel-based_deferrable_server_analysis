import matplotlib.pyplot as plt


def plot(data, name, xticks=None, title=''):
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.boxplot(data)
    if xticks is not None:
        plt.xticks(list(range(1, len(xticks) + 1)), xticks)
    plt.show()
