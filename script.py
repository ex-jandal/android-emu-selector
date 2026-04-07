#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filename: emu.py
Author: Abu_jandal
Date: 2026-04-07
Description: Script to open Android Emulator with any AVD you have.
"""

from rich import box
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.style import Style
from rich.panel import Panel
from rich.align import Align
from readchar import readkey, key

import os;
import sys;
import pathlib
import subprocess

stats = 0;

AVD_HOME = os.getenv("ANDROID_AVD_HOME");
ANDROID_HOME = os.getenv("ANDROID_HOME");
executable = f"{ANDROID_HOME}/emulator/emulator"

def env_var_not_found(var_name: str):
    sys.stderr.write(
f"""\
{var_name} is not set in your enviroment variable, 
so you have to set it to where the avd exists.

"""
    );

if AVD_HOME == None:
    env_var_not_found("ANDROID_AVD_HOME");
    stats += 1;

if ANDROID_HOME == None:
    env_var_not_found("ANDROID_HOME");
    stats += 1;

if stats > 0:
    input("Press Enter...")
    exit(1)

if not pathlib.Path(executable).is_file():
    sys.stderr.write(f"{executable} is not found in your System.\n");
    exit(1)

dirs = [ 
    item.name.split('.')[0]
    for item in pathlib.Path(AVD_HOME).iterdir() 
    if item.is_dir() and item.name.endswith(".avd")
];

term_size = os.get_terminal_size()

selected = 0
console = Console()

SELECTED_STYLE = Style(color="blue", bgcolor="white", bold=True)

def generate_devices_table(selected_index) -> Table:
    """Generates a table with highlighting for the selected item."""
    table = Table(
        box=box.ROUNDED, 
        width=term_size.columns,
        header_style="bold magenta", 
        title="Select an Option"
    )
    table.add_column("Index", width=5)
    table.add_column("Selection")
    
    for i, option in enumerate(dirs):
        row_style = SELECTED_STYLE if i == selected_index else None
        table.add_row(str(i), option, style=row_style)
    
    return table

with Live(generate_devices_table(selected), screen=True, refresh_per_second=30) as live:
    while True:
        k = readkey()
        if k == key.UP or k == 'k':
            selected = max(0, selected - 1)
        elif k == key.DOWN or k == 'j':
            selected = min(len(dirs) - 1, selected + 1)
        elif k == key.ENTER:
            break
        elif k == key.ESC or k == 'q':
            exit(0)
        
        live.update(generate_devices_table(selected))

options = ["Yes", "No"]
index = 0  # 0 for Yes, 1 for No

def get_dialog(selected_index):
    buttons = [
        f"[bold white on blue]  {opt}  [/]" if i == selected_index else f"  {opt}  "
        for i, opt in enumerate(options)
    ]
    menu = "    ".join(buttons)
    
    return Panel(
        Align.center(f"\nDo you want to have Internet Access in AVD?\n\n{menu}\n"),
        title="[bold red]Confirmation[/]",
        width=term_size.columns
    )

with Live(get_dialog(index), screen=True, refresh_per_second=30) as live:
    while True:
        k = readkey()
        if k == key.LEFT or k == 'h': index = 0
        elif k == key.RIGHT or k == 'l': index = 1
        elif k == key.ENTER : break
        elif k == 'q': sys.exit()
        
        live.update(get_dialog(index))

device_name = dirs[selected];
has_internet_access = True if index == 0 else False;

console.print(f"You selected device: [bold green]{device_name}[/bold green]")
console.print(f"Internet Access? [bold]{has_internet_access}[/]")

executable += f" -avd {device_name}"
if not has_internet_access:
    executable += " -dns-server 127.0.0.1"
env_vars = os.environ.copy()

executable = executable;

subprocess.Popen(
    executable, 
    shell=True, 
    env=env_vars, 
    start_new_session=True,
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL, 
    stderr=subprocess.DEVNULL
)
