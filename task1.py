import dearpygui.dearpygui as dpg
import cv2
import math
import numpy as np
files = [
    'image.jpg',    
    'image_grayscale_one.jpg',
    'image_grayscale_second.jpg',
    'image_grayscale_difference.jpg',
    'image_red.jpg',
    'image_green.jpg',
    'image_blue.jpg',
    'image_hsv.jpg'
]

temp = cv2.imread(files[0])
cv2.imwrite(files[7],temp)

gr_1_intensity = [0 for _ in range(256)]
gr_2_intensity = [0 for _ in range(256)]



def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    maxx = max(r, g, b)
    minn = min(r, g, b)
    dif = maxx - minn

    if maxx == minn:
        h = 0
    elif maxx == r and g >= b:
        h = (60 * ((g - b) / dif) + 0)
    elif maxx == r and g < b:
        h = (60 * ((g - b) / dif) + 360)
    elif maxx == g:
        h = (60 * ((b - r) / dif) + 120)
    elif maxx == b:
        h = (60 * ((r - g) / dif) + 240)

    if maxx == 0:
        s = 0
    else:
        s = (1 - minn / maxx) * 100
    v = maxx * 100
    return round(h), round(s), round(v)

def hsv_to_rgb(h,s,v):
    hi = math.floor(h / 60) % 6
    vmin = ((100 - s) * v) / 100
    a = (v - vmin) * (h % 60) / 60
    vinc = vmin + a
    vdec = v - a

    matr = [
        (v, vinc, vmin),
        (vdec, v, vmin),
        (vmin, v, vinc),
        (vmin, vdec, v),
        (vinc, vmin, v),
        (v, vmin, vdec),
    ]

    r, g, b = matr[int(hi)]

    rgb = round(b * 2.55), round(g * 2.55), round(r * 2.55)
    return rgb


targetH, targetS, targetV = rgb_to_hsv(temp[0][0][2], temp[0][0][1], temp[0][0][0])
targetH_const = targetH
targetS_const = targetS
targetV_const = targetV


def render_task1():
    image = cv2.imread(files[0])
    w,h,_ = image.shape
    for i in range(w):
        for j in range(h):
            #0.299 0.587 0.114
            y = image[i][j][0] * 0.114 + image[i][j][1] * 0.587 + image[i][j][2] * 0.299
            image[i][j] = [y,y,y]
    cv2.imwrite(files[1], image)
    image = cv2.imread(files[0])
    for i in range(w):
        for j in range(h):
            #0.2126 0.7152 0.0722
            y = image[i][j][0] * 0.0722 + image[i][j][1] * 0.7152 + image[i][j][2] * 0.2126
            image[i][j] = [y,y,y]
    cv2.imwrite(files[2], image)
    gr_1 = cv2.imread(files[1])
    gr_2 = cv2.imread(files[2])
    image = cv2.subtract(gr_2,gr_1)
    cv2.imwrite(files[3],image)
    for i in range(w):
        for j in range(h):
            gr_1_intensity[gr_1[i][j][0]] += 1
            gr_2_intensity[gr_2[i][j][0]] += 1
def render_task2():
    image = cv2.imread(files[0])
    channels = [
        image[:, :, 0].ravel(),
        image[:, :, 1].ravel(),
        image[:, :, 2].ravel(),
    ]

    image[:, :, 1] = 0
    image[:, :, 0] = 0
    cv2.imwrite(files[4], image)

    image = cv2.imread(files[0])
    image[:, :, 2] = 0
    image[:, :, 0] = 0
    cv2.imwrite(files[5], image)

    image = cv2.imread(files[0])
    image[:, :, 2] = 0
    image[:, :, 1] = 0
    cv2.imwrite(files[6], image)
    return channels

def changeH(e,v):
    global targetH
    targetH = int(v)
def changeV(e,v):
    global targetV
    targetV = int(v)
def changeS(e,v):
    global targetS
    targetS = int(v)


def render_task3():
    image = cv2.imread('image.jpg')
    W,H,_ = image.shape
    hsv_arr = []
    for i in range(W):
        for j in range(H):
            h, s, v = rgb_to_hsv(image[i][j][2], image[i][j][1], image[i][j][0])
            r,g,b = hsv_to_rgb(np.mod(h + targetH, 360),targetS,targetV)
            image[i][j][0] = r
            image[i][j][1] = g
            image[i][j][2] = b

    cv2.imwrite(files[7],image)
    width_hsv, height_hsv, channels_hsv, data_hsv = dpg.load_image(files[7])
    dpg.set_value("hsv", data_hsv)
    
render_task1()
channels_task2 = render_task2()

dpg.create_context()
with dpg.window(label="Task 1"):
    width, height, channels, data = dpg.load_image(files[0])
    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag="default")

    width_gr_1, height_gr_1, channels_gr_1, data_gr_1 = dpg.load_image(files[1])
    with dpg.texture_registry():
        dpg.add_static_texture(width_gr_1, height_gr_1, data_gr_1, tag="default_gr_1")
        
    width_gr_2, height_gr_2, channels_gr_2, data_gr_2 = dpg.load_image(files[2])
    with dpg.texture_registry():
        dpg.add_static_texture(width_gr_2, height_gr_2, data_gr_2, tag="default_gr_2")
        
    width_gr_3, height_gr_3, channels_gr_3, data_gr_3 = dpg.load_image(files[3])
    with dpg.texture_registry():
        dpg.add_static_texture(width_gr_3, height_gr_3, data_gr_3, tag="default_gr_3")

    dpg.add_simple_plot(label="First grayscale intensity", default_value=gr_1_intensity, height=180, width=256, histogram=True)
    dpg.add_simple_plot(label="Second grayscale intensity", default_value=gr_2_intensity, height=180, width=256, histogram=True) 
    with dpg.drawlist(width=600, height=400):
        dpg.draw_image("default", (0,0), (600, 400))
    with dpg.drawlist(width=600, height=400):
        dpg.draw_image("default_gr_1", (0,0), (600, 400))
    with dpg.drawlist(width=600, height=400):    
        dpg.draw_image("default_gr_2", (0,0), (600, 400))
    with dpg.drawlist(width=600, height=400):
        dpg.draw_image("default_gr_3", (0,0), (600, 400))
with dpg.window(label="Task 2"):
    width_red, height_red, channels_red, data_red = dpg.load_image(files[4])
    with dpg.texture_registry():
        dpg.add_static_texture(width_red, height_red, data_red, tag="red_channel")

    width_green, height_green, channels_green, data_green = dpg.load_image(files[5])
    with dpg.texture_registry():
        dpg.add_static_texture(width_green, height_green, data_green, tag="green_channel")
        
    width_blue, height_blue, channels_blue, data_blue= dpg.load_image(files[6])
    with dpg.texture_registry():
        dpg.add_static_texture(width_blue, height_blue, data_blue, tag="blue_channel")

    dpg.add_simple_plot(label="Red channel", default_value=channels_task2[0], histogram=True, height=180, width=256)
    dpg.add_simple_plot(label="Green chanel", default_value=channels_task2[1], histogram=True, height=180, width=256) 
    dpg.add_simple_plot(label="Blue chanel", default_value=channels_task2[2], histogram=True, height=180, width=256) 
    with dpg.drawlist(width=600, height=400):
        dpg.draw_image("red_channel", (0,0), (600, 400))
    with dpg.drawlist(width=600, height=400):    
        dpg.draw_image("green_channel", (0,0), (600, 400))
    with dpg.drawlist(width=600, height=400):
        dpg.draw_image("blue_channel", (0,0), (600, 400))
with dpg.window(label="Task 3"):
    width_hsv, height_hsv, channels_hsv, data_hsv = dpg.load_image(files[7])
    with dpg.texture_registry():
        dpg.add_dynamic_texture(width_hsv, height_hsv, data_hsv, tag="hsv")
    with dpg.drawlist(width=600, height=400):
        dpg.draw_image("default", (0,0), (600, 400))
    with dpg.drawlist(width=600, height=400):
        dpg.draw_image("hsv", (0,0), (600, 400), id=100)
    dpg.add_button(label="Render!",callback=render_task3)
    dpg.add_slider_float(label="H", default_value=targetH, max_value=360,callback=changeH)
    dpg.add_slider_float(label="S", default_value=targetS, max_value=100,callback=changeS)
    dpg.add_slider_float(label="V", default_value=targetV, max_value=100,callback=changeV)
dpg.create_viewport(title='Lab 02', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport() 
dpg.start_dearpygui()
dpg.destroy_context()

