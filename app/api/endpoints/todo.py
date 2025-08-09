from fastapi import APIRouter, HTTPException
from db.database import database
from ..shemas.todo import ResponseTodo, CreateTodo, ChangeTodo
from typing import List



router = APIRouter(
    prefix='/todo',
    tags=['TODOS'],
)


@router.get('/{id_user}', response_model=list[ResponseTodo], description='Getting user tasks')
async def get_todos(id_user: int):
    try:
        query = 'SELECT title, description, created_at, complete FROM tasks WHERE user_id = :id_user'

        result = await database.fetch_all(query=query, values={'id_user': id_user})

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Задачи для пользователя с указанным ID не найдены"
            )

        todos = []
        for row in result:
            todo = ResponseTodo(
                title=row['title'],
                description=row['description'],
                created_at=row['created_at'],
                complete=row['complete']
            )
            todos.append(todo)
        
        return todos
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении задач: {str(e)}"
        )
    

@router.post('/create_todo', description='Create tasks')
async def create_todo(todo: CreateTodo):
    try:
        if todo.description is None:
            query = 'INSERT INTO tasks(title, user_id) VALUES (:title, :id_user)'
            values = {'title': todo.title, 'id_user': todo.user_id}
        else: 
            query = 'INSERT INTO tasks(title, description, user_id) VALUES (:title, :description, :id_user)'
            values = {'title': todo.title, 'id_user': todo.user_id, 'description': todo.description}

        await database.execute(query=query, values=values)

        return {'success': 'New task created'}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при создании задачи: {str(e)}"
        )
    

@router.patch('/change_status/{id_task}', description='Task status changes')
async def change_status(id_task: int, status: int):
    try:
      select_task = 'SELECT * FROM tasks where id_task = :id_task'
      task = await database.fetch_one(query=select_task, values={'id_task': id_task})

      
      if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Задача не найдена!"
        )
      

      query = 'UPDATE tasks SET complete = :status WHERE id_task = :id_task'
      await database.execute(query=query, values={'status': status, 'id_task': id_task})

      if status == 1:
          return {'success': 'You have completed the task!'}
      else:
          return {'success': 'You need to complete the task!'}
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка изменения статуса: {str(e)}"
        )
    

@router.put('/change_task/{id_task}', description='Task changes')
async def change_todo(todo: ChangeTodo):
    try:
        select_task = 'SELECT * FROM tasks where id_task = :id_task'
        task = await database.fetch_one(query=select_task, values={'id_task': todo.id_task})

        if not task:
            raise HTTPException(
                status_code=404,
                detail=f"Задача не найдена!"
                )
        
        update_query = 'UPDATE tasks SET title = :title, description = :description WHERE id_task = :id_task'

        await database.execute(query=update_query, values={'title': todo.title, 'description': todo.description, 'id_task': todo.id_task})

        return {'success': 'The task has been changed!'}
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка изменения статуса: {str(e)}"
        )
    
    