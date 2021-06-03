import numpy as np
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
from PIL.ImageFilter import Kernel
from io import BytesIO

__author__ = 'Felipe V. Calderan'
__copyright__ = 'Copyright (C) 2021 Felipe V. Calderan'
__license__ = 'BSD 3-Clause "New" or "Revised" License'
__version__ = '1.0'

EQ_IMG = b'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'


def err_name_format():
    """Error that appears when something goes wrong while opening or saving"""
    sg.Popup('Invalid name or format. Fully supported formats:\n'
             'BMP, DIB, EPS, GIF, ICNS, ICO, IM, JPEG, MSP, PCX,\n'
             'PNG, PPM, SGI, SPIDER, TGA, TIFF, WebP, XBM',
             title='Error')


def err_type_format():
    """Error that appears when the parameters are invalid"""
    sg.Popup('Kernel, Scale and Offset must be floats and Rate must be int.',
        title='Error')


def help_message():
    """Small help message"""

    text1 = ['Skonvolve applies kernels to images. For each pixel (x,y):']
    text2 = ['where w are the kernel weights. if Scale = 0, it will be\n',
             'the sum of the kernel\'s elements.\n']

    layout = [[sg.Text(''.join(text1))],
              [sg.Image(data=BytesIO(EQ_IMG).getvalue())],
              [sg.Text(''.join(text2))],
              [sg.Text('\n'.join((f'Author:    {__author__}',
                                  f'Copyright: {__copyright__}',
                                  f'License:   {__license__}',
                                  f'Version:   {__version__}')))]]

    # Create the Window
    window = sg.Window( 'Help', layout, finalize=True,
        element_justification='left', font='Monospace')


def set_conv(
        window : sg.PySimpleGUI.Window, v : list, s : float, o : float, r : int
):
    """Convenience function to set the parameters values"""
    for i in range(25):
        window[f't{i}'].update(v[i])
    window['Scale'].update(s)
    window['Offset'].update(o)
    window['Rate'].update(r)


def main():
    # Create a layout for the window
    layout = [[sg.Canvas(key='plot_canvas')],
        *[[sg.Input('1' if i+5*j == 12 else '0', key=f't{i+5*j}', size=(5,1))
           for i in range(5)] for j in range(5)],
        [sg.Text('Scale:'), sg.Input('0', key='Scale', size=(5,1)),
         sg.Text('Offset:'), sg.Input('0', key='Offset', size=(5,1)),
         sg.Text('Rate:'), sg.Input('1', key='Rate',   size=(5,1))],
        [sg.Text('Preset:'),
         sg.Combo(['None', 'Average Blur', 'Gaussian Blur', 'Sharpen',
         'Edge Detect', 'Emboss', 'Brighten', 'Darken'],
         size=(20,1), key='ConvC', default_value='None', enable_events=True)],
        [sg.Input(key='_fileopen_', enable_events=True, visible=False)],
        [sg.Input(key='_filesave_', enable_events=True, visible=False)],
        [sg.FileBrowse('Open', size=(7,1), target='_fileopen_'),
         sg.FileSaveAs('Save', size=(7,1), target='_filesave_', disabled=True),
         sg.Button('Convolve', size=(7,1), disabled=True),
         sg.Button('Revert',   size=(7,1), disabled=True),
         sg.Button('Help',     size=(7,1))]]

    # Create the Window
    window = sg.Window( 'Skonvolve', layout, finalize=True,
        element_justification='center', font='Monospace')

    # Create the figure
    fig = plt.figure(figsize=(6, 6), tight_layout=True)
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Draw the figure in the GUI
    figure_canvas_agg = FigureCanvasTkAgg(fig, window['plot_canvas'].TKCanvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    fig_agg =  figure_canvas_agg

    # Loop until user quits the program
    while True:
        event, v = window.read()

        # Quit
        if event in (None, 'Cancel', 'Exit'):
            break

        # Show help message
        elif event == 'Help':
            help_message()

        # Choose prefab convolution
        elif event == 'ConvC':
            if v['ConvC'] == 'None':
                set_conv(
                    window,['0' if i!=12 else '1' for i in range(25)], 0, 0, 1
                )
            elif v['ConvC'] == 'Average Blur':
                set_conv(window, ['1' for i in range(25)], 0, 0, 10)
            elif v['ConvC'] == 'Gaussian Blur':
                vector = [1,  4,  6,  4, 1, 4, 16, 24, 16, 4, 6, 24, 36, 24, 6,
                          4, 16, 24, 16, 4, 1,  4,  6,  4, 1]
                set_conv(window, vector, 0, 0, 10)
            elif v['ConvC'] == 'Sharpen':
                vector = [0, 0, 0, 0, 0, 0, 0,-1, 0, 0, 0,-1, 5,-1, 0,
                          0, 0,-1, 0, 0, 0, 0, 0, 0, 0]
                set_conv(window, vector, 0, 0, 1)
            elif v['ConvC'] == 'Edge Detect':
                vector = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1,-4, 1, 0,
                          0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
                set_conv(window, vector, 0.5, 0, 1)
            elif v['ConvC'] == 'Emboss':
                vector = [0, 0, 0, 0, 0, 0,-2,-1, 0, 0, 0,-1, 1, 1, 0,
                          0, 0, 1, 2, 0, 0, 0, 0, 0, 0]
                set_conv(window, vector, 0, 0, 1)
            elif v['ConvC'] == 'Brighten':
                set_conv(
                    window,['0' if i!=12 else '1' for i in range(25)], 0, 32, 1
                )
            elif v['ConvC'] == 'Darken':
                set_conv(
                    window,['0' if i!=12 else '1' for i in range(25)], 0,-32, 1
                )

        # Open an image
        elif event == '_fileopen_':
            try:
                img = Image.open(v['Open'], 'r')
                img_m = img.copy()
                ax.imshow(img_m)
                fig_agg.draw()
                window['Save'].update(disabled=False)
                window['Convolve'].update(disabled=False)
                window['Revert'].update(disabled=False)
            except:
                err_name_format()

        # Apply convolution to an image
        elif event == 'Convolve':
            try:
                for _ in range(int(v['Rate']) if int(v['Rate']) > 0 else 0):
                    img_m = img_m.filter(
                    Kernel((5, 5), list(map(float,
                    (v['t0'], v['t1'], v['t2'], v['t3'], v['t4'],
                     v['t5'], v['t6'], v['t7'], v['t8'], v['t9'],
                     v['t10'],v['t11'],v['t12'],v['t13'],v['t14'],
                     v['t15'],v['t16'],v['t17'],v['t18'],v['t19'],
                     v['t20'],v['t21'],v['t22'],v['t23'],v['t24']))
                    ), None if v['Scale']=='0' else float(v['Scale']),
                    float(v['Offset'])))
                ax.imshow(img_m)
                fig_agg.draw()
            except:
                err_type_format()

        # Revert all the changes
        elif event == 'Revert':
            img_m = img.copy()
            ax.imshow(img_m)
            fig_agg.draw()

        # Save the image
        elif event == '_filesave_':
            try:
                img_m.save(v['Save'])
                sg.Popup('The image has been saved to the chosen location! :D')
            except:
                err_name_format()

    window.close()


if __name__ == '__main__':
    main()
