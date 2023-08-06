"""
PySimpleGUI Reskinner Plugin

https://github.com/definite_d/psg_reskinner/
Enables changing the theme of a PySimpleGUI window on the fly without the need for re-instantiating the window

Copyright (c) 2022 Divine Afam-Ifediogor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# VERSIONING
__version__ = '2.0.34'

# IMPORTS
import tkinter as tk
from PySimpleGUI.PySimpleGUI import Window, theme_text_color, theme_slider_color, theme_progress_bar_color, theme_list, \
    theme_button_color, theme_background_color, theme_input_background_color, theme, theme_input_text_color, \
    theme_text_element_background_color, ttk_part_mapping_dict
from colour import web2hsl, hsl2web
from random import choice as rc
from tkinter.ttk import Style


# CONSTANTS
NON_GENERIC_ELEMENTS = [
    'progress',
    'tabgroup',
    'table',
    'tree',
    'button',
    'text',
    'multiline',
    'listbox',
    'spin',
    'horizontalseparator',
    'verticalseparator',
    'sizegrip',
]
WINDOW_THEME_MAP = {}


# UTILITY FUNCTIONS
def _check_if_generics_apply(element_name: str) -> bool:
    """
    Internal use only.

    Checks if a given element should undergo the generic config tweaks.

    If the element affected by the non-generic elements blacklist, it returns False.

    :param element_name: The name of the element
    :return: bool
    """
    valid = True
    for case in NON_GENERIC_ELEMENTS:
        if case in element_name:
            valid = False
            break
    return valid


def _reverse_dict(input_dict: dict) -> dict:
    """
    Internal use only.

    Takes in a dict and returns a copy of it with the places of its keys and values swapped.

    :param input_dict: The source dictionary.
    :return: dict
    """
    result = {str(key): value for key, value in list(input_dict.items())}
    return result


def _configure_ttk_scrollbar_style(style_name, styler) -> None:
    """
    Internal use only.
    
    Gets the colors that would be used to create a ttk scrollbar based on how it's done in the PySimpleGUI source.

    :return: None
    """

    mapper = {'Background Color': theme_background_color(),
              'Button Background Color': theme_button_color()[1],
              'Button Text Color': theme_button_color()[0],
              'Input Element Background Color': theme_input_background_color(),
              'Input Element Text Color': theme_input_text_color(),
              'Text Color': theme_text_color(),
              'Slider Color': theme_slider_color()}

    trough_color = mapper[ttk_part_mapping_dict['Trough Color']]
    frame_color = mapper[ttk_part_mapping_dict['Frame Color']]
    background_color = mapper[ttk_part_mapping_dict['Background Color']]
    arrow_color = mapper[ttk_part_mapping_dict['Arrow Button Arrow Color']]

    styler.configure(style_name, troughcolor=trough_color, framecolor=frame_color, bordercolor=frame_color)
    styler.map(style_name,
        background=[("selected", background_color), ('active', arrow_color), ('background', background_color),
                    ('!focus', background_color)])
    styler.map(style_name, arrowcolor=[("selected", arrow_color), ('active', background_color),
                                       ('background', background_color), ('!focus', arrow_color)])


# RESKIN FUNCTION
def reskin(
        window: Window,
        new_theme: str,
        theme_function,
        lf_table: dict,
        set_future: bool = False,
        exempt_element_keys: list = None) -> None:
    """
    Applies the theme instantaneously to the specified window. This is where the magic happens.

    :param window: The window to work on.
    :param new_theme: The name of the new theme, as you would pass it to your `theme()` call.
    :param theme_function: The PySimpleGUI `theme()` function object itself. Pass it without parentheses.
    :param lf_table: The `LOOK_AND_FEEL_TABLE` constant from your PySimpleGUI import.
    :param set_future: False by default. If set to `True`, future windows will also use the new theme.
    :param exempt_element_keys: A list of element keys which will be excluded from the process if specified.
    :return: None
    """
    # Handle parameters
    ''' print(f'New theme: {new_theme}') '''
    new_theme = new_theme if new_theme is not None else rc(lf_table)
    exempt_element_keys = exempt_element_keys if exempt_element_keys is not None else []

    if window not in list(WINDOW_THEME_MAP.keys()):
        WINDOW_THEME_MAP[window] = (theme_function(), lf_table[theme_function()])

    # Old theme stuff
    old_theme, old_theme_dict = WINDOW_THEME_MAP[window]
    # rev_old_theme_dict = _reverse_dict(old_theme_dict)
    
    # New theme stuff
    theme(new_theme)
    new_theme_dict = lf_table[new_theme]
    # rev_new_theme_dict = _reverse_dict(new_theme_dict)

    # Window level changes
    window.TKroot.config(background=theme_background_color())

    # Per-element changes happen henceforth
    for element in window.element_list():
        if element.Key not in exempt_element_keys:

            # Generic tweaks
            el = str(type(element)).lower()[0:len(str(type(element)).lower()) - 2].rsplit('.', 1)[1]
            '''print(el)'''
            if element.ParentRowFrame != None:
                element.ParentRowFrame.config(background=theme_background_color())
            if _check_if_generics_apply(el):
                element.Widget.configure(background=theme_background_color())

            # Element-specific tweaks
            styler = Style()  # Declare a styler object

            # Handling ttk scrollbars
            orientations = ['Vertical', 'Horizontal']
            for i in range(window._counter_for_ttk_widgets):
                for orientation in orientations:
                    style_name = f'{i+1}___{element.Key}.{orientation}.TScrollbar'
                    if styler.configure(style_name) != None:  # If we've stumbled upon a valid style:
                        _configure_ttk_scrollbar_style(style_name, styler)

            if el in ('text', 'statusbar'):
                text_fg = element.Widget.cget('foreground')
                text_bg = element.Widget.cget('background')
                if text_fg == old_theme_dict['TEXT']:
                    element.Widget.configure(foreground=theme_text_color()),
                    element.TextColor = theme_text_color()
                if text_bg == old_theme_dict['BACKGROUND']:
                    element.Widget.configure(background=theme_text_element_background_color())
            elif el == 'sizegrip':
                sizegrip_style = element.Widget.cget('style')
                styler.configure(sizegrip_style, background=theme_background_color())
            elif el == 'optionmenu':
                element.Widget['menu'].configure(foreground=theme_input_text_color(),
                                                 background=theme_input_background_color(),
                                                 # activeforeground=theme_input_background_color(),
                                                 # activebackground=theme_input_text_color(),
                                                 )
                element.Widget.configure(foreground=theme_input_text_color(),
                                         background=theme_input_background_color(),
                                         activeforeground=theme_input_background_color(),
                                         activebackground=theme_input_text_color())
            elif el in ('input', 'multiline'):
                element.Widget.configure(foreground=theme_input_text_color(),
                                         background=theme_input_background_color(),
                                         selectforeground=theme_input_background_color(),
                                         selectbackground=theme_input_text_color())
            elif el == 'listbox':
                element.Widget.configure(foreground=theme_input_text_color(),
                                         background=theme_input_background_color(),
                                         selectforeground=theme_input_background_color(),
                                         selectbackground=theme_input_text_color())
            elif el == 'slider':
                element.Widget.configure(foreground=theme_text_color(), troughcolor=theme_slider_color())
            elif el == 'button' and element.ButtonColor == (old_theme_dict['BUTTON'][0], old_theme_dict['BUTTON'][1]):
                element.ButtonColor = theme_button_color()
                # For regular Tk buttons
                if 'ttk' not in str(type(element.TKButton)).lower():
                    element.Widget.configure(background=theme_button_color()[1], foreground=theme_button_color()[0],
                                             activebackground=theme_button_color()[0],
                                             activeforeground=theme_button_color()[1]
                                             )
                # For Ttk Buttons
                else:
                    style_name = element.Widget.cget('style')
                    styler.configure(f'{style_name}', background=theme_button_color()[1],
                                     foreground=theme_button_color()[0])
                    styler.map(style_name,
                               foreground=[
                                   ('pressed', theme_button_color()[1]),
                                   ('active', theme_button_color()[1])
                               ],
                               background=[
                                   ('pressed', theme_button_color()[0]),
                                   ('active', theme_button_color()[0])
                               ]
                               )
            elif el == 'progressbar':
                style_name = element.TKProgressBar.style_name
                styler.configure(style_name, background=theme_progress_bar_color()[1],
                                 troughcolor=theme_progress_bar_color()[0])
            elif el == 'buttonmenu':
                element.Widget.configure(background=theme_button_color()[1], foreground=theme_button_color()[0],
                                         activebackground=theme_button_color()[0],
                                         activeforeground=theme_button_color()[1])
                element.TKMenu.configure(background=theme_input_background_color(), foreground=theme_input_text_color())
                menudef = element.MenuDefinition
                element.BackgroundColor = theme_input_background_color()
                element.TextColor = theme_input_text_color()
                element.update(menu_definition=menudef)

            elif el in 'spin':
                element.Widget.configure(background=theme_input_background_color(),
                                         foreground=theme_input_text_color(),
                                         buttonbackground=theme_input_background_color())
            elif el == 'combo':
                # Configuring the listbox of the combo.
                prefix = '$popdown.f.l configure'
                window.TKroot.tk.call('eval', f'set popdown [ttk::combobox::PopdownWindow {element.Widget}]')
                window.TKroot.tk.call('eval', f'{prefix} -background {theme_input_background_color()}')
                window.TKroot.tk.call('eval', f'{prefix} -foreground {theme_input_text_color()}')
                window.TKroot.tk.call('eval', f'{prefix} -selectforeground {theme_input_background_color()}')
                window.TKroot.tk.call('eval', f'{prefix} -selectbackground {theme_input_text_color()}')
                style_name = element.Widget.cget('style')
                # Configuring the combo itself.
                print(styler.configure(style_name))
                styler.configure(style_name,
                                 selectforeground=theme_input_background_color(),
                                 selectbackground=theme_input_text_color(),
                                 selectcolor=theme_input_text_color(),
                                 fieldbackground=theme_input_background_color(),
                                 foreground=theme_input_text_color(),
                                 background=theme_button_color()[1],
                                 arrowcolor=theme_button_color()[0],
                                 )
                styler.map(style_name,
                           foreground=[
                               ('readonly', theme_input_text_color()),
                               ('disabled', '#A3A3A3')
                           ],
                           fieldbackground=[
                               ('readonly', theme_input_background_color())
                           ]
                           )
            elif el in ('table', 'tree'):
                style_name = element.Widget.cget('style')
                styler.configure(style_name, foreground=theme_text_color(), background=theme_background_color(),
                                 fieldbackground=theme_background_color(), fieldcolor=theme_text_color())
                styler.map(style_name, foreground=[('selected', theme_button_color()[0])],
                           background=[('selected', theme_button_color()[1])])
                styler.configure(f'{style_name}.Heading', foreground=theme_input_text_color(),
                                 background=theme_input_background_color())
            elif el in ('radio', 'checkbox'):
                text_hsl = web2hsl(theme_text_color())
                background_hsl = web2hsl(theme_background_color())
                l_delta = abs(text_hsl[2] - background_hsl[2])/50
                if text_hsl[2] > background_hsl[2]:
                    adjusted = l_delta-background_hsl[2] if l_delta-background_hsl[2] >= 0 else 0
                    toggle = hsl2web((background_hsl[0], background_hsl[1], adjusted))
                else:
                    adjusted = l_delta+background_hsl[2] if l_delta+background_hsl[2] <= 1 else 1
                    toggle = hsl2web((background_hsl[0], background_hsl[1], adjusted))
                element.Widget.configure(background=theme_background_color(), foreground=theme_text_color(),
                                         selectcolor=toggle,
                                         activebackground=theme_background_color(), activeforeground=theme_text_color())
            elif el == 'tabgroup':
                style_name = element.Widget.cget('style')
                styler.configure(f'{style_name}', background=theme_background_color())
                styler.configure(f'{style_name}.Tab',
                                 background=theme_input_background_color(),
                                 foreground=theme_input_text_color())
                styler.map(f'{style_name}.Tab',
                           foreground=[
                               ('pressed', theme_button_color()[1]),
                               ('selected', theme_text_color())
                           ],
                           background=[
                               ('pressed', theme_button_color()[0]),
                               ('selected', theme_background_color())
                           ]
                           )
        else:
            pass

    WINDOW_THEME_MAP[window] = (new_theme, new_theme_dict)
    if set_future:
        theme_function(new_theme)
    window.Refresh()

def toggle_transparency(window: Window) -> None:
    """
    Reskinner currently goes around the window transparency feature that comes built in with PySimpleGUI.

    Use this function to replace that functionality on your reskinned windows. It will also work with non-reskinned
    windows.

    I say "goes around" because the current implementation for that feature in PySimpleGUI's source relies on the
    value returned by `theme_background_color()` in your namespace at the time that feature is invoked. This module
    will not modify your namespace's `theme()` value (unless you set `set_future` to True), hence it doesn't update the
    background color to that of the reskinned theme, hence the background color that gets used is that of the former
    theme. This results in the transparency toggle not doing anything visible, where it is in fact setting the former
    background color to transparent.

    :param window: The window to work on.
    :return: None
    """
    window_bg = window.TKroot.cget('background')
    transparent_color = window.TKroot.attributes('-transparentcolor')
    window.set_transparent_color(window_bg if transparent_color == '' else '')

# MAIN FUNCTION
def main():

    from PySimpleGUI import theme, theme_list, Text, Button, DropDown, TIMEOUT_KEY, LOOK_AND_FEEL_TABLE
    from random import choice as rc


    window_layout = [
        [Text('Hello! You are currently running Reskinner instead of importing it.')],
        [Text('Clicking the button will change the theme to the one specified.')],
        [Text('Or do nothing. The theme will change every few seconds')],
        [DropDown(values=theme_list(), default_value='DarkBlue3', k='new_theme')],
        [Button('Change Theme', k='change')]
    ]

    window = Window('Reskinner Demo', window_layout, element_justification='center')

    while True:

        e, v = window.Read(timeout=3000)

        if e in (None, 'Exit'):
            window.Close()
            break

        if e == 'change':
            reskin(window, v['new_theme'], theme, LOOK_AND_FEEL_TABLE)

        elif e == TIMEOUT_KEY:
            reskin(window, rc(theme_list()), theme, LOOK_AND_FEEL_TABLE)

# ENTRY POINT
if __name__ == '__main__':
    main()

