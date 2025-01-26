from fasthtml.common import *
from fasthtml.svg import *
import uvicorn

if __name__ == "__main__": sys.exit("Run this app with `uvicorn main:app`")

app,rt,counts,Count = fast_app('data/counts.db', live=True, 
    hdrs=[Style(':root { --pico-font-size: 100%; }')],
    id=int, value=int, pk='id',
    exts='ws'
)
try: counts[1]
except: counts.insert(Count(value=0))
count = counts[1]

@rt('/')
def get():
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

    title = 'PUSH THE GODDAMN BUTTON!'

    img = Div(Img(src='pushthegdbutton.jpeg'))

    button_presses = P(f'The goddamn button has been pushed {count.value}x', id='count')
    return Title(title), Main(H1(title), img, button, button_presses)

users = {}
def on_conn(ws, send): users[str(id(ws))] = send
def on_disconn(ws): users.pop(str(id(ws)), None)

async def update_count():
    for u in users.values(): 
        await u(P(f'The goddamn button has been pushed {count.value}x', id='count'))

@app.ws('/ws', conn=on_conn, disconn=on_disconn)
async def ws(msg:str, send): 
    count.value = count.value + 1
    counts.update(count)
    await update_count()
