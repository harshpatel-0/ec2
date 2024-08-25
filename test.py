import os
import unittest
import tempfile
from main import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Create a temporary directory to store uploads
        self.test_dir = tempfile.mkdtemp()
        app.config['UPLOAD_FOLDER'] = self.test_dir

    def test_main_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_image_upload(self):
        test_file = (BytesIO(b"test image content"), 'test.jpg')
        response = self.app.post('/success', data={'file': test_file}, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)  # Assuming redirection after upload

    def test_non_image_upload(self):
        test_file = (BytesIO(b"test non-image content"), 'test.txt')
        response = self.app.post('/success', data={'file': test_file}, content_type='multipart/form-data')
        self.assertNotEqual(response.status_code, 302)  # Assuming it does not redirect for non-image files

    def test_images_route(self):
        response = self.app.get('/images')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        # Remove the directory after the test
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main()
