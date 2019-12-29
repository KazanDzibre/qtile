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
browser = "firefox"


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
        Key([mod],"w", lazy.spawn(browser)),
        # Toggle between different layouts as defined below
        Key([mod], "Tab", lazy.next_layout()),
        Key([mod, "shift"], "c", lazy.window.kill()),

        Key([mod, "control"], "r", lazy.restart()),
        Key([mod, "control"], "q", lazy.shutdown()),
        Key([mod], "r", lazy.spawncmd()),
        ]
    return keys


##### BAR COLORS #####

def init_colors():
    return [["#eb4034", "#282a36"], # panel background
            ["#434758", "#434758"], # background for current screen tab
            ["#ffffff", "#ffffff"], # font color for group names
            ["#ff5555", "#ff5555"], # background color for layout widget
            ["#000000", "#000000"], # background for other screen tabs
            ["#A77AC4", "#A77AC4"], # dark green gradiant for other screen tabs
            ["#50fa7b", "#50fa7b"], # background color for network widget
            ["#7197E7", "#7197E7"], # background color for pacman widget
            ["#9AEDFE", "#9AEDFE"], # background color for cmus widget
            ["#000000", "#000000"], # background color for clock widget
            ["#434758", "#434758"]] # background color for systray widget


@hook.subscribe.startup_once
def start_once():
    os.system("nitrogen --restore &")


def init_layouts():
    return [layout.MonadTall(),
            layout.Max(),
            layout.Stack(num_stacks=2),
            layout.Floating()
            ]




widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()


def init_group_names():
    return [("WWW", {'layout': 'monadtall'}),
            ("DEV", {'layout': 'monadtall'}),
            ("SYS", {'layout': 'monadtall'}),
            ("DOC", {'layout': 'monadtall'}),
            ("VBOX", {'layout': 'monadtall'}),
            ("CHAT", {'layout': 'monadtall'}),
            ("MUS", {'layout': 'monadtall'}),
            ("VID", {'layout': 'monadtall'}),
            ("GFX", {'layout': 'floating'})]

def init_groups():
    return [Group(name, **kwargs) for name, kwargs in group_names]




screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.TextBox("default config", name="default"),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            24,
        ),
    ),
]

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
    layouts = init_layouts()
    group_names = init_group_names()
    groups = init_groups()
    
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
