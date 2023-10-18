# import the pyautogui library to test and use it to do initial cursor movement
import pyautogui

# find the size of the screen
print(pyautogui.size())

# move the cursor to a specified location over a period of time
pyautogui.moveTo(100, 100, duration=1)

# move the cursor relative to its current position over a period of time
pyautogui.moveRel(0, 50, duration=1)

# print out the current position of the cursor
print(pyautogui.position())

# click at a specified location
pyautogui.click(100, 100)