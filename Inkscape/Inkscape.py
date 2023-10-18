# -*- coding: utf-8 -*-
# """
# Created on Sun Mar 12 16:15:12 2023

# @author: carol

# to convert svg to ico 
# https://cloudconvert.com/

# # https://github.com/spakin/SimpInkScr/wiki/Shape-construction#circles-and-ellipses

# import sys
# sys.path.insert(0, r'C:\Users\carol\AppData\Roaming\inkscape\extensions\SimpInkScr') 


# """
# import sys, os
# add = """C:/Users/carol/AppData/Roaming/inkscape/extensions/SimpInkScr/simpinkscr
# C:/Users/carol/AppData/Roaming/inkscape/extensions""".split('\n')
 

# for n, file in enumerate(add):
#     sys.path.insert(n, file) 
    
# from simple_inkscape_scripting import *
 
# 0,25π = 45
#  0,5π = 90
# 1π = 180
#  0,75π  = 135°
# 0,1666666667π = 30°
# 0,3333333333π = 60°
"""
Grados 	0° 	30° 	45° 	60° 	90° 	120° 	135° 	150° 	180° 	210° 	225° 	240° 	270° 	300° 	315° 	330° 	360°
Radianes 	0 	π/6 	π/4 	π/3 	π/2 	2π/3 	3π/4 	5π/6 	π 	7π/6 	5π/4 	4π/3 	3π/2 	5π/3 	7π/4 	11π/6 	2π

"""

# to use next time 
def radian(angle):
    rad = (angle * pi)/180
    return rad


    
    

"""
selected = selected_shapes() 
# selected = group(selected)
move_to_topleft(selected)

"""

# import inkex 
import os 

#%% Set up

def page_square():
    svg_root.set('width', 128)
    svg_root.set('height', 128)
    svg_root.set('viewBox', '0 0 128 128')
    
def page_history():
    page_w = 100
    page_h  = 128
    
    svg_root.set('width', page_w)
    svg_root.set('height', page_h)
    svg_root.set('viewBox', f'0 0 {page_w} {page_h}')
    
    return page_w, page_h
    


#%% Path 

def path():
    
    path = 'D:/Dropbox/Python/My_packages/MathGameScenes/images'
    path = 'D:/Dropbox/Python/My_packages/MultiInvaders/images'
    return path 
    

#%% Modules functions 

from my_scripts import lookup_dir as look 

def look_inkscape(obj, name):
    
    childs_names = look(obj, name, return_list = True)
    lst = list()
    for child in childs_names:
        print(f'box.{child} ,')
        lst.append(f'box.{child}')
        
    for child in lst:
        # print(child)
        try:
            eval(child)
            print(child,': ', eval(child))
        except:
            print(print(child,': FAIL'  ))
    return lst

def look_box(obj, name = None, noisy = False):
    """
    print values of a bounding box for inspection. 
    """
    
    # box = obj.bounding_box()
    if name is None:
        name = 'box'
    
    box_object = obj.bounding_box()
    box = dict()
    for var in  'left',  'top', 'right',  'bottom', 'width', 'height', 'center', 'center_x', 'center_y',    'x', 'y','maximum', 'minimum', 'get_anchor',   'new_xywh', 'resize', 'size'  , 'anchor_distance', 'area',:
        if noisy :
            print(f'{name}.{var}: ', eval(f'box_object.{var}'))
        box[var] = eval(f'box_object.{var}')
        
    return box
        
        
def move_to_topleft(obj, margin = None):
    obj.scale(0.5)

    box = look_box(obj)
    
    
    # move_x = - box['left']*pt  
    # move_y = - box['top']*pt 
    
    # print(canvas.true_width)
    # print(canvas.true_height)
    canvas.true_width = box['width']*pt
    canvas.true_height =  box['height']*pt
    # print(canvas.true_width)
    # print(canvas.true_height)
    
    # print(canvas.width)
    # # print(canvas.height)
    
    canvas.width =  box['width']*pt
    canvas.height =  box['height']*pt
    # # svg_root.set('width', box['width'])
    # # svg_root.set('height', box['height'])
    
    # # print(canvas.width)
    # # print(canvas.height)
    # svg_root.set('viewBox', [  (-box['left']*pt )  , ( -box['top']*pt)  ,box['width']*pt,   box['height']*pt ])
    
    # box = look_box(obj, noisy= True )
    
    # canvas.resize_to_content([obj])
    # print( obj.svg_get('x')    , obj.svg_get('y')  )
      
    # obj.translate(( - box['left']*pt , - box['top']*pt  ))
    # canvas.resize_to_content([obj])
 
    # box1 = obj.bounding_box()
    # look_bounding_box(box1, name = 'after')
     
#%% Home button
 
def home_button(color = 'red'):
    page_square()
    
    style(stroke_linecap='round',stroke =  color, stroke_width=10, stroke_linejoin='round')
    
    base_house = rect((32, 64), (96, 112), fill='none'  )
    roof = polygon([(16, 65), (64, 16), (112, 65)], fill=color)
    
    house = group([base_house, roof])

    path_ = os.path.join(path(), f'{color}_home.svg')
    save_file(path_)
    
    house.remove()
 


#%% Play button
def play_button(color = 'red'):
    page_square()
    
    style(stroke_linecap='round',stroke =  color, stroke_width=10, stroke_linejoin='round')
    play = regular_polygon(3, (50, 65), 116//2, -pi*2/3, fill=color)
    path_ = os.path.join(path(), f'{color}_play.svg')
    save_file(path_)
    
    play.remove()
 


#%% garbage colors 
def change_colors():
    # with template open! change different colors and save 
 
    for color in 'blue', 'green', 'grey', 'red':
        for obj in all_shapes():
            obj.style(stroke = color, fill =color)
            path_ = os.path.join(path(), f'{color}_garbage.svg')
            save_file(path_)
    


#%% History button 

# this is only part, as there som
def history_button(color = 'red'):
       
    page_w, page_h = page_history()
    
    h_unit = page_h/5
    w_unit = page_w/5

    x = w_unit + 10
    y = h_unit + 10
    
    style(stroke_linecap='round',stroke =  color, stroke_linejoin='round')
    paper = rect( (x,y),  (x + 3*w_unit, y + 3*h_unit))
    # circle((cx, cy), radius)
    
    # clock 
    circ= circle( (x,y), w_unit, fill = 'none', stroke_width=10)
    clock = circle( (x,y), w_unit, fill = 'none', stroke_width=10)
    line1 = line((x,y), (x + w_unit*2/5 ,y + w_unit*2/5), stroke_width=5 )
    line2 = line((x,y), (x  ,y - w_unit*2/5), stroke_width=5 )
    
    # paper lines 
    circ_box = circ.bounding_box()
    paper_box = paper.bounding_box()
    
    w = paper_box.width*2/3
    margin_x = paper_box.width - w
    h = paper_box.height -  circ_box.height/2
    y = circ_box.bottom
    x = paper_box.left + margin_x/2
    h_unit = h/4
    
    for i in range(4):
        line((x,y), (x+w , y), stroke_width=5  )
        y = y + h_unit
        
    circ = circ.to_path()
    paper = paper.to_path()
    contourn = apply_path_operation('union', [circ, paper])
    
 
    path_ = os.path.join(path(), 'template_history.svg')
    save_file(path_)
    
    
    
def history_colors():
    # with template open! change different colors and save 
    page_history()
    
    for color in 'blue', 'green', 'grey', 'red':
        for obj in all_shapes():
            obj.style(stroke = color)
            path_ = os.path.join(path(), f'{color}_history.svg')
            save_file(path_)
    
   
      
# history_button()
# history_colors()

 
#%% Mute Unmute button 


def sound_button(color = 'red', silence = False):
    
    svg_root.set('width', 150)
    svg_root.set('height', 128)
    svg_root.set('viewBox', '0 0 128 128')
    
    style(stroke_linecap='round',stroke =  color, stroke_width=10, stroke_linejoin='round')
    
    # magafono
    center_x = 50
    center_y = 65
    radius = 116//2
    angle = -pi*1/3 # 
    
    
    t = regular_polygon(3, (center_x, center_y), radius , angle , fill=color).to_path()
    s = rect(  (5.113 , 36.059) ,  (5.113 +36.021 , 36.059 + 57.184)  ,  fill= color  ).to_path()

    a,b,c  = apply_path_operation('division', [t, s])
    max_height = 0
    heights = list()
    for obj in  a,b,c:
        h = obj.bounding_box().height 
        heights.append(h)
        max_height = h if h > max_height else max_height
        
    for obj,h in  zip([a,b,c],heights) :
        if h < max_height:
            obj.remove()
        if h == max_height:
            trumpet = obj
     
    square = rect(  (5.113 , 36.059) ,  (5.113 +36.021 , 36.059 + 57.184)  , fill= color  ).to_path() 

    # circles 
    box = trumpet.bounding_box()
    x, y = box.right , box.center_y 
    h = box.height

    # arcs 
    """
    # 315, 45 grados 
    ang1 = 7*pi/4
    ang2 =  pi/4
    """
    # 300, 60 grados 
    ang1 = 5*pi/3
    ang2 =  pi/3
    
    # arc((cx, cy), (rx, ry), (ang1, ang2), arc_type)
    # arc((canvas.width/2, canvas.height/2), 100, (pi/5, 9*pi/5), 'slice', fill='yellow', stroke_width=2)
    arc1 =  arc( (x, y), h//2, (  ang1 ,ang2  ) ,   'arc', fill='none', stroke_width=10)
    arc2 =  arc( (x, y), ((h//2)*2/3), (ang1 , ang2) ,   'arc', fill='none', stroke_width=10)
    arc3 =  arc( (x, y), ((h//2)*1/3), ( ang1  , ang2) ,   'arc', fill='none', stroke_width=10)
    path_ = os.path.join(path(), f'{color}_sound.svg')
    save_file(path_)
    # silence line 
     
    line1 = line((5.13, 10), (120, 120), fill=color, stroke_width=10, stroke = color )
    path_ = os.path.join(path(), f'{color}_silence.svg')
    save_file(path_)
    
    items  = group([trumpet, square, arc1, arc2, arc3, line1])
    items.remove()
   
    
#%% Icon 
def icon():
    w, h = 128, 128
    svg_root.set('width', w)
    svg_root.set('height', h)
    svg_root.set('viewBox', f'0 0 {w} {h}')
    circ= circle( (w//2,h//2), (w*0.9)//2, fill = 'red', stroke_width=0)
    circ= circle( (w//2,h//2), (w*0.7)//2, fill = 'blue', stroke_width=0)
    circ= circle( (w//2,h//2), (w*0.4)//2, fill = 'yellow', stroke_width=0)
    path_ = os.path.join(path(),  'icon.svg')
    save_file(path_)
       


 
#%% Run 

 
# home_button()
# home_button('blue')
# home_button('green')
# home_button('grey')

# play_button()
# play_button('blue')
# play_button('green')
# play_button('grey')

# sound_button() 
# sound_button('blue')
# sound_button('green')
# sound_button('grey')



 




 
