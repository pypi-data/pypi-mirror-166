import sys

from je_auto_control.utils.exception.exception_tag import windows_import_error
from je_auto_control.utils.exception.exceptions import AutoControlException

if sys.platform not in ["win32", "cygwin", "msys"]:
    raise AutoControlException(windows_import_error)

"""
windows mouse virtual keycode
"""

win32_MOVE = 0x0001
win32_LEFTDOWN = 0x0002
win32_LEFTUP = 0x0004
win32_RIGHTDOWN = 0x0008
win32_RIGHTUP = 0x0010
win32_MIDDLEDOWN = 0x0020
win32_MIDDLEUP = 0x0040
win32_DOWN = 0x0080
win32_XUP = 0x0100
win32_WHEEL = 0x0800
win32_HWHEEL = 0x1000
win32_ABSOLUTE = 0x8000
win32_XBUTTON1 = 0x0001
win32_XBUTTON2 = 0x0002

win32_VK_LBUTTON = 0x01
win32_VK_RBUTTON = 0x02
win32_VK_MBUTTON = 0x04
win32_VK_XBUTTON1 = 0x05
win32_VK_XBUTTON2 = 0x06

"""
windows keyboard virtual keycode
"""

win32_EventF_EXTENDEDKEY = 0x0001
win32_EventF_KEYUP = 0x0002
win32_EventF_UNICODE = 0x0004
win32_EventF_SCANCODE = 0x0008

win32_VkToVSC = 0
win32_VK_CANCEL = 0x03
win32_VK_BACK = 0x08  # BACKSPACE key
win32_VK_TAB = 0x09  # TAB key
win32_VK_CLEAR = 0x0C  # CLEAR key
win32_VK_RETURN = 0x0D  # ENTER key
win32_VK_SHIFT = 0x10  # SHIFT key
win32_VK_CONTROL = 0x11  # CTRL key
win32_VK_Menu = 0x12  # ALT key
win32_VK_PAUSE = 0x13  # PAUSE key
win32_VK_CAPITAL = 0x14  # CAPS LOCK key
win32_VK_KANA = 0x15
win32_VK_IME_ON = 0x16
win32_VK_JUNJA = 0x17
win32_VK_FINAL = 0x18  # ESC key
win32_VK_HANJA = 0x19
win32_VK_IME_OFF = 0x1A
win32_VK_ESCAPE = 0x1B
win32_VK_CONVERT = 0x1C
win32_VK_NONCONVERT = 0x1D
win32_VK_ACCEPT = 0x1E
win32_VK_MODECHANGE = 0x1F
win32_VK_SPACE = 0x20  # SPACEBAR
win32_VK_PRIOR = 0x21  # PAGE UP key
win32_VK_NEXT = 0x22  # PAGE DOWN key
win32_VK_END = 0x23  # END key
win32_VK_HOME = 0x24  # HOME key
win32_VK_LEFT = 0x25  # LEFT ARROW key
win32_VK_UP = 0x26
win32_VK_RIGHT = 0x27
win32_VK_DOWN = 0x28
win32_VK_SELECT = 0x29
win32_VK_PRINT = 0x2A
win32_VK_EXECUTE = 0x2B
win32_VK_SNAPSHOT = 0x2C
win32_VK_INSERT = 0x2D
win32_VK_DELETE = 0x2E
win32_VK_HELP = 0x2F
win32_key0 = 0x30
win32_key1 = 0x31
win32_key2 = 0x32
win32_key3 = 0x33
win32_key4 = 0x34
win32_key5 = 0x35
win32_key6 = 0x36
win32_key7 = 0x37
win32_key8 = 0x38
win32_key9 = 0x39
win32_keyA = 0x41
win32_keyB = 0x42
win32_keyC = 0x43
win32_keyD = 0x44
win32_keyE = 0x45
win32_keyF = 0x46
win32_keyG = 0x47
win32_keyH = 0x48
win32_keyI = 0x49
win32_keyJ = 0x4A
win32_keyK = 0x4B
win32_keyL = 0x4C
win32_keyM = 0X4D
win32_keyN = 0x4E
win32_keyO = 0x4F
win32_keyP = 0x50
win32_keyQ = 0x51
win32_keyR = 0x52
win32_keyS = 0x53
win32_keyT = 0x54
win32_keyU = 0x55
win32_keyV = 0x56
win32_keyW = 0x57
win32_keyX = 0x58
win32_keyY = 0x59
win32_keyZ = 0x5A
win32_VK_LWIN = 0x5B  # Left Windows key (Natural keyboard)
win32_VK_RWIN = 0x5C  # Right Windows key (Natural keyboard)
win32_VK_APPS = 0x5D  # Applications key (Natural keyboard)
win32_VK_SLEEP = 0x5F  # Computer Sleep key
win32_VK_NUMPAD0 = 0x60  # Numeric keypad 0 key
win32_VK_NUMPAD1 = 0x61
win32_VK_NUMPAD2 = 0x62
win32_VK_NUMPAD3 = 0x63
win32_VK_NUMPAD4 = 0x64
win32_VK_NUMPAD5 = 0x65
win32_VK_NUMPAD6 = 0x66
win32_VK_NUMPAD7 = 0x67
win32_VK_NUMPAD8 = 0x68
win32_VK_NUMPAD9 = 0x69
win32_VK_MULTIPLY = 0x6A  # Multiply key
win32_VK_ADD = 0x6B  # Add key
win32_VK_SEPARATOR = 0x6C  # Separator key
win32_VK_SUBTRACT = 0x6D  # Subtract key
win32_VK_DECIMAL = 0x6E  # Decimal key
win32_VK_DIVIDE = 0x6F  # VK_DIVIDE
win32_VK_F1 = 0x70  # F1
win32_VK_F2 = 0x71
win32_VK_F3 = 0x72
win32_VK_F4 = 0x73
win32_VK_F5 = 0x74
win32_VK_F6 = 0x75
win32_VK_F7 = 0x76
win32_VK_F8 = 0x77
win32_VK_F9 = 0x78
win32_VK_F10 = 0x79
win32_VK_F11 = 0x7A
win32_VK_F12 = 0x7B
win32_VK_F13 = 0x7C
win32_VK_F14 = 0x7D
win32_VK_F15 = 0x7E
win32_VK_F16 = 0x7F
win32_VK_F17 = 0x80
win32_VK_F18 = 0x81
win32_VK_F19 = 0x82
win32_VK_F20 = 0x83
win32_VK_F21 = 0x84
win32_VK_F22 = 0x85
win32_VK_F23 = 0x86
win32_VK_F24 = 0x87
win32_VK_NUMLOCK = 0x90  # NUM LOCK key
win32_VK_SCROLL = 0x91  # SCROLL LOCK key
win32_VK_LSHIFT = 0xA0  # Left SHIFT key
win32_VK_RSHIFT = 0xA1
win32_VK_LCONTROL = 0xA2  # Left CONTROL key
win32_VK_RCONTROL = 0xA3  # Right CONTROL key
win32_VK_LMENU = 0xA4  # Left MENU key
win32_VK_RMENU = 0xA5  # Right MENU key
win32_VK_BROWSER_BACK = 0xA6  # Browser Back key
win32_VK_BROWSER_FORWARD = 0xA7  # Browser Forward key
win32_VK_BROWSER_REFRESH = 0xA8  # Browser Refresh key
win32_VK_BROWSER_STOP = 0xA9  # Browser Stop key
win32_VK_BROWSER_SEARCH = 0xAA  # Browser Search key
win32_VK_BROWSER_FAVORITES = 0xAB  # Browser Favorites key
win32_VK_VOLUME_MUTE = 0xAD
win32_VK_VOLUME_DOWN = 0xAE
win32_VK_VOLUME_UP = 0xAF
win32_VK_MEDIA_NEXT_TRACK = 0xB0
win32_VK_MEDIA_PREV_TRACK = 0xB1
win32_VK_MEDIA_STOP = 0xB2
win32_VK_MEDIA_PLAY_PAUSE = 0xB3
win32_VK_LAUNCH_MAIL = 0xB4
win32_VK_LAUNCH_MEDIA_SELECT = 0xB5
win32_VK_LAUNCH_APP1 = 0xB6
win32_VK_LAUNCH_APP2 = 0xB7
