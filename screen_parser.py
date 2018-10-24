import pyautogui
import pytesseract
import time
import os

def get_sq_size():
    input('Move your mouse to the top left square and press Enter.')
    currentMouseX, currentMouseY = pyautogui.position()
    print('Thank you. You can use your mouse now.')
    img = pyautogui.screenshot()
    color = img.getpixel((currentMouseX, currentMouseY))
    left = currentMouseX
    right = currentMouseX
    top = currentMouseY
    bot = currentMouseY
    while img.getpixel((left, top)) == color:
        left -= 1
    left += 1
    while img.getpixel((right, top)) == color:
        right += 1
    right -= 1
    while img.getpixel((left, top)) == color:
        top -= 1
    top += 1
    # while img.getpixel((left, bot)) == color:
    #     bot += 1
    # bot -= 1
    n = len(list(pyautogui.locateAll('imgs/cross.jpg', img)))
    n //= 16
    n **= 0.5
    n = round(n)
    n *= 5
    return right - left + 1, (left, top), n

def is_empty(crop):
    w, h = crop.size
    color = crop.getpixel((0, h // 2))
    for r in range(w):
        if crop.getpixel((r, h // 2)) != color:
            return False
    return True

def get_rows(n, size, top_left):
    config_opt = '--psm 10 -c tessedit_char_whitelist=0123456789'
    img = pyautogui.screenshot()
    right = top_left[0] - size // 2
    left = right
    top = top_left[1]
    color = img.getpixel((left, top))
    while img.getpixel((left, top)) == color:
        left -= 1
    left += 3
    # row___lrtb = []
    row___string = []
    row___ltrb = []
    row___pattern = []
    # prev_bot = top
    for line in range(n):
        t = top + line * (size + 2)
        b = t + size
        l = right - size - 2
        r = right
        row___pattern.append([])
        i = 0
        while True:
            l = max(left, l)
            crop = img.crop((l, t, r, b))
            if is_empty(crop):
                break
            num = pytesseract.image_to_string(crop, config=config_opt)
            if num == '' or any(x not in '1234567890' for x in num):
                crop.save(os.path.join('crops', 'r_{}_{}.png'.format(line, i)))
            row___pattern[line].append(int(num))
            l -= size + 2
            r -= size + 2
            i += 1
        row___pattern[line] = row___pattern[line][::-1]

    return row___pattern

def get_cols(n, size, top_left):
    img = pyautogui.screenshot()
    left = top_left[0]
    bot = top_left[1] - size // 2
    top = bot
    color = img.getpixel((left, bot))
    while img.getpixel((left, top)) == color:
        top -= 1
        if top < 0:
            break
    top += 3
    col___ltrb = []
    col___string = []
    col___pattern = []
    config_opt = '--psm 10 -c tessedit_char_whitelist=0123456789'
    for line in range(n):
        l = left + line * (size + 2)
        r = l + size
        b = bot
        t = bot - size - 2
        col___pattern.append([])
        while True:
            t = max(top, t)
            crop = img.crop((l, t, r, b))
            if is_empty(crop):
                break
            num = pytesseract.image_to_string(crop, config=config_opt)
            if num == '' or any(x not in '1234567890' for x in num):
                crop.save(os.path.join('crops', 'c_{}.png'.format(line)))
            col___pattern[line].append(int(num))
            b -= size + 2
            t -= size + 2
        col___pattern[line] = col___pattern[line][::-1]
    # col___ltrb.append((l, t, r, b))
    return col___pattern

def fill(n, top_left, size, ans):
    left = top_left[0] + size // 2
    top = top_left[1] + size // 2
    for r, line in enumerate(ans):
        t = top + r * (size + 2)
        for c, val in enumerate(line):
            l = left + c * (size + 2)
            pyautogui.moveTo(l, t)
            if val == 0:
                pyautogui.click(button='right')
            elif val == 1:
                pyautogui.click()

def get_rows__cols():
    size, top_left, n = get_sq_size()
    rows = get_rows(n, size, top_left)
    print('ROWS')
    print(*rows, sep = '\n')
    cols = get_cols(n, size, top_left)
    print('COLS')
    print(*cols, sep = '\n')
    print("#####")
    return n, cols, rows, top_left, size

if __name__ == '__main__':
    # top_left = pyautogui.locateOnScreen('imgs/top_left.jpg')
    # print(top_left)
    # all_ones = list(pyautogui.locateAllOnScreen('imgs/1.jpg'))
    # print(all_ones)
    size, top_left, n = get_sq_size()

    # input('Now press Enter and open Pattern fullscreen')
    # time.sleep(3)
    # img = pyautogui.screenshot()
    # print(pytesseract.image_to_string(img))
    rows = get_rows(n, size, top_left)
    print(*rows, sep='\n')
    print('$$$$$$$$$$')
    cols = get_cols(n, size, top_left)
    print(*cols, sep='\n')
    print('############')
    print(size)
    print(top_left)
    print(n)

    # os.system('play --no-show-progress --null --channels 1 synth %s sine %f' %( 0.1, 400)) #make beep
