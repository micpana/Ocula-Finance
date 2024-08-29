import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
y = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
l, = plt.plot(x, y)
plt.axis([0, 2, 0, 9])

axcolor = 'lightgoldenrodyellow'
axpos = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)

spos = Slider(axpos, 'Pos', 0.1, 7.0)

def update(val):
    pos = spos.val
    ax.axis([pos, pos+2, 0, 9])
    fig.canvas.draw_idle()

spos.on_changed(update)

plt.show()