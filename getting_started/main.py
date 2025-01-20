from fasthtml.common import *


# tells the fast_app how you want to render the todos and needs to be passed into fastapp
def render(todo):
    tid = f'todo-{todo.id}'
    toggle = A('Toggle', hx_get=f'/toggle/{todo.id}', target_id=tid)
    delete = A('Delete', hx_delete=f'/{todo.id}', hx_swap='outerHTML', target_id=tid)
    return Li(
        toggle, 
        todo.title + (' done' if todo.done else ''), 
        delete,
        id=tid
    )

"""
todos = object containing the actual table
Todo = type of things in that table
"""
app,rt,todos,Todo = fast_app('todos.db', live=True, render=render,
                                id=int, title=str, done=bool, pk='id') # these are the table details

def mk_input(): return Input(placeholder='Add a todo', id='title', hx_swap_oob='true')

@rt('/')
def get(): 
    frm = Form(
        Group(
            mk_input(), 
            Button('Add')
        ), hx_post='/', target_id='todo-list', hx_swap='beforeend') 

    return Titled('Todos', 
                    Card(
                        Ul(*todos(), id='todo-list'),
                        header=frm)
                )

@rt('/toggle/{tid}')
def get(tid:int): # needs to be an int because that is what is defined in the table
    todo = todos[tid]
    todo.done = not todo.done
    return todos.update(todo)

@rt('/{tid}')
def delete(tid:int): todos.delete(tid) # needs to be an int because that is what is defined in the table
    
@rt('/')
def post(todo:Todo): return todos.insert(todo), mk_input()

serve()
