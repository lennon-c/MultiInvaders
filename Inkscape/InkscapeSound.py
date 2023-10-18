# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:13:09 2023

@author: carol
"""

# from my_scripts import lookup_dir as look 

# for c in svg_root.iter():
#     if isinstance(c, inkex.ShapeElement) and not isinstance(c, inkex.Layer):
#         c.delete()
        
# def look_inkscape(obj, name):
#     childs_names = look(obj, name, return_list = True)
#     lst = list()
#     for child in childs_names:
#         print(f'box.{child} ,')
#         lst.append(f'box.{child}')
        
#     for child in lst:
#         # print(child)
#         try:
#             eval(child)
#             print(child,': ', eval(child))
#         except:
#             print(print(child,': FAIL'  ))
#     return lst





svg_root.set('width', 150)
svg_root.set('height', 128)
svg_root.set('viewBox', '0 0 128 128')

def sound_button(color = 'red', silence = False):
    
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
    
    # silence line 
    if silence:
        line1 = line((5.13, 10), (120, 120), fill=color, stroke_width=10, stroke = 'blue' )
        
    
    
sound_button()
 