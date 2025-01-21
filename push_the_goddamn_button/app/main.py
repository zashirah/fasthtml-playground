from fasthtml.common import *
from fasthtml.svg import *
import uvicorn
import asyncio


app,rt,counts,Count = fast_app('count.db', live=True,
                                hdrs=[Style(':root { --pico-font-size: 100%; }')],
                                id=int, value=int, pk='id')

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

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv("PORT", default=8000)))