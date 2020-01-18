# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#  __  __            _           ____            _
# |  \/  | __ _ _ __| | _____   |  _ \ _   _ ___(_) ___
# | |\/| |/ _` | '__| |/ / _ \  | |_) | | | |_  / |/ __|
# | |  | | (_| | |  |   < (_) | |  _ <| |_| |/ /| | (__
# |_|  |_|\__,_|_|  |_|\_\___/  |_| \_\\__,_/___|_|\___|


import os
import re
import socket
import subprocess
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.widget import Spacer


from typing import List  # noqa: F401

mod = "mod4"
myTerm = "termite"
browser = "brave"


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

##### LAUNCH APPS IN SPECIFIED GROUPS #####

def app_or_group(group, app):
    def f(qtile):
        if qtile.groupMap[group].windows:
            qtile.groupMap[group].cmd_toscreen()
        else:
            qtile.groupMap[group].cmd_toscreen()
            qtile.cmd_spawn(app)
    return f


##### KEYBINDINGS

def init_keys():
    keys = [
        # Switch between windows in current stack pane
        Key([mod], "k", lazy.layout.down()),
        Key([mod], "j", lazy.layout.up()),

        # Move windows up or down in current stack
        Key([mod, "control"], "k", lazy.layout.shuffle_down()),
        Key([mod, "control"], "j", lazy.layout.shuffle_up()),

        # Switch window focus to other pane(s) of stack
        Key([mod], "space", lazy.layout.next()),

        # Swap panes of split stack
        Key([mod, "shift"], "space", lazy.layout.rotate()),

        # Toggle between split and unsplit sides of stack.
        # Split = all windows displayed
        # Unsplit = 1 window displayed, like Max layout, but still with
        # multiple stack panes
        Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
        Key([mod], "Return", lazy.spawn(myTerm)),
        Key([mod], "s", lazy.spawn("stacer")),
        Key([mod],"w", lazy.spawn(browser)),
        Key([mod],"x", lazy.spawn("scrot /home/rule/screenshots/%Y-%m-%d-%T-screenshot.png")),
        Key([mod],"q", lazy.spawn("qutebrowser")),
        Key([mod],"g", lazy.spawn("gimp")),
        Key([mod],"t", lazy.spawn("qbittorrent")),
        # Toggle between different layouts as defined below
        Key([mod], "Tab", lazy.next_layout()),
        Key([mod, "shift"], "c", lazy.window.kill()),

		#DODACI
		Key([mod, "shift"], "l", lazy.layout.grow(),lazy.layout.increase_nmaster()),
		Key([mod, "shift"], "h", lazy.layout.shrink(),lazy.layout.decrease_nmaster()),
		Key([mod, "shift"], "o", window_to_prev_group),
		Key([mod, "shift"], "p", window_to_next_group),
		Key([mod, "shift"], "space",lazy.layout.rotate(),lazy.layout.flip()),

                Key([mod, "shift"], "Left",window_to_prev_group),
                Key([mod, "shift"], "Right",window_to_next_group),


        Key([mod, "control"], "r", lazy.restart()),
        Key([mod, "control"], "q", lazy.shutdown()),
        Key([mod], "r", lazy.spawncmd()),
        ]
    return keys


##### BAR COLORS #####

def init_colors():
    return [["#282a36", "#282a36"], # panel background
            ["#434758", "#434758"], # background for current screen tab
            ["#ffffff", "#ffffff"], # font color for group names
            ["#4038e0", "#3883e0"], # background color for layout widget
            ["#000000", "#000000"], # background for other screen tabs
            ["#A77AC4", "#A77AC4"], # dark green gradiant for other screen tabs
            ["#4038e0", "#4038e0"], # background color for network widget
            ["#4038e0", "#4038e0"], # background color for pacman widget
            ["#9AEDFE", "#9AEDFE"], # background color for cmus widget
            ["#000000", "#000000"], # background color for clock widget
            ["#434758", "#434758"]] # background color for systray widget



@hook.subscribe.startup_once
def start_once():
    os.system("nitrogen --restore &")


##### LAYOUTS #####

def init_floating_layout():
    return layout.Floating(border_focus="#3B4022")


def init_layout_theme():
    return {"border_width": 3,
            "margin": 5,
            "border_focus": "3db1e3",
            "border_normal": "1e24d4"
           }

def init_border_args():
    return {"border_width": 2}


def init_layouts():
    return [layout.MonadTall(**layout_theme),
            layout.Max(**layout_theme),
            layout.Stack(num_stacks=2, **layout_theme),
            layout.Floating(**layout_theme)
            ]




widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()


def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
               widget.Sep(
                        linewidth = 0,
                        padding = 6,
                        foreground = colors[2],
                        background = colors[0]
                        ),
               widget.GroupBox(font="Ubuntu Bold",
                        fontsize = 9,
                        margin_y = 0,
                        margin_x = 0,
                        padding_y = 5,
                        padding_x = 5,
                        borderwidth = 1,
                        active = colors[2],
                        inactive = colors[2],
                        rounded = False,
                        highlight_method = "block",
                        this_current_screen_border = colors[5],
                        this_screen_border = colors [1],
                        other_current_screen_border = colors[0],
                        other_screen_border = colors[0],
                        foreground = colors[2],
                        background = colors[0]
                        ),
               widget.Prompt(
                        prompt=prompt,
                        font="Ubuntu Mono",
                        padding=10,
                        foreground = colors[3],
                        background = colors[1]
                        ),
               widget.Sep(
                        linewidth = 0,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[0]
                        ),
               widget.WindowName(font="Ubuntu",
                        fontsize = 11,
                        foreground = colors[5],
                        background = colors[0],
                        padding = 5
                        ),
               widget.Systray(
                        background=colors[10],
                        padding = 5
                        ),
               widget.Image(
                        filename="/home/rule/slike/slika1.png"
                        ),
               widget.Net(
                        interface = "wlp18s0b1",
                        foreground = colors[2],
                        background = colors[5],
                        padding = 5
                        ),
               widget.Image(
                        filename="/home/rule/slike/slika3.png"
                        ),
               widget.CurrentLayout(
                        foreground = colors[2],
                        background = colors[7],
                        padding = 5
                        ),
               widget.Image(
                        filename="/home/rule/slike/slika2.png"
                        ),
               widget.Pacman(
                        execute = "urxvtc",
                        update_interval = 1800,
                        foreground = colors[2],
                        background = colors[5]
                        ),
               widget.Image(
                        filename="/home/rule/slike/slika3.png"
                        ),
               widget.TextBox(
                        font="Ubuntu Bold",
                        text=" ♫",
                        padding = 5,
                        foreground=colors[2],
                        background=colors[7],
                        fontsize=14
                        ),
               widget.Cmus(
                        max_chars = 40,
                        update_interval = 0.5,
                        foreground=colors[2],
                        background = colors[7]
                        ),
               widget.Image(
                        filename="/home/rule/slike/slika2.png"
                        ),
               widget.CapsNumLockIndicator(
                        background = colors[5],
                        foreground = colors[2],
                        font = "Ubuntu Bold",
                        update_interval = 0.1
                       ),
               widget.Clock(
                        foreground = colors[2],
                        background = colors[5],
                        format="%A, %B %d - %H:%M"
                        )
              ]
    return widgets_list



def init_group_names():
    return [("WWW", {'layout': 'monadtall'}),
            ("DEV", {'layout': 'monadtall'}),
            ("MUS", {'layout': 'monadtall'}),
            ("DOC", {'layout': 'monadtall'}),
            ("VBOX", {'layout': 'monadtall'}),
            ("CHAT", {'layout': 'monadtall'}),
            ("SYS", {'layout': 'monadtall'}),
            ("VID", {'layout': 'monadtall'}),
            ("GFX", {'layout': 'floating'})]

def init_groups():
    return [Group(name, **kwargs) for name, kwargs in group_names]



def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1                       # Slicing removes unwanted widgets on Monitors 1,3


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.95, size=20))]



def init_mouse():
    return [Drag([mod], "Button1", lazy.window.set_position_floating(),      # Move floating windows
                 start=lazy.window.get_position()),
            Drag([mod], "Button3", lazy.window.set_size_floating(),          # Resize floating windows
                 start=lazy.window.get_size()),
            Click([mod, "shift"], "Button1", lazy.window.bring_to_front())]  # Bring floating window to front


dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"


if __name__ in ["config", "__main__"]:
    mod = "mod4"

    colors = init_colors()
    keys = init_keys()
    mouse = init_mouse()
    group_names = init_group_names()
    groups = init_groups()
    floating_layout = init_floating_layout()
    layout_theme = init_layout_theme()
    border_args = init_border_args()
    layouts = init_layouts()
    screens = init_screens()
    #widget_defaults = init_widgets_defaults()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()



##### SETS GROUPS KEYBINDINGS #####

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))          # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))   # Send current window to another group



# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
