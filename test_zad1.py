import unittest
from unittest.mock import patch
import io
import os
import shutil
from zad1 import UnixConsoleApp
class TestUnixConsoleApp(unittest.TestCase):

    def setUp(self):
        self.app = UnixConsoleApp("/papka/shape")  # Инициализация приложения

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ls_command_no_arguments(self, mock_stdout):
        """Тестируем команду 'ls' без аргументов"""
        with patch('os.listdir', return_value=['pack']):
            self.app.process_command('ls')
            output = mock_stdout.getvalue().strip()
            print(output)
            self.assertIn("pack", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ls_command_with_directory(self, mock_stdout):
        """Тестируем команду 'ls' с аргументом каталога"""
        with patch('os.listdir', return_value=['ewf.py file.txt file2.txt pack2']):
            self.app.process_command('ls pack')
            output = mock_stdout.getvalue().strip()
            self.assertIn("ewf.py file.txt file2.txt pack2", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cd_command_no_arguments(self, mock_stdout):
        """Тестируем команду 'cd' без аргументов (возврат в дефолтную директорию)"""
        self.app.curDir = "/papka/shape/pack"
        self.app.process_command('cd')
        self.assertEqual(self.app.curDir, self.app.defDir)
        self.assertEqual(self.app.prompt, "user:~#")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cd_command_invalid_directory(self, mock_stdout):
        """Тестируем команду 'cd' с недопустимым каталогом"""
        with patch('os.path.exists', return_value=False):
            self.app.process_command('cd ppp')
            output = mock_stdout.getvalue().strip()
            self.assertIn("No such directory", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('os.path.exists', return_value=True)
    def test_mv_command_move_file(self, mock_stdout, mock_exists):
        """Тестируем команду 'mv' для перемещения файла"""
        with patch('shutil.move') as mock_move:
            self.app.process_command('mv pack/file.txt pack/pack2')
            mock_move.assert_called_once_with('/papka/shape/pack/file.txt', '/papka/shape/pack/pack2')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_mv_command_rename_file(self, mock_stdout):
        """Тестируем команду 'mv' для переименования файла"""
        with patch('os.rename') as mock_rename, patch('os.path.exists', return_value=True):
            self.app.process_command('mv file2.txt file3.txt')
            mock_rename.assert_called_once_with('/papka/shape/pack/file2.txt', '/papka/shape/pack/file3.txt')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_tac_command_valid_file(self, mock_stdout):
        """Тестируем команду 'tac' с допустимым файлом"""
        with patch('builtins.open', unittest.mock.mock_open(read_data="2) tut tozhe\n1) tut cho-to napisano")):
            self.app.process_command('tac pack/file.txt')
            output = mock_stdout.getvalue().strip()
            self.assertIn("2) tut tozhe\n1) tut cho-to napisano", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_tac_command_invalid_file(self, mock_stdout):
        """Тестируем команду 'tac' с недопустимым файлом"""
        with patch('os.path.exists', return_value=False):
            self.app.process_command('tac non_existing_file.txt')
            output = mock_stdout.getvalue().strip()
            self.assertIn("No such file", output)

if __name__ == '__main__':
    unittest.main()
