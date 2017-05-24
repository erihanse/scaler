import numpy as np
import matplotlib.pyplot as plt
import random

def plot_graph(container_values, request_values):
    '''
    Plots the amount of containers and the amount of requests per second, from
    an interval which spans a minute. For now.
    '''
    fig, ax1 = plt.subplots()
    t = np.arange(0, 60, 1)
    y1 = container_values
    ax1.plot(t, y1, 'b-')
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('number of containers', color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    y2 = request_values
    ax2.plot(t, y2, 'r')
    ax2.set_ylabel('requests/s ', color='r')
    ax2.tick_params('y', colors='r')

    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    container_values = []
    request_values = []
    for i in range(0,60):
        randomNr = random.randint(5,20)
        container_values.append(randomNr)
        request_values.append(randomNr * 100 + random.randint(-10,10))
        # request_values.append(random.randint(15,30))

    plot_graph(container_values, request_values)