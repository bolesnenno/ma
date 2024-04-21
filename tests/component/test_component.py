import requests

admin_url = 'http://localhost:8001'
get_tasks_url = f'{admin_url}/tasks'
get_task_by_id_url = f'{admin_url}/get_task_by_id'
add_task_url = f'{admin_url}/create_task'
delete_task_url = f'{admin_url}/delete_task'

new_task = {
    "id": 0,
    "time": "12:00:00",
    "text": "Finalize and submit the quarterly report"
}


def test_1_add_task():
    res = requests.post(f"{add_task_url}", json=new_task)
    assert res.status_code == 200


def test_2_get_tasks():
    res = requests.get(f"{get_tasks_url}").json()
    assert new_task in res


def test_3_get_task_by_id():
    res = requests.get(f"{get_task_by_id_url}?task_id=0").json()
    assert res == new_task


def test_4_delete_task():
    res = requests.delete(f"{delete_task_url}?task_id=0").json()
    assert res == {"message": "Task deleted successfully"}
