"""
Project Manager Utility using pathlib

Демонстрирует практическое использование pathlib для:
- Сканирования структуры проекта
- Поиска файлов по паттернам
- Анализа структуры директорий
- Выполнения операций с файлами
"""

from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
import json
from datetime import datetime


class ProjectManager:
    """Утилита для управления структурой проекта."""

    # Типы файлов для классификации
    FILE_TYPES = {
        'python': ['.py'],
        'javascript': ['.js', '.ts', '.jsx', '.tsx'],
        'web': ['.html', '.css', '.scss', '.less'],
        'config': ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg'],
        'markdown': ['.md', '.rst', '.txt'],
        'data': ['.csv', '.json', '.xml', '.sql'],
        'image': ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico'],
        'archive': ['.zip', '.tar', '.gz', '.rar', '.7z'],
    }

    def __init__(self, project_path: str = '.'):
        """Инициализация менеджера проекта."""
        self.project_path = Path(project_path).resolve()
        if not self.project_path.exists():
            raise ValueError(f"Путь {project_path} не существует")

    def scan_project(self, max_depth: int = 20) -> Dict:
        """
        Сканирует проект и возвращает статистику.

        Args:
            max_depth: Максимальная глубина рекурсии

        Returns:
            Словарь со статистикой проекта
        """
        stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'by_type': defaultdict(int),
            'by_extension': defaultdict(int),
            'max_depth': 0,
            'empty_dirs': [],
            'large_files': [],
        }

        for path in self.project_path.rglob('*'):
            # Пропускаем скрытые файлы
            if any(part.startswith('.') for part in path.relative_to(self.project_path).parts):
                continue

            # Проверяем глубину
            depth = len(path.relative_to(self.project_path).parts)
            if depth > max_depth:
                continue

            stats['max_depth'] = max(stats['max_depth'], depth)

            if path.is_file():
                stats['total_files'] += 1
                size = path.stat().st_size
                stats['total_size'] += size

                # Классифицируем по расширению
                suffix = path.suffix.lower()
                stats['by_extension'][suffix] += 1

                # Классифицируем по типу
                file_type = self._get_file_type(suffix)
                stats['by_type'][file_type] += 1

                # Ищем большие файлы (> 1 MB)
                if size > 1024 * 1024:
                    stats['large_files'].append({
                        'path': str(path.relative_to(self.project_path)),
                        'size': size,
                    })

            elif path.is_dir():
                stats['total_dirs'] += 1

                # Ищем пустые директории
                if not any(path.iterdir()):
                    stats['empty_dirs'].append(str(path.relative_to(self.project_path)))

        # Конвертируем defaultdict в обычный dict
        stats['by_type'] = dict(stats['by_type'])
        stats['by_extension'] = dict(stats['by_extension'])

        return stats

    def find_files(self, pattern: str = '*', file_type: str = None) -> List[Path]:
        """
        Находит файлы по паттерну или типу.

        Args:
            pattern: Паттерн поиска (например, '*.py')
            file_type: Тип файла (например, 'python')

        Returns:
            Список найденных файлов
        """
        if file_type:
            # Поиск по типу файла
            extensions = self.FILE_TYPES.get(file_type, [])
            files = []
            for ext in extensions:
                files.extend(self.project_path.rglob(f'*{ext}'))
            return sorted(set(files))
        else:
            # Поиск по паттерну
            return sorted(self.project_path.rglob(pattern))

    def get_project_tree(self, max_depth: int = 3, prefix: str = '') -> str:
        """
        Генерирует текстовое представление структуры проекта.

        Args:
            max_depth: Максимальная глубина отображения
            prefix: Префикс для отступа

        Returns:
            Строка с деревом проекта
        """
        lines = []

        def _tree(path: Path, depth: int = 0, prefix: str = ''):
            if depth > max_depth:
                return

            # Пропускаем скрытые файлы
            if path.name.startswith('.'):
                return

            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))

            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = '└── ' if is_last else '├── '
                next_prefix = '    ' if is_last else '│   '

                if item.is_dir():
                    lines.append(f"{prefix}{current_prefix}{item.name}/")
                    _tree(item, depth + 1, prefix + next_prefix)
                else:
                    size = item.stat().st_size
                    size_str = self._format_size(size)
                    lines.append(f"{prefix}{current_prefix}{item.name} ({size_str})")

        lines.append(f"{self.project_path.name}/")
        _tree(self.project_path)
        return '\n'.join(lines)

    def copy_files(self, pattern: str, dest_dir: str, create_dirs: bool = True) -> int:
        """
        Копирует файлы, соответствующие паттерну, в целевую директорию.

        Args:
            pattern: Паттерн поиска
            dest_dir: Целевая директория
            create_dirs: Создавать ли целевую директорию

        Returns:
            Количество скопированных файлов
        """
        dest_path = Path(dest_dir)

        if create_dirs:
            dest_path.mkdir(parents=True, exist_ok=True)

        files = self.find_files(pattern)
        count = 0

        for file in files:
            dest_file = dest_path / file.name
            dest_file.write_bytes(file.read_bytes())
            count += 1

        return count

    def delete_files(self, pattern: str, confirm: bool = True) -> int:
        """
        Удаляет файлы, соответствующие паттерну.

        Args:
            pattern: Паттерн поиска
            confirm: Требовать ли подтверждение

        Returns:
            Количество удаленных файлов
        """
        files = self.find_files(pattern)

        if not files:
            return 0

        if confirm:
            print(f"Найдено {len(files)} файлов для удаления:")
            for f in files[:5]:
                print(f"  - {f.relative_to(self.project_path)}")
            if len(files) > 5:
                print(f"  ... и еще {len(files) - 5}")

            response = input("Продолжить? (y/n): ")
            if response.lower() != 'y':
                return 0

        count = 0
        for file in files:
            file.unlink()
            count += 1

        return count

    def generate_report(self, output_file: str = None) -> str:
        """
        Генерирует отчет о проекте.

        Args:
            output_file: Файл для сохранения отчета (опционально)

        Returns:
            Текст отчета
        """
        stats = self.scan_project()

        report = []
        report.append("=" * 60)
        report.append(f"PROJECT REPORT: {self.project_path.name}")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Path: {self.project_path}")
        report.append("")

        report.append("STATISTICS:")
        report.append(f"  Total files: {stats['total_files']}")
        report.append(f"  Total directories: {stats['total_dirs']}")
        report.append(f"  Total size: {self._format_size(stats['total_size'])}")
        report.append(f"  Max depth: {stats['max_depth']}")
        report.append("")

        report.append("FILES BY TYPE:")
        for file_type, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True):
            report.append(f"  {file_type}: {count}")
        report.append("")

        if stats['large_files']:
            report.append("LARGE FILES (> 1 MB):")
            for file_info in sorted(stats['large_files'], key=lambda x: x['size'], reverse=True):
                report.append(f"  {file_info['path']}: {self._format_size(file_info['size'])}")
            report.append("")

        if stats['empty_dirs']:
            report.append("EMPTY DIRECTORIES:")
            for dir_path in stats['empty_dirs'][:10]:
                report.append(f"  {dir_path}")
            if len(stats['empty_dirs']) > 10:
                report.append(f"  ... и еще {len(stats['empty_dirs']) - 10}")
            report.append("")

        report_text = '\n'.join(report)

        if output_file:
            Path(output_file).write_text(report_text)

        return report_text

    def export_to_json(self, output_file: str) -> None:
        """Экспортирует статистику в JSON."""
        stats = self.scan_project()
        stats['by_type'] = dict(stats['by_type'])
        stats['by_extension'] = dict(stats['by_extension'])

        Path(output_file).write_text(json.dumps(stats, indent=2))

    @staticmethod
    def _get_file_type(suffix: str) -> str:
        """Определяет тип файла по расширению."""
        suffix = suffix.lower()
        for file_type, extensions in ProjectManager.FILE_TYPES.items():
            if suffix in extensions:
                return file_type
        return 'other'

    @staticmethod
    def _format_size(size: int) -> str:
        """Форматирует размер файла в читаемый вид."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"


def main():
    """Пример использования ProjectManager."""
    # Создаем менеджер для текущей директории
    manager = ProjectManager('.')

    # Выводим статистику
    print(manager.generate_report())

    # Выводим структуру проекта
    print("\nPROJECT STRUCTURE:")
    print(manager.get_project_tree(max_depth=2))

    # Находим все Python файлы
    print("\nPYTHON FILES:")
    py_files = manager.find_files(file_type='python')
    for py_file in py_files[:5]:
        print(f"  - {py_file.relative_to(manager.project_path)}")
    if len(py_files) > 5:
        print(f"  ... и еще {len(py_files) - 5}")


if __name__ == '__main__':
    main()
