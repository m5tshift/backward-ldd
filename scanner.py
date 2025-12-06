import os
from utils import is_valid_elf, get_elf_architecture, get_dynamic_dependencies


def scan_executables(scan_dir, target_libs, target_archs):
    """
    Основной сканер с фильтрацией по архитектуре.
    Возвращает структуру: {arch: {lib: [executables]}}
    """
    results = {arch: {lib: [] for lib in target_libs} for arch in target_archs}

    for root, _, files in os.walk(scan_dir, topdown=True):
        for file in files:
            path = os.path.join(root, file)

            if os.path.islink(path):
                continue

            if not os.access(path, os.X_OK) or not is_valid_elf(path):
                continue

            arch = get_elf_architecture(path)
            if arch not in target_archs:
                continue

            deps = get_dynamic_dependencies(path)

            for lib in target_libs:
                for dep in deps:
                    if lib in dep:
                        results[arch][lib].append(path)
                        break

    return results
