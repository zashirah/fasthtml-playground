from fasthtml.common import *
from fasthtml.svg import *

app,rt,counts,Count = fast_app('data/counts.db', live=True, 
    hdrs=[Style(':root { --pico-font-size: 100%; }')],
    id=int, value=int, pk='id',
    exts='ws'
)
try: counts[1]
except: counts.insert(Count(value=0))
count = counts[1]
pg13 = False

def update_image(pg13):
    if pg13: img_name = 'pushthegdbutton.jpeg'
    else: img_name = 'pushthebutton.jpeg'

    return Div(Img(src=img_name, hx_swap_oob='true', id='image'))

def update_count(): 
    return P(count.value, id='count')
    
def update_counter_txt(pg13):
    return P(f"Number of{' goddamn' if pg13 else ''} button pushes: ", hx_swap_oob='true', id='counter_txt')

def update_title(pg13):
    return H1(f'PUSH THE{" GODDAMN" if pg13 else ""} BUTTON!', id='title')

        
@rt('/')
def get():
    pg13_toggle = Label(
        "I want to see the PG-13 version", 
        Input(type='checkbox', role='switch', hx_get='/pg13')
    )

    button = Div(Svg(w=50, h=50)(
        Circle(
            20, 25, 25, 
            stroke='red', 
            stroke_width=3,
            id='goddamn_btn',
            ws_send=True)),
        hx_ext='ws',
        ws_connect='/ws'
    )
    
    button_push_txt = update_counter_txt(pg13)

    button_push_ct = update_count()

    button_push = Div(button_push_txt, button_push_ct)

    title_h = update_title(pg13)

    return Title("PUSH THE BUTTON"), Main(title_h, pg13_toggle, update_image(pg13), button, button_push)

users = {}
def on_conn(ws, send): users[str(id(ws))] = send
def on_disconn(ws): users.pop(str(id(ws)), None)
@app.ws('/ws', conn=on_conn, disconn=on_disconn)
async def ws(msg:str, send): 
    global pg13
    count.value = count.value + 1
    counts.update(count)
    for u in users.values(): 
        await u(update_count())

@rt('/pg13')
def get():
    global pg13
    pg13 = not pg13
    return update_title(pg13), update_image(pg13), update_counter_txt(pg13)

if __name__ == '__main__':
    serve()