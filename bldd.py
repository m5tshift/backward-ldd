import argparse
import os
from scanner import scan_executables
from output import get_output

SUPPORTED_ARCHS = ["x86", "x86_64", "armv7", "aarch64"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="bldd: Находит исполняемые файлы, использующие указанные разделяемые библиотеки (обратный ldd).",
        epilog="Примеры использования:\n"
        "  1. Поиск libc.so.6 в /usr/bin:\n"
        "     python3 bldd.py libc.so.6 -d /usr/bin\n"
        "  2. Поиск нескольких библиотек с сохранением в PDF:\n"
        "     python3 bldd.py libssl.so libcrypto.so -o report.pdf\n"
        "  3. Поиск библиотек armv7 в /opt:\n"
        "     python3 bldd.py libc.so.6 -d /opt --arch armv7",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "libraries",
        nargs="+",
        help="Один или несколько файлов разделяемых библиотек для поиска (например, libc.so.6)",
    )
    parser.add_argument(
        "-d",
        "--directory",
        default="/",
        help="Корневая директория для сканирования (default: /)",
    )
    parser.add_argument(
        "-a",
        "--arch",
        nargs="+",
        choices=SUPPORTED_ARCHS,
        default=SUPPORTED_ARCHS,
        help=f"Целевые архитектуры. Поддерживаются: {', '.join(SUPPORTED_ARCHS)}.\n"
        f"По умолчанию: Все ({', '.join(SUPPORTED_ARCHS)})",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Путь к файлу отчета (поддерживаются .txt, .pdf). Если не указано, выводится в консоль.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.isdir(args.directory):
        print(f"[!] Ошибка: Директория '{args.directory}' не найдена.")
        return

    print(f"[*] Сканирование '{args.directory}' для библиотек: {args.libraries}")
    print(f"[*] Целевые архитектуры: {', '.join(args.arch)}")

    results = scan_executables(args.directory, args.libraries, args.arch)

    total_found = sum(
        len(execs) for arch_data in results.values() for execs in arch_data.values()
    )

    if total_found == 0:
        print("[!] Не найдено исполняемых файлов, соответствующих критериям.")
    else:
        get_output(results, args.output)


if __name__ == "__main__":
    main()
