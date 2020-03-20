import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')
                print(response)
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                resp = client.post('/store/test')
                expected = {'message': "A store with name 'test' already exists."}
                self.assertEqual(resp.status_code, 400)
                self.assertEqual(json.loads(resp.data),  {'message': "A store with name 'test' already exists."})

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                self.assertIsNotNone(StoreModel.find_by_name('test'))

                resp = client.delete('/store/test')

                self.assertEqual(json.loads(resp.data), {'message': 'Store deleted'})
                self.assertIsNone(StoreModel.find_by_name('test'))


    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                self.assertIsNotNone(StoreModel.find_by_name('test'))

                resp = client.get('/store/test')
                self.assertEqual(json.loads(resp.data), {'name': 'test', 'items': []})

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/store/test')
                self.assertEqual(json.loads(resp.data), {'message': 'Store not found'})
                self.assertEqual(resp.status_code, 404)

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('test')
                store.items = [ItemModel('book', 20, 1)]
                store.save_to_db()

                resp = client.get('/store/test')
                self.assertEqual(json.loads(resp.data), {'name': 'test', 'items': [{'name': 'book', 'price': 20}]})

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test1').save_to_db()

                resp = client.get('/stores')
                self.assertDictEqual(json.loads(resp.data), {'stores': [{'name': 'test1', 'items': []}]})
