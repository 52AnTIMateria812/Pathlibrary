"""
Тесты для ProjectManager

Демонстрирует использование pathlib в тестировании.
"""

import unittest
from pathlib import Path
import tempfile
import shutil
from project_manager import ProjectManager


class TestProjectManager(unittest.TestCase):
    """Тесты для класса ProjectManager."""

    def setUp(self):
        """Подготовка к тестам."""
        # Создаем временную директорию
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)

        # Создаем тестовую структуру
        self._create_test_structure()

    def tearDown(self):
        """Очистка после тестов."""
        shutil.rmtree(self.test_dir)

    def _create_test_structure(self):
        """Создает тестовую структуру проекта."""
        # Python файлы
        (self.test_path / 'main.py').write_text('print("Hello")')
        (self.test_path / 'utils.py').write_text('def helper(): pass')

        # Конфиги
        (self.test_path / 'config.json').write_text('{}')
        (self.test_path / 'settings.yaml').write_text('key: value')

        # Документация
        (self.test_path / 'README.md').write_text('# Project')

        # Поддиректория
        subdir = self.test_path / 'src'
        subdir.mkdir()
        (subdir / 'module.py').write_text('class Module: pass')
        (subdir / 'data.json').write_text('[]')

        # Пустая директория
        (self.test_path / 'empty').mkdir()

        # Большой файл (> 1 MB)
        large_file = self.test_path / 'large.bin'
        large_file.write_bytes(b'x' * (2 * 1024 * 1024))

    def test_initialization(self):
        """Тест инициализации ProjectManager."""
        manager = ProjectManager(self.test_dir)
        self.assertEqual(manager.project_path, self.test_path)

    def test_initialization_invalid_path(self):
        """Тест инициализации с невалидным путем."""
        with self.assertRaises(ValueError):
            ProjectManager('/nonexistent/path')

    def test_scan_project(self):
        """Тест сканирования проекта."""
        manager = ProjectManager(self.test_dir)
        stats = manager.scan_project()

        # Проверяем основные метрики
        self.assertGreater(stats['total_files'], 0)
        self.assertGreater(stats['total_dirs'], 0)
        self.assertGreater(stats['total_size'], 0)

        # Проверяем классификацию
        self.assertIn('python', stats['by_type'])
        self.assertIn('config', stats['by_type'])
        self.assertIn('markdown', stats['by_type'])

    def test_find_files_by_pattern(self):
        """Тест поиска файлов по паттерну."""
        manager = ProjectManager(self.test_dir)

        # Поиск Python файлов
        py_files = manager.find_files('*.py')
        self.assertGreater(len(py_files), 0)
        self.assertTrue(all(f.suffix == '.py' for f in py_files))

    def test_find_files_by_type(self):
        """Тест поиска файлов по типу."""
        manager = ProjectManager(self.test_dir)

        # Поиск Python файлов по типу
        py_files = manager.find_files(file_type='python')
        self.assertGreater(len(py_files), 0)
        self.assertTrue(all(f.suffix == '.py' for f in py_files))

        # Поиск конфигов
        config_files = manager.find_files(file_type='config')
        self.assertGreater(len(config_files), 0)

    def test_get_project_tree(self):
        """Тест генерации дерева проекта."""
        manager = ProjectManager(self.test_dir)
        tree = manager.get_project_tree(max_depth=2)

        # Проверяем, что дерево содержит файлы
        self.assertIn('main.py', tree)
        self.assertIn('config.json', tree)
        self.assertIn('README.md', tree)

    def test_copy_files(self):
        """Тест копирования файлов."""
        manager = ProjectManager(self.test_dir)

        # Копируем Python файлы
        dest_dir = self.test_path / 'backup'
        count = manager.copy_files('*.py', str(dest_dir))

        self.assertGreater(count, 0)
        self.assertTrue(dest_dir.exists())
        self.assertTrue((dest_dir / 'main.py').exists())

    def test_delete_files(self):
        """Тест удаления файлов."""
        manager = ProjectManager(self.test_dir)

        # Создаем временные файлы
        (self.test_path / 'temp1.tmp').touch()
        (self.test_path / 'temp2.tmp').touch()

        # Удаляем без подтверждения
        count = manager.delete_files('*.tmp', confirm=False)

        self.assertEqual(count, 2)
        self.assertFalse((self.test_path / 'temp1.tmp').exists())
        self.assertFalse((self.test_path / 'temp2.tmp').exists())

    def test_generate_report(self):
        """Тест генерации отчета."""
        manager = ProjectManager(self.test_dir)
        report = manager.generate_report()

        # Проверяем, что отчет содержит информацию
        self.assertIn('PROJECT REPORT', report)
        self.assertIn('STATISTICS', report)
        self.assertIn('FILES BY TYPE', report)

    def test_export_to_json(self):
        """Тест экспорта в JSON."""
        manager = ProjectManager(self.test_dir)
        output_file = self.test_path / 'stats.json'

        manager.export_to_json(str(output_file))

        self.assertTrue(output_file.exists())
        content = output_file.read_text()
        self.assertIn('total_files', content)
        self.assertIn('total_dirs', content)

    def test_empty_directories_detection(self):
        """Тест обнаружения пустых директорий."""
        manager = ProjectManager(self.test_dir)
        stats = manager.scan_project()

        # Проверяем, что пустая директория обнаружена
        self.assertGreater(len(stats['empty_dirs']), 0)
        self.assertTrue(any('empty' in d for d in stats['empty_dirs']))

    def test_large_files_detection(self):
        """Тест обнаружения больших файлов."""
        manager = ProjectManager(self.test_dir)
        stats = manager.scan_project()

        # Проверяем, что большой файл обнаружен
        self.assertGreater(len(stats['large_files']), 0)
        self.assertTrue(any('large.bin' in f['path'] for f in stats['large_files']))

    def test_file_type_classification(self):
        """Тест классификации типов файлов."""
        manager = ProjectManager(self.test_dir)

        # Проверяем классификацию
        self.assertEqual(manager._get_file_type('.py'), 'python')
        self.assertEqual(manager._get_file_type('.json'), 'config')
        self.assertEqual(manager._get_file_type('.md'), 'markdown')
        self.assertEqual(manager._get_file_type('.unknown'), 'other')

    def test_format_size(self):
        """Тест форматирования размера файла."""
        # Проверяем форматирование
        self.assertEqual(ProjectManager._format_size(512), '512.0 B')
        self.assertEqual(ProjectManager._format_size(1024), '1.0 KB')
        self.assertEqual(ProjectManager._format_size(1024 * 1024), '1.0 MB')
        self.assertEqual(ProjectManager._format_size(1024 * 1024 * 1024), '1.0 GB')


class TestPathLibIntegration(unittest.TestCase):
    """Тесты интеграции с pathlib."""

    def setUp(self):
        """Подготовка к тестам."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)

    def tearDown(self):
        """Очистка после тестов."""
        shutil.rmtree(self.test_dir)

    def test_path_composition(self):
        """Тест композиции путей."""
        base = self.test_path
        file_path = base / 'subdir' / 'file.txt'

        self.assertEqual(file_path.parent, base / 'subdir')
        self.assertEqual(file_path.name, 'file.txt')
        self.assertEqual(file_path.stem, 'file')
        self.assertEqual(file_path.suffix, '.txt')

    def test_path_operations(self):
        """Тест операций с путями."""
        file_path = self.test_path / 'test.txt'

        # Создание файла
        file_path.write_text('Hello, World!')
        self.assertTrue(file_path.exists())
        self.assertTrue(file_path.is_file())

        # Чтение файла
        content = file_path.read_text()
        self.assertEqual(content, 'Hello, World!')

        # Переименование
        new_path = self.test_path / 'renamed.txt'
        file_path.rename(new_path)
        self.assertFalse(file_path.exists())
        self.assertTrue(new_path.exists())

        # Удаление
        new_path.unlink()
        self.assertFalse(new_path.exists())

    def test_glob_operations(self):
        """Тест операций glob."""
        # Создаем файлы
        (self.test_path / 'file1.txt').touch()
        (self.test_path / 'file2.txt').touch()
        (self.test_path / 'script.py').touch()

        # Поиск .txt файлов
        txt_files = list(self.test_path.glob('*.txt'))
        self.assertEqual(len(txt_files), 2)

        # Поиск всех файлов
        all_files = list(self.test_path.glob('*'))
        self.assertEqual(len(all_files), 3)

    def test_directory_operations(self):
        """Тест операций с директориями."""
        # Создание директории
        subdir = self.test_path / 'subdir'
        subdir.mkdir()
        self.assertTrue(subdir.exists())
        self.assertTrue(subdir.is_dir())

        # Создание файла в поддиректории
        file_path = subdir / 'file.txt'
        file_path.write_text('Content')
        self.assertTrue(file_path.exists())

        # Итерация по файлам
        files = list(subdir.iterdir())
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, 'file.txt')


def run_tests():
    """Запуск всех тестов."""
    unittest.main(verbosity=2)


if __name__ == '__main__':
    run_tests()
