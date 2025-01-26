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

def update_counter_txt(pg13):
    return P(f"The{' goddamn' if pg13 else ''} button has been pushed {count.value}x", hx_swap_oob='true', id='count')

def update_title(pg13):
    return H1(f'PUSH THE{" GODDAMN" if pg13 else ""} BUTTON!', id='title')
        
@rt('/')
def get():
    pg13_toggle = Label(
        "I want to see the PG-13 version", 
        Input(type='checkbox', role='switch', hx_get='/pg13', target_id='title')
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
    
    title = f'PUSH THE{" GODDAMN" if pg13 else ""} BUTTON!'

    button_presses = update_counter_txt(pg13)

    title_h = update_title(pg13)

    return Title(title), Main(title_h, pg13_toggle, update_image(pg13), button, button_presses, cls='main')

users = {}
def on_conn(ws, send): users[str(id(ws))] = send
def on_disconn(ws): users.pop(str(id(ws)), None)

async def update_count():
    global pg13
    for u in users.values(): 
        await u(update_counter_txt(pg13))

@app.ws('/ws', conn=on_conn, disconn=on_disconn)
async def ws(msg:str, send): 
    count.value = count.value + 1
    counts.update(count)
    await update_count()

@rt('/pg13')
def get():
    global pg13
    pg13 = not pg13
    return update_title(pg13), update_image(pg13), update_counter_txt(pg13)

if __name__ == '__main__':
    serve()