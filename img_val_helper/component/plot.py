import os

import matplotlib
import numpy as np

# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def save_plot_img(image, name):
    # figure = plt.figure()
    # plot = figure.add_subplot(1, 1, 1)
    # plot.imshow(image)
    # im = fig2img(figure)
    # return im

    plt.clf()
    fill_value = image.fill_value
    data = np.ma.masked_invalid(image[:]).astype(np.float)
    data[data == fill_value] = np.ma.masked
    data.filled(np.nan)
    plt.imshow(image)
    # plt.show()
    plt.savefig(name + '.png')
    return name + '.png'

# def fig2data(fig):
#     """
#     @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
#     @param fig a matplotlib figure
#     @return a numpy 3D array of RGBA values
#     """
#     # draw the renderer
#     fig.canvas.draw()
#
#     # Get the RGBA buffer from the figure
#     w, h = fig.canvas.get_width_height()
#     buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
#     buf.shape = (w, h, 4)
#
#     # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
#     buf = np.roll(buf, 3, axis=2)
#     return buf
#
#
# def fig2img(fig):
#     """
#     @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
#     @param fig a matplotlib figure
#     @return a Python Imaging Library ( PIL ) image
#     """
#     # put the figure pixmap into a numpy array
#     buf = fig2data(fig)
#     w, h, d = buf.shape
#     return Image.frombytes("RGBA", (w, h), buf)
