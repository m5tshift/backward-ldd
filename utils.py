from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError
import os

ARCH_MAP = {
    "EM_386": "x86",
    "EM_X86_64": "x86_64",
    "EM_ARM": "armv7",
    "EM_AARCH64": "aarch64",
}


def is_valid_elf(file_path):
    """Проверка корректности ELF-файла по магическим байтам"""
    try:
        if not os.path.isfile(file_path) or not os.access(file_path, os.R_OK):
            return False

        with open(file_path, "rb") as f:
            return f.read(4) == b"\x7fELF"
    except Exception:
        return False


def get_elf_architecture(file_path):
    """Определение архитектуры ELF-файла"""
    try:
        with open(file_path, "rb") as f:
            elf = ELFFile(f)
            machine_code = elf.header["e_machine"]
            return ARCH_MAP.get(machine_code, "unknown")
    except (ELFError, Exception):
        return "unknown"


def get_dynamic_dependencies(file_path):
    """
    Извлечение списка библиотек из DT_NEEDED.
    Этот блок try/except перехватывает ошибки SHT_NULL и другие структурные
    ошибки, возникающие при парсинге поврежденных или необычных ELF-файлов.
    """
    dependencies = []
    try:
        with open(file_path, "rb") as f:
            elf = ELFFile(f)

            for segment in elf.iter_segments():
                if segment.header.p_type == "PT_DYNAMIC":
                    for tag in segment.iter_tags():
                        if tag.entry.d_tag == "DT_NEEDED":
                            dependencies.append(tag.needed)
                    break
    except Exception:
        pass
    return dependencies
