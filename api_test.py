
from io import BytesIO
import unittest
from flask import jsonify
import json
from faker import Faker
from app import app

class TestLoginClass(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_login(self):
        # admin login
        data = {
            'email': 'admin@admin.com',
            'password': 'admin'
        }
        res = self.app.post('/api/user/login', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # user login
        data = {
            'email': '2826232264@qq.com',
            'password': '200212'
        }
        res = self.app.post('/api/user/login', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        data = {
            'email': '2826232264@qq.com',
            'password':'123456'
        }
        res = self.app.post('/api/user/login', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        data = {
            'email': '2826232264@qq.com',
            'password': ''
        }
        res = self.app.post('/api/user/login', data=json.dumps(data), content_type='application/json')
        # print(type(res))
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        data = {
            'email': '',
            'password': 'password',
        }
        res = self.app.post('/api/user/login', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        data = {
            'email': '',
            'password': '',
        }
        res = self.app.post('/api/user/login', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        faker_en = Faker('en_US')
        data_list = []
        for i in range(100):
            data_list.append({
                'email': str(faker_en.email()),
                'password': str(faker_en.password())
            })
        # print(data_list)
        for data in data_list:
            res = self.app.post('/api/user/login', data=json.dumps(data), content_type='application/json')
            res_dict = json.loads(res.data)
            self.assertIn('code', res_dict)
            self.assertEqual(res_dict['code'], 400)

    def test_captcha(self):
        data = {
            'email': 'test@test.com',
        }
        res = self.app.post('/api/user/captcha', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        data = {
            'email': '',
        }
        res = self.app.post('/api/user/captcha', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_register(self):
        data = {
            'email': '',
            'password': '',
            'captcha': '',
        }
        res = self.app.post('/api/user/register', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        data = {
            'email': '',
            'password': '',
            'captcha': '',
        }
        res = self.app.post('/api/user/register', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

class TestIndexClass(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        email = '2826232264@qq.com'
        res = self.app.post('/api/user/login', data=json.dumps({'email': email, 'password': '200212'}),
                                content_type='application/json')
        res_dict = json.loads(res.data)
        print("res_dict:", res_dict)
        self.token = res_dict['token']

    def tearDown(self):
        pass

    def test_logout(self):
        res = self.app.post('/api/user/logout', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        res = self.app.post('/api/user/logout')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

    def test_username(self):
        res = self.app.get('/api/user/username?id=1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        res = self.app.get('/api/user/username?id=2', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        res = self.app.get('/api/user/username?id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        res = self.app.get('/api/user/username?id=1')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        res = self.app.get('/api/user/username?id=')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

    def test_make_friend(self):

        # ????????????
        self.app.delete('/api/user/make_friend?user1_id=1&user2_id=2',headers={'token': self.token}, content_type='application/json')
        che = self.app.get('/api/user/make_friend?user1_id=1&user2_id=2', headers={'token': self.token}, content_type='application/json')
        self.assertEqual(che.data, b'0\n') #??????????????????????????????

        # ????????????
        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.post('/api/user/make_friend',data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????????????????
        che = self.app.get('/api/user/make_friend?user1_id=1&user2_id=2', headers={'token': self.token}, content_type='application/json')
        self.assertEqual(che.data, b'1\n')

        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.post('/api/user/make_friend',data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????
        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.delete('/api/user/make_friend?user1_id=1&user2_id=2', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????????????????????????????????????????
        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.post('/api/user/make_friend', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????????????????????????????????????????
        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.post('/api/user/make_friend',data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????token
        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.post('/api/user/make_friend', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # ???????????????????????????????????????
        data = {
            'user1_id': '1',
            'user2_id': '1',
        }
        res = self.app.post('/api/user/make_friend', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)
        self.assertEqual(res_dict['message'], "You can't add yourself as a friend!")

        # ???????????????????????????????????????????????????
        data = {
            'user1_id': '',
            'user2_id': '2',
        }
        res = self.app.post('/api/user/make_friend', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        data = {
            'user1_id': '1',
            'user2_id': '',
        }
        res = self.app.post('/api/user/make_friend', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        data = {
            'user1_id': '',
            'user2_id': '',
        }
        res = self.app.post('/api/user/make_friend', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????????????????????????????
        res = self.app.delete('/api/user/make_friend?user1_id=&user2_id=2', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        res = self.app.delete('/api/user/make_friend?user1_id=1&user2_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        res = self.app.delete('/api/user/make_friend?user1_id=&user2_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_friends(self):
        # ????????????????????????
        res = self.app.get('/api/user/friends', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????token
        res = self.app.get('/api/user/friends', content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

    def test_avatar(self):
        # ??????????????????
        data = {
            'file': (BytesIO(b"abcdef"), 'test.jpg'),
        }
        res = self.app.post('/api/user/avatar', data=data, headers={'token': self.token}, content_type='multipart/form-data')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????token
        data = {
            'file': (BytesIO(b"abcdef"), 'test.jpg'),
        }
        res = self.app.post('/api/user/avatar', data=data, content_type='multipart/form-data')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # ??????????????????
        res = self.app.post('/api/user/avatar', headers={'token': self.token}, content_type='multipart/form-data')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_profile(self):
        # ????????????????????????
        res = self.app.get('/api/user/profile?id=1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????token
        res = self.app.get('/api/user/profile?id=1', content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # ????????????user_id
        res = self.app.get('/api/user/profile', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????????????????
        res = self.app.get('/api/user/profile?id=100', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????
        data = {
            'id' : '1',
            'username' : 'test',
            'address' : 'test',
            'tel' : 'test',
            'remarks' : 'test',
            'place': 'test',
        }
        res = self.app.post('/api/user/profile', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????token
        data = {
            'id'    : '1',
            'username' : 'test',
            'address' : 'test',
            'tel' : 'test',
            'remarks' : 'test',
            'place': 'test',
        }
        res = self.app.post('/api/user/profile', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # ??????????????????
        data = {
            'id'    : '',
            'username' : '',
            'address' : '',
            'tel' : '',
            'remarks' : '',
            'place': '',
        }
        res = self.app.post('/api/user/profile',data = json.dumps(data) ,headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????????????????
        data = {
            'id'    : '100',
            'username' : 'test',
            'address' : 'test',
            'phone' : 'test',
            'remarks' : 'test',
            'place': 'test',
        }
        res = self.app.post('/api/user/profile', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ?????????????????????????????????id
        data = {
            'id' : '',
            'username' : 'test',
            'address' : 'test',
            'phone' : 'test',
            'remarks' : 'test',
            'place': 'test',
        }
        res = self.app.post('/api/user/profile', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_group(self):
        # ?????????????????????
        res = self.app.get('/api/user/group', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????token
        res = self.app.get('/api/user/group', content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

class TestSession(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        email = '2826232264@qq.com'
        res = self.app.post('/api/user/login', data=json.dumps({'email': email, 'password': '200212'}),
                                content_type='application/json')
        res_dict = json.loads(res.data)
        print("res_dict:", res_dict)
        self.token = res_dict['token']

    def tearDown(self):
        pass

    def test_session(self):
        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????token
        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # ??????????????????
        data = {
            'user1_id': '',
            'user2_id': '',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????user1_id
        data = {
            'user1_id': '',
            'user2_id': '2',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????user2_id
        data = {
            'user1_id': '1',
            'user2_id': '',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????user1_id?????????
        data = {
            'user1_id': '100',
            'user2_id': '2',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????user2_id?????????
        data = {
            'user1_id': '1',
            'user2_id': '100',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????user1_id???user2_id??????
        data = {
            'user1_id': '1',
            'user2_id': '1',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????user1_id???user2_id????????????
        data = {
            'user1_id': '100',
            'user2_id': '100',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????
        res = self.app.get('/api/session/session?session_id=2', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????????????????token
        res = self.app.get('/api/session/session?session_id=2', content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # ??????????????????????????????session_id
        res = self.app.get('/api/session/session', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????session_id?????????
        res = self.app.get('/api/session/session?session_id=100', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????session_id????????????
        res = self.app.get('/api/session/session?session_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????session_id?????????
        res = self.app.get('/api/session/session?session_id=1.1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????session_id?????????
        res = self.app.get('/api/session/session?session_id=-1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????session_id???0
        res = self.app.get('/api/session/session?session_id=0', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????session_id???????????????
        res = self.app.get('/api/session/session?session_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????session_id?????????
        res = self.app.get('/api/session/session?session_id= ', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????session_id????????????
        res = self.app.get('/api/session/session?session_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_message(self):
        # ??????????????????
        res = self.app.get('/api/session/message?session_id=2', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????????????????token
        res = self.app.get('/api/session/message?session_id=2', content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # ????????????????????????session_id
        res = self.app.get('/api/session/message', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id?????????
        res = self.app.get('/api/session/message?session_id=100', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id????????????
        res = self.app.get('/api/session/message?session_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id?????????
        res = self.app.get('/api/session/message?session_id=1.1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id?????????
        res = self.app.get('/api/session/message?session_id=-1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id???0
        res = self.app.get('/api/session/message?session_id=0', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id???????????????
        res = self.app.get('/api/session/message?session_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id?????????
        res = self.app.get('/api/session/message?session_id= ', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????
        data = {
            'session_id': '2',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????????????????token
        res = self.app.post('/api/session/message', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # ????????????????????????session_id
        data = {
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????content
        data = {
            'session_id': '2'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id?????????
        data = {
            'session_id': '100',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id????????????
        data = {
            'session_id': 'abc',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id?????????
        data = {
            'session_id': '1.1',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id?????????
        data = {
            'session_id': '-1',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id???0
        data = {
            'session_id': '0',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id???????????????
        data = {
            'session_id': '',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id?????????
        data = {
            'session_id': ' ',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????content???????????????
        data = {
            'session_id': '2',
            'content': ''
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????content?????????
        data = {
            'session_id': '2',
            'content': ' '
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????content??????
        data = {
            'session_id': '2',
            'content': None
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????content?????????
        data = {
            'session_id': '2',
            'content': '123'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????content?????????
        data = {
            'session_id': '2',
            'content': '1.1'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????content?????????
        data = {
            'session_id': '2',
            'content': '-1'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????content???????????????
        data = {
            'session_id': '2',
            'content': '!@#$%^&*()_+'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????content?????????
        data = {
            'session_id': '2',
            'content': '??????'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????content?????????
        data = {
            'session_id': '2',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????content??????????????????
        data = {
            'session_id': '2',
            'content': 'test123'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????content????????????????????????
        data = {
            'session_id': '2',
            'content': 'test!@#$%^&*()_+'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????content??????????????????
        data = {
            'session_id': '2',
            'content': 'test??????'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????content????????????????????????
        data = {
            'session_id': '2',
            'content': '123!@#$%^&*()_+'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????content??????????????????
        data = {
            'session_id': '2',
            'content': '123??????'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????content????????????????????????
        data = {
            'session_id': '2',
            'content': '!@#$%^&*()_+??????'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????content??????????????????????????????????????????
        data = {
            'session_id': '2',
            'content': 'test123!@#$%^&*()_+??????'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????
        res = self.app.delete('/api/session/message?message_id=6', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id?????????
        res = self.app.delete('/api/session/message?message_id=10000', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id????????????
        res = self.app.delete('/api/session/message?message_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id??????
        res = self.app.delete('/api/session/message?message_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id?????????
        res = self.app.delete('/api/session/message?message_id=-1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id???0
        res = self.app.delete('/api/session/message?message_id=0', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id?????????
        res = self.app.delete('/api/session/message?message_id=1.1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id????????????
        res = self.app.delete('/api/session/message?message_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id???????????????
        res = self.app.delete('/api/session/message?message_id=!@#$%^&*()_+', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id?????????
        res = self.app.delete('/api/session/message?message_id=??????', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id??????????????????????????????????????????
        res = self.app.delete('/api/session/message?message_id=test123!@#$%^&*()_+??????', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_upload(self):
        # ??????????????????
        data = {
            'file': (BytesIO(b'test'), 'test.txt')
        }
        res = self.app.post('/api/session/upload', headers={'token': self.token, 'id':"11"}, data=data, content_type='multipart/form-data')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????session_id?????????
        data = {
            'file': (BytesIO(b'test'), 'test.txt')
        }
        res = self.app.post('/api/session/upload', headers={'token': self.token, 'id':"10000"}, data=data, content_type='multipart/form-data')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id????????????
        data = {
            'file': (BytesIO(b'test'), 'test.txt')
        }
        res = self.app.post('/api/session/upload', headers={'token': self.token, 'id':"abc"}, data=data, content_type='multipart/form-data')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????session_id??????
        data = {
            'file': (BytesIO(b'test'), 'test.txt')
        }
        res = self.app.post('/api/session/upload', headers={'token': self.token, 'id':"  "}, data=data, content_type='multipart/form-data')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_upload_file_content(self):
        # ????????????????????????
        data = {
            'content': "test",
            'session_id': "2",
        }
        res = self.app.post('/api/session/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????????????????session_id?????????
        data = {
            'content': "test",
            'session_id': "1000",
        }
        res = self.app.post('/api/session/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????session_id??????
        data = {
            'content': "test",
            'session_id': "  ",
        }
        res = self.app.post('/api/session/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????session_id????????????
        data = {
            'content': "test",
            'session_id': "abc",
        }
        res = self.app.post('/api/session/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????content??????
        data = {
            'content': "  ",
            'session_id': "2",
        }
        res = self.app.post('/api/session/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

class TestGroup(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        email = '2826232264@qq.com'
        res = self.app.post('/api/user/login', data=json.dumps({'email': email, 'password': '200212'}),
                                content_type='application/json')
        res_dict = json.loads(res.data)
        print("res_dict:", res_dict)
        self.token = res_dict['token']

    def tearDown(self):
        pass

    def test_create_group(self):
        # ??????????????????
        data = {
            "users": [11, 12, 13],
            "name": "test",
            "user2_id": "11",
        }
        res = self.app.post('/api/group/group', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????users??????
        data = {
            "users": [],
            "name": "test",
            "user2_id": "1",
        }
        res = self.app.post('/api/group/group', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????users????????????
        data = {
            "users": "1",
            "name": "test",
            "user2_id": "1",
        }
        res = self.app.post('/api/group/group', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????user2_id????????????
        data = {
            "users": [1, 2, 3],
            "name": "test",
            "user2_id": "abc",
        }
        res = self.app.post('/api/group/group', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????user2_id??????
        data = {
            "users": [1, 2, 3],
            "name": "test",
            "user2_id": "  ",
        }
        res = self.app.post('/api/group/group', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????name??????
        data = {
            "users": [1, 2, 3],
            "name": "  ",
            "user2_id": "1",
        }
        res = self.app.post('/api/group/group', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        res = self.app.get('/api/group/group?group_id=1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????????????????group_id
        res = self.app.get('/api/group/group?group_id=200', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????group_id?????????
        res = self.app.get('/api/group/group?group_id=  ', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????group_id????????????
        res = self.app.get('/api/group/group?group_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????group_id??????
        res = self.app.get('/api/group/group?group_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_message(self):
        # ????????????????????????
        res = self.app.get('/api/group/message?group_id=1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????????????????group_id
        res = self.app.get('/api/group/message?group_id=200', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????group_id?????????
        res = self.app.get('/api/group/message?group_id= ', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????group_id????????????
        res = self.app.get('/api/group/message?group_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????group_id??????
        res = self.app.get('/api/group/message?group_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????
        data = {
            "group_id": 1,
            "content": "test",
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????????????????group_id
        data = {
            "group_id": 200,
            "content": "test",
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????group_id?????????
        data = {
            "group_id": " ",
            "content": "test",
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????group_id????????????
        data = {
            "group_id": "abc",
            "content": "test",
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????group_id??????
        data = {
            "group_id": "",
            "content": "test",
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????content??????
        data = {
            "group_id": 1,
            "content": "",
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????content?????????
        data = {
            "group_id": 1,
            "content": " ",
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????content???None
        data = {
            "group_id": 1,
            "content": None,
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????content?????????
        data = {
            "group_id": 1,
            "content": 123,
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????
        res = self.app.delete('/api/group/message?message_id=12', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????????????????
        res = self.app.delete('/api/group/message?message_id=1000', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id??????
        res = self.app.delete('/api/group/message?message_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id?????????
        res = self.app.delete('/api/group/message?message_id= ', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id???None
        res = self.app.delete('/api/group/message?message_id=None', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id????????????
        res = self.app.delete('/api/group/message?message_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id?????????
        res = self.app.delete('/api/group/message?message_id=1.1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id?????????
        res = self.app.delete('/api/group/message?message_id=-1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????message_id???0
        res = self.app.delete('/api/group/message?message_id=0', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_upload(self):
        # ??????????????????
        data = {
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': '11'}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ??????????????????group_id?????????
        data = {
            "group_id": 1000,
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': '1'}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????group_id??????
        data = {
            "group_id": "",
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': '1'}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????group_id?????????
        data = {
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': ' '}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????group_id???None
        data = {
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': None}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????group_id????????????
        data = {
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': 'abc'}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????group_id?????????
        data = {
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': '1.1'}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????group_id?????????
        data = {
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': '-1'}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ??????????????????group_id???0
        data = {
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': '0'}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_upload_file_content(self):
        # ????????????????????????
        data = {
            'content': "test",
            'group_id': "2",
        }
        res = self.app.post('/api/group/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # ????????????????????????group_id?????????
        data = {
            'content': "test",
            'group_id': "1000",
        }
        res = self.app.post('/api/group/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????group_id??????
        data = {
            'content': "test",
            'group_id': "  ",
        }
        res = self.app.post('/api/group/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????group_id????????????
        data = {
            'content': "test",
            'group_id': "abc",
        }
        res = self.app.post('/api/group/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # ????????????????????????content??????
        data = {
            'content': "  ",
            'group_id': "2",
        }
        res = self.app.post('/api/group/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)


if __name__ == '__main__':
    unittest.main()