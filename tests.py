import pytest
import requests

# CRUD
BASE_URL = "http://127.0.0.1:5000"
tasks = []


# Create
def test_create_task():
    new_task = {"title": "Nova tarefa", "description": "Descrição nova tarefa"}
    # toda requisição retorna uma resposta, no caso o requests.post cria essa requisição
    response = requests.post(f"{BASE_URL}/tasks", json=new_task)
    assert response.status_code == 200
    # o teste ocorre aqui no assert, para validar se retonou 200
    response_json = response.json()
    print("\nConteúdo do response_json:", response_json)
    assert "message" in response_json
    assert "id" in response_json
    tasks.append(response_json["id"])


# Read
def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    response_json = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json


def test_get_task_id():
    if tasks:
        task_id = tasks[0]
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert task_id == response_json["id"]


# Update
def test_update_task():
    payload = {
        "title": "Título atualizado",
        "description": "Descrição nova tarefa",
        "completed": True,
    }
    if tasks:
        task_id = tasks[0]
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json

        # Nova requisição, para testar se os valores foram alterados
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["title"] == payload["title"]
        assert response_json["description"] == payload["description"]
        assert response_json["completed"] == payload["completed"]


def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404
