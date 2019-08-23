from peewee import SqliteDatabase

import unittest
import json

import app
import models

BASE_URL = 'http://127.0.0.1:5000/api/v1/todos'
BAD_URL = '{}/99'.format(BASE_URL)
GOOD_URL = '{}/1'.format(BASE_URL)


test_db = SqliteDatabase(':memory:')
MODELS = [models.Todo]
    
class TestApi(unittest.TestCase):

    def setUp(self):
        test_db.bind(MODELS)
        test_db.connect(reuse_if_open=True)
        test_db.create_tables(MODELS, safe=True)
        models.Todo.create(name='finish project', completed=False)
        self.app = app.app.test_client()

    def tearDown(self):
        test_db.close()

    def test_get_todo_list(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['todos']), 1)

    def test_get_one_todo(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['todos'][0]['name'], 'finish project')

    def test_todo_does_not_exist(self):
        response = self.app.get(BAD_URL)
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        # missing value field
        todo = {}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(todo),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # valid field provided
        todo = {"name": "wash floors"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(todo),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['id'], 2)
        self.assertEqual(data['name'], 'wash floors')

    def test_update(self):
        todo = {"name": 'finish project', 'completed': True}
        response = self.app.put(GOOD_URL,
                                data=json.dumps(todo),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['completed'], True)

    def test_delete(self):
        response = self.app.delete(GOOD_URL)
        self.assertEqual(response.status_code, 204)

    
if __name__ == "__main__":
    unittest.main()