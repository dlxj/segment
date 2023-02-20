
# 鼠标移动最左上角退出本程序

from time import sleep
import pyautogui, sys
import keyboard
import time

'''默认这项功能为True, 这项功能意味着：当鼠标的指针在屏幕的最坐上方，程序会报错；目的是为了防止程序无法停止'''
#pyautogui.FAILSAFE =False
'''意味着所有pyautogui的指令都要暂停一秒；其他指令不会停顿；这样做，可以防止键盘鼠标操作太快；'''
pyautogui.PAUSE = 1

# 得到当前鼠标位置
print(pyautogui.position()) #Point(x=502, y=365)

print(pyautogui.isValidKey('del'))

# pyautogui.click(745,421,button='left')  # netflix pin码输入框最左边单击左键
# pyautogui.press('del')  # 按下 Del
# time.sleep(0.1)
# pyautogui.press('del')
# time.sleep(0.1)
# pyautogui.press('del')


#time.sleep(3)

while True:
    # 鼠标移动最左上角退出
    pyautogui.click(613,421,button='left')  # netflix pin码输入框最左边单击左键
    pyautogui.press('6')  # 按下 6
    time.sleep(0.01)
    pyautogui.press('1')
    time.sleep(0.01)
    pyautogui.press('7')
    time.sleep(0.01)
    pyautogui.press('4')
    time.sleep(10)

# try:
#     curr = 0
#     while True:
#         x, y = pyautogui.position()
#         positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
#         print(positionStr, end='')
#         print('\b' * len(positionStr), end='', flush=True)

#         pyautogui.moveTo(184, 941, 3)
#         pyautogui.moveTo(1685, 121, 3)
#         if keyboard.is_pressed('b'):
#             break
        
#         time.sleep(10)


#         curr += 1
#         if curr >= 3:
#             break
# except KeyboardInterrupt:
#     print('KeyboardInterrupt')


