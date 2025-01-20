from fasthtml.common import *
from fasthtml.svg import *

app,rt = fast_app(hdrs=[Style(':root { --pico-font-size: 100%; }')], live=True)

count = 0

@rt('/')
def get():
    button = Svg(w=100, h=100)(
        Circle(
            20, 25, 25, 
            stroke='red', 
            stroke_width=3,
            id='goddamn_btn',
            hx_get='/increment/',
            target_id='count'))

    title = 'PUSH THE GODDAMN BUTTON!'

    button_presses = P(f'The goddamn button has been pushed {count}x', id='count')
    return Title(title), Main(H1(title), button, button_presses)

@rt('/increment/')
def get():
    global count
    
    count += 1

    return P(f'The goddamn button has been pushed {count}x')

serve()