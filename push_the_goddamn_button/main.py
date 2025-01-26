from fasthtml.common import *
from fasthtml.svg import *


css = Style('''
article { text-align: center }
img { height: 200px }
button { height: 75px; width: 150px; margin: 10px; padding: 1px}
header { text-align: center }
''')

app,rt,counts,Count = fast_app('data/counts.db', live=True, 
    hdrs=[Style(':root { --pico-font-size: 100%; }'), css],
    id=int, value=int, pk='id',
    exts='ws'
)
try: counts[1]
except: counts.insert(Count(value=0))
count = counts[1]
pg13 = False

def update_image(pg13): return Div(Img(src=f'pushthe{"gd" if pg13 else ""}button.jpeg'), hx_swap_oob='true', id='image')

def update_count(): return B(count.value, id='count', style='text-align: left')
    
def update_counter_txt(pg13): return Div(f"Number of{' goddamn' if pg13 else ''} button pushes: ", hx_swap_oob='true', id='counter_txt')

def update_title(pg13): return H1(f'PUSH THE{" GODDAMN" if pg13 else ""} BUTTON!', hx_swap_oob='true', id='title')

def update_button(pg13): return Div(Button(f"this {'goddamn ' if pg13 else ''}button", id='goddamn_btn', hx_swap_oob='true', ws_send=True), hx_ext='ws', ws_connect='/ws')

@rt('/')
def get():
    pg13_toggle = Label(
        "I want to see the PG-13 version", 
        Input(type='checkbox', role='switch', hx_get='/pg13')
    )

    button_push_txt = update_counter_txt(pg13)

    button_push_ct = update_count()

    title_h = update_title(pg13)

    header = Grid(title_h, pg13_toggle)

    return Title("PUSH THE BUTTON"), Main(Header(header), Card(update_image(pg13), update_button(pg13), Div(button_push_txt, button_push_ct)))

users = {}
def on_conn(ws, send): users[str(id(ws))] = send
def on_disconn(ws): users.pop(str(id(ws)), None)

@app.ws('/ws', conn=on_conn, disconn=on_disconn)
async def ws(msg:str, send): 
    count.value = count.value + 1
    counts.update(count)
    for u in users.values(): await u(update_count())

@rt('/pg13')
def get():
    global pg13
    pg13 = not pg13
    return update_title(pg13), update_image(pg13), update_counter_txt(pg13), update_button(pg13)

if __name__ == '__main__': serve()