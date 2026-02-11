# pathlib Deep Dive — Полный разбор библиотеки

Полный анализ библиотеки `pathlib` Python с теоретическим разбором, практическими примерами и реальной утилитой.

## Структура проекта

```
pathlib_deep_dive/
├── docs/
│   ├── overview.md          # Инженерное описание инструмента
│   ├── task.md              # Техническое задание на практику
│   ├── conclusions.md       # Выводы и рефлексия
│   └── sources.md           # Использованные источники
├── project_manager.py       # Практическая реализация утилиты
├── examples.py              # 10 примеров использования pathlib
├── test_project_manager.py  # Тесты для утилиты
└── README.md                # Этот файл
```

## Что такое pathlib?

`pathlib` — встроенная библиотека Python для объектно-ориентированной работы с путями файловой системы. Вместо строк и функций модуля `os.path`, `pathlib` предлагает классы `Path`, которые инкапсулируют логику работы с путями.

### Почему pathlib лучше os.path?

| Операция | os.path | pathlib |
|----------|---------|---------|
| Создание пути | `os.path.join('a', 'b')` | `Path('a') / 'b'` |
| Существование | `os.path.exists(p)` | `p.exists()` |
| Это файл? | `os.path.isfile(p)` | `p.is_file()` |
| Это папка? | `os.path.isdir(p)` | `p.is_dir()` |
| Имя файла | `os.path.basename(p)` | `p.name` |
| Расширение | `os.path.splitext(p)[1]` | `p.suffix` |
| Чтение файла | `open(p).read()` | `p.read_text()` |
| Поиск файлов | `os.walk()` | `p.rglob()` |

## Быстрый старт

### Запуск примеров

```bash
python examples.py
```

Выведет 10 практических примеров использования pathlib.

### Запуск утилиты

```bash
python project_manager.py
```

Выведет отчет о текущем проекте, структуру и список файлов.

### Запуск тестов

```bash
python -m unittest test_project_manager.py -v
```

## Основные операции

### Создание путей

```python
from pathlib import Path

Path('file.txt')                    # Относительный путь
Path('/home/user/file.txt')         # Абсолютный путь
Path.cwd()                          # Текущая директория
Path.home()                         # Домашняя директория
Path('data') / 'file.txt'           # Композиция путей
```

### Компоненты пути

```python
p = Path('/home/user/documents/report.pdf')

p.name          # 'report.pdf'
p.stem          # 'report'
p.suffix        # '.pdf'
p.parent        # Path('/home/user/documents')
p.parts         # ('/', 'home', 'user', 'documents', 'report.pdf')
```

### Проверка типов

```python
p = Path('something')

p.exists()      # Существует ли
p.is_file()     # Это файл?
p.is_dir()      # Это директория?
p.is_symlink()  # Это символическая ссылка?
```

### Работа с файлами

```python
p = Path('file.txt')

# Чтение
content = p.read_text()
data = p.read_bytes()

# Запись
p.write_text('Hello')
p.write_bytes(b'data')

# Операции
p.touch()                           # Создать пустой файл
p.unlink()                          # Удалить файл
p.rename('new.txt')                 # Переименовать
p.stat().st_size                    # Размер в байтах
```

### Работа с директориями

```python
p = Path('folder')

# Создание
p.mkdir(parents=True, exist_ok=True)

# Содержимое
list(p.iterdir())                   # Все файлы и папки
list(p.glob('*.txt'))               # Файлы по паттерну
list(p.rglob('*.txt'))              # Рекурсивный поиск

# Удаление
p.rmdir()                           # Удалить пустую директорию
```

## Практическая утилита

### ProjectManager

Класс для управления структурой проекта:

```python
from project_manager import ProjectManager

manager = ProjectManager('.')

# Сканирование проекта
stats = manager.scan_project()
print(f"Файлов: {stats['total_files']}")
print(f"Директорий: {stats['total_dirs']}")

# Поиск файлов
py_files = manager.find_files(file_type='python')
config_files = manager.find_files(pattern='*.json')

# Операции
manager.copy_files('*.py', 'backup/')
manager.delete_files('*.tmp', confirm=False)

# Отчеты
print(manager.generate_report())
print(manager.get_project_tree(max_depth=3))
manager.export_to_json('stats.json')
```

**Возможности:**
- Сканирование и анализ структуры проекта
- Классификация файлов по типам
- Поиск больших файлов и пустых директорий
- Копирование и удаление файлов
- Генерация отчетов и экспорт в JSON

## 10 примеров использования

1. **Создание и навигация** — создание путей, текущая/домашняя директория
2. **Компоненты пути** — name, stem, suffix, parent, parts
3. **Композиция путей** — оператор `/`, with_suffix(), with_name()
4. **Проверка типов** — is_file(), is_dir(), exists()
5. **Работа с файлами** — read_text(), write_text(), stat()
6. **Работа с директориями** — mkdir(), iterdir(), touch()
7. **Поиск файлов** — glob(), rglob()
8. **Фильтрация** — по расширению, размеру, сортировка
9. **Копирование и перемещение** — shutil.copy(), rename()
10. **Манипуляция именами** — изменение расширения и имени

Запустите `python examples.py` для просмотра всех примеров.

## Best Practices

1. **Используйте pathlib вместо os.path** — более читаемо и безопасно
2. **Используйте `/` для композиции путей** — вместо os.path.join()
3. **Используйте resolve() для абсолютных путей** — для надежности
4. **Проверяйте типы перед операциями** — is_file(), is_dir()
5. **Используйте glob() и rglob()** — для поиска файлов
6. **Используйте read_text() и write_text()** — для простых операций
7. **Используйте stat() для информации** — вместо нескольких вызовов
8. **Используйте exist_ok для mkdir()** — для идемпотентности
9. **Обрабатывайте исключения правильно** — FileNotFoundError, IsADirectoryError
10. **Используйте type hints с Path** — для лучшей типизации

## Часто задаваемые вопросы

**Q: Когда pathlib был добавлен?**  
A: В Python 3.4 (2014 год) как часть стандартной библиотеки.

**Q: Нужно ли переписывать старый код?**  
A: Не обязательно, но рекомендуется для новых проектов.

**Q: Какая разница между Path и PurePath?**  
A: Path работает с файловой системой, PurePath только парсит пути.

**Q: Медленно ли pathlib?**  
A: Нет, примерно такая же производительность как os.path.

**Q: Работает ли на Windows?**  
A: Да, полностью поддерживает Windows с правильными разделителями.

**Q: Как работать с большими директориями?**  
A: Используйте iterdir() вместо glob() для лучшей производительности.

**Q: Как обработать ошибки?**  
A: Перехватывайте FileNotFoundError, IsADirectoryError, PermissionError.

**Q: Как использовать с type hints?**  
A: `def process(path: Path) -> str: return path.read_text()`

**Q: Как работать с символическими ссылками?**  
A: Используйте is_symlink() для проверки, resolve() для получения реального пути.

**Q: Как найти самый большой файл?**  
A: `max(p.rglob('*'), key=lambda f: f.stat().st_size if f.is_file() else 0)`

## Документация

- **docs/overview.md** — полное инженерное описание (модули 1-3)
- **docs/task.md** — техническое задание на практику
- **docs/conclusions.md** — выводы и рефлексия
- **docs/sources.md** — использованные источники

## Требования

- Python 3.4+ (pathlib встроена в стандартную библиотеку)
- Рекомендуется Python 3.6+ для f-strings

## Использование в своем коде

```python
from project_manager import ProjectManager

# Инициализация
manager = ProjectManager('/path/to/project')

# Сканирование
stats = manager.scan_project()

# Поиск файлов
python_files = manager.find_files(file_type='python')

# Генерация отчета
report = manager.generate_report()
print(report)
```

## Автор

Сысоев Тимофей, Затонский Егор Олегович

## Ссылки

- [Официальная документация pathlib](https://docs.python.org/3/library/pathlib.html)
- [PEP 428 — The pathlib module](https://www.python.org/dev/peps/pep-0428/)
- [Real Python: Python pathlib](https://realpython.com/python-pathlib/)
