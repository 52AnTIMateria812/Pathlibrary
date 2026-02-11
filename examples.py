"""
Примеры использования pathlib

Демонстрирует различные способы работы с путями и файлами.
"""

from pathlib import Path
from typing import List
import shutil


# ============================================================================
# 1. СОЗДАНИЕ И НАВИГАЦИЯ ПО ПУТЯМ
# ============================================================================

def example_path_creation():
    """Примеры создания путей."""
    print("=" * 60)
    print("1. СОЗДАНИЕ И НАВИГАЦИЯ ПО ПУТЯМ")
    print("=" * 60)

    # Абсолютный путь
    abs_path = Path('/home/user/documents')
    print(f"Абсолютный путь: {abs_path}")

    # Относительный путь
    rel_path = Path('data/files')
    print(f"Относительный путь: {rel_path}")

    # Текущая директория
    cwd = Path.cwd()
    print(f"Текущая директория: {cwd}")

    # Домашняя директория
    home = Path.home()
    print(f"Домашняя директория: {home}")

    # Абсолютный путь из относительного
    abs_rel = rel_path.resolve()
    print(f"Абсолютный путь из относительного: {abs_rel}")

    print()


# ============================================================================
# 2. КОМПОНЕНТЫ ПУТИ
# ============================================================================

def example_path_components():
    """Примеры работы с компонентами пути."""
    print("=" * 60)
    print("2. КОМПОНЕНТЫ ПУТИ")
    print("=" * 60)

    p = Path('/home/user/documents/report_2024.pdf')

    print(f"Полный путь: {p}")
    print(f"Имя файла (name): {p.name}")
    print(f"Имя без расширения (stem): {p.stem}")
    print(f"Расширение (suffix): {p.suffix}")
    print(f"Родительская директория (parent): {p.parent}")
    print(f"Все компоненты (parts): {p.parts}")
    print(f"Корень (root): {p.root}")
    print(f"Диск (drive): {p.drive}")

    print()


# ============================================================================
# 3. КОМПОЗИЦИЯ ПУТЕЙ
# ============================================================================

def example_path_composition():
    """Примеры композиции путей с оператором /."""
    print("=" * 60)
    print("3. КОМПОЗИЦИЯ ПУТЕЙ")
    print("=" * 60)

    base = Path('data')
    subfolder = 'reports'
    filename = 'report.txt'

    # Композиция с оператором /
    full_path = base / subfolder / filename
    print(f"Композиция путей: {full_path}")

    # Добавление к пути
    new_path = full_path.parent / 'backup' / full_path.name
    print(f"Новый путь: {new_path}")

    # Замена расширения
    backup_path = full_path.with_suffix('.bak')
    print(f"С новым расширением: {backup_path}")

    # Замена имени
    renamed = full_path.with_name('report_v2.txt')
    print(f"С новым именем: {renamed}")

    print()


# ============================================================================
# 4. ПРОВЕРКА ТИПОВ И СУЩЕСТВОВАНИЯ
# ============================================================================

def example_path_checks():
    """Примеры проверки типов и существования."""
    print("=" * 60)
    print("4. ПРОВЕРКА ТИПОВ И СУЩЕСТВОВАНИЯ")
    print("=" * 60)

    # Создаем тестовые файлы
    test_dir = Path('test_pathlib')
    test_dir.mkdir(exist_ok=True)

    test_file = test_dir / 'test.txt'
    test_file.write_text('Hello, pathlib!')

    print(f"Существует: {test_file.exists()}")
    print(f"Это файл: {test_file.is_file()}")
    print(f"Это директория: {test_file.is_dir()}")
    print(f"Это символическая ссылка: {test_file.is_symlink()}")
    print(f"Абсолютный путь: {test_file.is_absolute()}")

    # Очищаем
    test_file.unlink()
    test_dir.rmdir()

    print()


# ============================================================================
# 5. РАБОТА С ФАЙЛАМИ
# ============================================================================

def example_file_operations():
    """Примеры работы с файлами."""
    print("=" * 60)
    print("5. РАБОТА С ФАЙЛАМИ")
    print("=" * 60)

    test_dir = Path('test_pathlib')
    test_dir.mkdir(exist_ok=True)

    # Создание файла
    file_path = test_dir / 'example.txt'
    file_path.write_text('Hello, World!\nLine 2\nLine 3')
    print(f"Файл создан: {file_path}")

    # Чтение файла
    content = file_path.read_text()
    print(f"Содержимое:\n{content}")

    # Работа с байтами
    bytes_content = file_path.read_bytes()
    print(f"Размер в байтах: {len(bytes_content)}")

    # Информация о файле
    stat = file_path.stat()
    print(f"Размер: {stat.st_size} байт")
    print(f"Время изменения: {stat.st_mtime}")

    # Переименование
    new_name = test_dir / 'renamed.txt'
    file_path.rename(new_name)
    print(f"Переименовано в: {new_name}")

    # Очищаем
    new_name.unlink()
    test_dir.rmdir()

    print()


# ============================================================================
# 6. РАБОТА С ДИРЕКТОРИЯМИ
# ============================================================================

def example_directory_operations():
    """Примеры работы с директориями."""
    print("=" * 60)
    print("6. РАБОТА С ДИРЕКТОРИЯМИ")
    print("=" * 60)

    # Создание директории
    test_dir = Path('test_pathlib/subdir/deep')
    test_dir.mkdir(parents=True, exist_ok=True)
    print(f"Директория создана: {test_dir}")

    # Создание файлов
    (test_dir / 'file1.txt').touch()
    (test_dir / 'file2.txt').touch()
    (test_dir.parent / 'file3.txt').touch()

    # Список файлов в директории
    print(f"\nФайлы в {test_dir}:")
    for item in test_dir.iterdir():
        print(f"  - {item.name}")

    # Список файлов в родительской директории
    print(f"\nФайлы в {test_dir.parent}:")
    for item in test_dir.parent.iterdir():
        print(f"  - {item.name}")

    # Очищаем
    for item in test_dir.iterdir():
        item.unlink()
    test_dir.rmdir()
    for item in test_dir.parent.iterdir():
        item.unlink()
    test_dir.parent.rmdir()
    test_dir.parent.parent.rmdir()

    print()


# ============================================================================
# 7. ПОИСК ФАЙЛОВ С GLOB
# ============================================================================

def example_glob_search():
    """Примеры поиска файлов с glob."""
    print("=" * 60)
    print("7. ПОИСК ФАЙЛОВ С GLOB")
    print("=" * 60)

    # Создаем тестовую структуру
    test_dir = Path('test_pathlib')
    test_dir.mkdir(exist_ok=True)

    (test_dir / 'file1.txt').touch()
    (test_dir / 'file2.txt').touch()
    (test_dir / 'script.py').touch()
    (test_dir / 'data.json').touch()

    subdir = test_dir / 'subdir'
    subdir.mkdir(exist_ok=True)
    (subdir / 'nested.txt').touch()
    (subdir / 'nested.py').touch()

    # Поиск всех .txt файлов (не рекурсивно)
    print("Все .txt файлы (не рекурсивно):")
    for f in test_dir.glob('*.txt'):
        print(f"  - {f.relative_to(test_dir)}")

    # Поиск всех .txt файлов (рекурсивно)
    print("\nВсе .txt файлы (рекурсивно):")
    for f in test_dir.rglob('*.txt'):
        print(f"  - {f.relative_to(test_dir)}")

    # Поиск по паттерну
    print("\nВсе файлы, начинающиеся с 'file':")
    for f in test_dir.glob('file*'):
        print(f"  - {f.relative_to(test_dir)}")

    # Очищаем
    for item in subdir.iterdir():
        item.unlink()
    subdir.rmdir()
    for item in test_dir.iterdir():
        item.unlink()
    test_dir.rmdir()

    print()


# ============================================================================
# 8. ФИЛЬТРАЦИЯ И ОБРАБОТКА ФАЙЛОВ
# ============================================================================

def example_filtering():
    """Примеры фильтрации и обработки файлов."""
    print("=" * 60)
    print("8. ФИЛЬТРАЦИЯ И ОБРАБОТКА ФАЙЛОВ")
    print("=" * 60)

    # Создаем тестовую структуру
    test_dir = Path('test_pathlib')
    test_dir.mkdir(exist_ok=True)

    files = ['file1.txt', 'file2.txt', 'script.py', 'data.json', 'readme.md']
    for f in files:
        (test_dir / f).write_text(f'Content of {f}')

    # Фильтрация по расширению
    print("Python файлы:")
    py_files = [f for f in test_dir.iterdir() if f.suffix == '.py']
    for f in py_files:
        print(f"  - {f.name}")

    # Фильтрация по размеру
    print("\nФайлы больше 10 байт:")
    large_files = [f for f in test_dir.iterdir() if f.is_file() and f.stat().st_size > 10]
    for f in large_files:
        print(f"  - {f.name} ({f.stat().st_size} байт)")

    # Сортировка по размеру
    print("\nФайлы, отсортированные по размеру:")
    sorted_files = sorted(test_dir.iterdir(), key=lambda f: f.stat().st_size if f.is_file() else 0)
    for f in sorted_files:
        if f.is_file():
            print(f"  - {f.name} ({f.stat().st_size} байт)")

    # Очищаем
    for item in test_dir.iterdir():
        item.unlink()
    test_dir.rmdir()

    print()


# ============================================================================
# 9. КОПИРОВАНИЕ И ПЕРЕМЕЩЕНИЕ
# ============================================================================

def example_copy_move():
    """Примеры копирования и перемещения файлов."""
    print("=" * 60)
    print("9. КОПИРОВАНИЕ И ПЕРЕМЕЩЕНИЕ")
    print("=" * 60)

    # Создаем тестовую структуру
    test_dir = Path('test_pathlib')
    test_dir.mkdir(exist_ok=True)

    source = test_dir / 'source.txt'
    source.write_text('Original content')

    # Копирование файла
    dest = test_dir / 'copy.txt'
    shutil.copy(source, dest)
    print(f"Файл скопирован: {source} -> {dest}")

    # Перемещение файла
    moved = test_dir / 'moved.txt'
    source.rename(moved)
    print(f"Файл перемещен: {source} -> {moved}")

    # Копирование директории
    src_dir = test_dir / 'src'
    src_dir.mkdir(exist_ok=True)
    (src_dir / 'file.txt').write_text('Content')

    dst_dir = test_dir / 'dst'
    shutil.copytree(src_dir, dst_dir)
    print(f"Директория скопирована: {src_dir} -> {dst_dir}")

    # Очищаем
    for item in test_dir.rglob('*'):
        if item.is_file():
            item.unlink()
    for item in test_dir.iterdir():
        if item.is_dir():
            item.rmdir()
    test_dir.rmdir()

    print()


# ============================================================================
# 10. РАБОТА С РАСШИРЕНИЯМИ И ИМЕНАМИ
# ============================================================================

def example_name_manipulation():
    """Примеры работы с именами и расширениями."""
    print("=" * 60)
    print("10. РАБОТА С РАСШИРЕНИЯМИ И ИМЕНАМИ")
    print("=" * 60)

    p = Path('documents/report_2024.pdf')

    print(f"Исходный путь: {p}")
    print(f"Имя файла: {p.name}")
    print(f"Имя без расширения: {p.stem}")
    print(f"Расширение: {p.suffix}")

    # Замена расширения
    new_ext = p.with_suffix('.docx')
    print(f"С новым расширением: {new_ext}")

    # Замена имени
    new_name = p.with_name('summary.pdf')
    print(f"С новым именем: {new_name}")

    # Добавление суффикса к имени
    backup = p.with_stem(p.stem + '_backup')
    print(f"С суффиксом: {backup}")

    print()


def main():
    """Запуск всех примеров."""
    example_path_creation()
    example_path_components()
    example_path_composition()
    example_path_checks()
    example_file_operations()
    example_directory_operations()
    example_glob_search()
    example_filtering()
    example_copy_move()
    example_name_manipulation()

    print("=" * 60)
    print("Все примеры выполнены!")
    print("=" * 60)


if __name__ == '__main__':
    main()
