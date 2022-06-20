import unittest


class Testadmin(unittest.TestCase):
    def test_admin_manager(self, client):
        response = client.post('/manager')

        assert response.status_code == 200
