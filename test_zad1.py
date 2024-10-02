import time
import unittest
import tkinter as tk
from unittest.mock import patch
import io
import os
import shutil
from zad1 import UnixConsoleApp
class TestUnixConsoleApp(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = UnixConsoleApp(self.root,"/papka/shape")


    def tearDown(self):
        # Закрываем корневое окно после тестов
        self.root.destroy()


    def test_ls_command_no_arguments(self):
        # Выполняем команду `ls` в текущей директории
        self.app.process_command("ls")

        self.assertIn("pack", self.app.res)



    def test_ls_command_with_directory(self):
        # Выполняем команду `ls` в текущей директории
        self.app.process_command("ls pack")

        # Проверяем, что в выводе присутствует содержимое директории

        self.assertIn('ewf.py file.txt file2.txt file4.txt file5.txt pack2 ', self.app.res)


    def test_cd_command_no_arguments(self):
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

            self.assertIn("No such directory", self.app.res)

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
            self.app.process_command('tac pack/file5.txt')
            output = mock_stdout.getvalue().strip()
            self.assertIn('\n1) tut cho-to napisano\n2) tut tozhe\n',  self.app.res)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_tac_command_invalid_file(self, mock_stdout):
        """Тестируем команду 'tac' с недопустимым файлом"""
        with patch('os.path.exists', return_value=False):
            self.app.process_command('tac non_existing_file.txt')

            self.assertIn("No such file", self.app.res)

if __name__ == '__main__':
    unittest.main()
