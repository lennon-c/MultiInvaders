
import os


def root():
    """Give root of working tree adjusted to freeze, Spyder, and cmd line."""
    try:
        # print("using  __file__ object")
        root = os.path.dirname(os.path.abspath(__file__))
        # print(root)

    except:
        # print("using '__file__' string")
        root = os.path.dirname(os.path.abspath('__file__'))
        # print(root)
    return root


def c(constant=None):
    """Return dictionary of predefinided arguments to use in the game.

    Return a dictionary value if `constant` is given, otherwise return a copy of the dictionary.
    """
    dic = dict()
    # colors
    dic['colors'] = ['cadetblue3', 'dodgerblue1', 'gold', 'green2',
                     'deeppink1', 'coral', 'lightpink1', 'mediumorchid', 'red', 'darkorange']
    dic['palette'] = {1: 'turquoise3', 2: (
        187, 255, 51), 3: 'green', 4: (255, 255, 102)}# , 4: (251, 238, 172)}#

    dic['border_radius'] = 30
    # font
    dic['fontsize'] = 24
    dic['fontsize_small'] = 16
    dic['fontsize_medium'] = 18
    dic['fontsize_large'] = 30

    dic['fontname'] = 'comicsansms'  # None #  'papyrus' #   'ravie' #  'twcen' # 'calisto'  #    'javanesetext' # 'goudystout' # 'holomdl2assets' # 'inkfree'

    dic['second_numbers'] = None
    dic['n_alternatives'] = 6

    dic['score_correct'] = 1
    dic['score_incorrect'] = -1

    # circles/squares for players and alternatives, windows
    dic['rect_size'] = (80, 60)  # altenatives c('size')
    dic['circle_size'] = (80, 80) # c('player size')  
    
    n = dic['n_alternatives']
    w , h  = dic['circle_size']

    dic['height_window'] = h*n*1.4  

    add_marging = int(w/4)
    dic['width_window'] = (w*n) + add_marging * (n + 2)
    dic['width_mat'] = (w*n) + add_marging * (n - 1)

    # avatars
    dic['avatar_play_size'] = (65, 65)

    # paths
    dic['sounds_path'] = os.path.join(root(), 'sounds')
    dic['images_path'] = os.path.join(root(), 'images')
    dic['ico_path'] = os.path.join(root(), 'images')
    dic['root'] = root()

    # sounds
    dic['correct_sound'] = 'tick.wav'  # 'ding.wav'
    dic['wrong_sound'] = 'nope.wav'

    # default user settings
    image_path = os.path.join(dic['images_path'], '0_avatar.svg')
    dic['settings'] = {
        'selected_numbers': [1, 2, 3, 4, 5, 10]
        , 'selected_speed': 'normal'
        , 'selected_avatar': image_path
        , 'selected_game': 1
        , 'selected_variant' : "variant_1"
        , 'sound': True
                        }

    # installer
    dic['onefile'] = False
    name = 'MultiInvaders'
    dic['name'] = f'{name}App' if dic['onefile'] else name

    if constant is not None:
        return dic.get(constant, f'Constant {constant} not found')
    else:
        return dic 



