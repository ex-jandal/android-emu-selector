# Android Emulator Selector

A lightweight Python script to quickly select and launch Android Virtual Devices (AVDs) from your terminal with a beautiful interactive UI.

## Features

- **Interactive TUI**: Uses `rich` and `readchar` to provide a smooth, keyboard-driven selection interface.
- **AVD Discovery**: Automatically detects available AVDs from your `ANDROID_AVD_HOME`.
- **Internet Toggle**: Quickly choose whether to start the emulator with or without internet access (useful for testing offline scenarios).
- **Vim-like Navigation**: Supports both arrow keys and `h`, `j`, `k`, `l` (Vim keys) for navigation.

## Prerequisites

Before using this script, ensure you have the following environment variables set:

- `ANDROID_HOME`: Path to your Android SDK root (e.g., `~/Android/Sdk`).
- `ANDROID_AVD_HOME`: Path to where your `.avd` directories are stored (usually `~/.android/avd`).

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/android-emu-selector.git
   cd android-emu-selector
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   or install it system-wide e.g.:
   ```bash
   yay -S python-rich python-readchar
   ```

## Usage

Run the script using Python:

```bash
python3 script.py
```

### Controls
- **Up/Down** or **j/k**: Navigate through the list of available AVDs.
- **Enter**: Select the highlighted AVD or confirm an option.
- **Left/Right** or **h/l**: Toggle between "Yes" and "No" for internet access.
- **Esc** or **q**: Quit the script.

### Desktop Entry

A `.desktop` file is included to help make the script more portable and accessible from your application launcher. To use it:

1. **Copy the file**:
   ```bash
   cp android-emulator.desktop ~/.local/share/applications/
   ```

2. **Customize the configuration**:
   Edit the `Exec` line in `~/.local/share/applications/android-emulator.desktop` to match your environment:
   - **Path**: Update `/absolute/path/to/script.py` to the actual path of your script.
   - **Terminal**: The default uses `foot`. You can change this to your preferred terminal (e.g., `gnome-terminal --`, `alacritty -e`, `konsole -e`).
   - **Shell**: The command is wrapped in `bash -c`. You can modify this if you use a different shell or need specific environment variables.

   Example for a standard setup:
   ```ini
   Exec=gnome-terminal -- python3 /path/to/script.py
   ```
   Or:
   ```ini
   Exec=foot -e python3 /path/to/script.py
   ```

   ⚠️ Make like this if your working with Wayland-Compositor e.g.(Niri, Hyprland, ...):
   ```ini
   Exec=bash -c "QT_QPA_PLATFORM=xcb gnome-terminal -- python3 /path/to/script.py"
   ```
   The command is wrapped in `bash -c`. You can modify this if you use a different shell or need specific environment variables.

## How it Works

The script scans your `ANDROID_AVD_HOME` for directories ending in `.avd`. Once you select a device and decide on internet access, it launches the emulator in a detached process:
- `emulator -avd <device_name>` (with internet)
- `emulator -avd <device_name> -dns-server 127.0.0.1` (without internet)

## License

This project is licensed under the terms of the [LICENSE] file included in the repository.
