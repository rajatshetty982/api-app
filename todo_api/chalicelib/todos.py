import os
import json
import psycopg2
from chalice import Blueprint
from chalice import Response
from chalicelib.dbConnections import getDbConnection
from chalicelib.dbSchema import 

app = Blueprint(__name__)


@app.route('/test')
def test():
    return {'Test': 'Successful'}

@app.route('/todos', methods=['GET'])
def get_todo():
    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM todo_tasks;')
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()

        task_list = []
        for task in tasks:
            task_list.append({
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'start_date': task[3].isoformat() if isinstance(task[3], datetime.date) else None,
                'finished': task[4],
            })

        return {'tasks': task_list}
    except psycopg2.Error as e:
        errMessage = {'error': 'Database error', 'message': str(e)}
        return Response(body=errMessage, status_code=500, headers={'Content-Type': 'application/json'})
    except Exception as e:
        errMessage = {'error': 'Internal server error', 'message': str(e)}
        return Response(body=errMessage, status_code=500, headers={'Content-Type': 'application/json'})


@app.route('/todos', methods=['POST'])
def create_todo():
    try:
        request = app.current_request
        todo_data = request.json_body
        
        title = todo_data.get('title')
        description = todo_data.get('description', '')
        start_date = todo_data.get('start_date')
        finished = todo_data.get('finished', False)

        if not title:
            errMessage = {'error': 'Title is required'}
            return Response(body=errMessage, status_code=400, headers={'Content-Type': 'application/json'})

        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%d-%m-%Y').date()  # Validate format
            except ValueError:
                errMessage = {'error': 'Invalid date format. Use DD-MM-YYYY.'}
                return Response(body=errMessage, status_code=400, headers={'Content-Type': 'application/json'})


        conn = getDbConnection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO todo_tasks (title, description, finished) VALUES (%s, %s, %s) RETURNING id", 
            (title, description, finished)
        )
        new_id = cursor.fetchone()[0]

        conn.commit()
        conn.close()

        responseMessage = {
            'id': new_id,
            'title': title,
            'description': description,
            'start_date': start_date,
            'finished': finished
        }
        return Response(body=responseMessage, status_code=201, headers={'Content-Type': 'application/json'})

    except psycopg2.Error as db_error:
        errMessage =  {'error': 'Database operation failed', 'message': str(db_error)}
        return  Response(body=errMessage, status_code=500, headers={'Content-Type': 'application/json'})

    except Exception as e:
        errMessage = {"Unexpected error": str(e)}
        return Response(body=errMessage, status_code=500, headers={'Content-Type': 'application/json'})

@app.route('/todos/{task_id}', methods=['PATCH'])
def complete_taks(task_id):
    try:
        if not task_id.isdigit():
            errMessage = {'error': 'Invalid task ID. It must be numeric.'}
            return Response(body=errMessage, status_code=400, headers={'Content-Type': 'application/json'})

        request = app.current_request
        todo_data = request.json_body

        finished = todo_data.get('finished')

        if finished is None:
            errMessage = {'error': 'Finish status is required'}
            return Response(body=errMessage, status_code=400, headers={'Content-Type': 'application/json'})

        conn = getDbConnection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE todo_tasks
            SET finished = %s
            WHERE id = %s
            RETURNING id, title, finished
        """, (finished, task_id))

        update_task = cursor.fetchone()

        if not update_task:
            errMessage = {'error': 'task Id not found!'}
            return Response(body=errMessage, status_code=400, headers={'Content-Type': 'application/json'})

        conn.commit()
        conn.close()

        responseMessage = {
            'id': update_task[0],
            'title': update_task[1],
            'finished': update_task[2]
        }
        return Response(body=responseMessage, status_code=200, headers={'Content-Type': 'application/json'})

    except psycopg2.Error as db_error:
        errMessage = {'error': 'Database operation failed', 'message': str(db_error)}
        return Response(body=errMessage, status_code=500, headers={'Content-Type': 'application/json'})

    except Exception as e:
        errMessage =  {'error': 'Failed to update todo item', 'message': str(e)}
        return Response(body=errMessage, status_code=500, headers={'Content-Type': 'application/json'})

@app.route('/todos/{task_id}', methods=['DELETE'])
def delete_task(task_id):
    try:
        if not task_id.isdigit():
            errMessage = {'error': 'Invalid task ID. It must be numeric.'}
            return Response(body=errMessage, status_code=400, headers={'Content-Type': 'application/json'})

        # Connect to the database
        conn = getDbConnection()
        cursor = conn.cursor()

        # Delete the task by ID
        cursor.execute("""
            DELETE FROM todo_tasks
            WHERE id = %s
            RETURNING id
        """, (task_id,))

        deleted_task = cursor.fetchone()

        conn.commit()
        conn.close()

        if not deleted_task:
            errMessage = {'error': f'Task with ID {task_id} does not exist'}
            return Response(body=errMessage, status_code=404, headers={'Content-Type': 'application/json'})

        responseMessage = {'message': f'Task with ID {task_id} deleted successfully'}
        return Response(body=responseMessage, status_code=200, headers={'Content-Type': 'application/json'})

    except psycopg2.Error as db_error:
        errMessage = {'error': 'Database operation failed', 'message': str(db_error)}
        return Response(body=errMessage, status_code=500, headers={'Content-Type': 'application/json'})

    except Exception as e:
        errMessage = {'error': 'Failed to delete todo item', 'message': str(e)}
        return Response(body=errMessage, status_code=500, headers={'Content-Type': 'application/json'})

