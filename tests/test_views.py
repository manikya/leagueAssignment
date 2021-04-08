from tests.test_setup import TestSetup


class TestViews(TestSetup):
    def test_user_can_view_user_list(self):
        res = self.client.get(self.user_url)
        self.assertEqual(res.status_code, 200)

    def test_user_can_received_correct_data(self):
        res = self.client.get(self.user_url + '1')
        self.assertEqual(res.status_code, 301)

    def test_admin_user_can_create_user(self):
        user = {'username': 'user2',
                'password': '123',
                'email': 'user2@gmail.com'
                }
        res = self.client.post(self.user_url, user)
        self.assertEqual(res.status_code, 201)

    def test_error_for_missing_required_details(self):
        user = {'username': 'user2',
                'password': '123'
                }
        res = self.client.post(self.user_url, user)
        self.assertEqual(res.status_code, 400)
