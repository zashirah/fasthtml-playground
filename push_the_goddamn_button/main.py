from fasthtml.common import *
from fasthtml.svg import *
import uvicorn

app,rt,counts,Count = fast_app('data/counts.db', live=True, 
    hdrs=[Style(':root { --pico-font-size: 100%; }')],
    id=int, value=int, pk='id')

@rt('/')
def get():
    try: counts[1]
    except: counts.insert(Count(value=0))
    
    count = counts[1]

    button = Svg(w=100, h=100)(
        Circle(
            20, 25, 25, 
            stroke='red', 
            stroke_width=3,
            id='goddamn_btn',
            hx_get='/increment/1',
            target_id='count'))

    title = 'PUSH THE GODDAMN BUTTON!'

    button_presses = P(f'The goddamn button has been pushed {count.value}x', id='count')
    return Title(title), Main(H1(title), button, button_presses)

@rt('/increment/{cid}')
def get(cid:int):
    count = counts[cid]
    count.value = count.value + 1
    counts.update(count)
    return P(f'The goddamn button has been pushed {count.value}x')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv("PORT", default=8000)))