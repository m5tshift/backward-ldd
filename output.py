from fpdf import FPDF
import os


def print_to_terminal(data):
    print("Report on dynamic used libraries by ELF executables")

    sorted_arch_data = dict(sorted(data.items()))

    for arch, libs_data in sorted_arch_data.items():
        if not any(libs_data.values()):
            continue

        print(f"\n---------- {arch} ----------")

        sorted_libs = dict(
            sorted(libs_data.items(), key=lambda x: len(x[1]), reverse=True)
        )

        for lib, executables in sorted_libs.items():
            if not executables:
                continue

            unique_executables = sorted(list(set(executables)))
            count = len(unique_executables)

            print(f"{lib} ({count} execs)")

            for exe in unique_executables:
                print(f"    -> {exe}")


def generate_txt_report(data, output_path):
    sorted_arch_data = dict(sorted(data.items()))

    with open(output_path, "w") as f:
        f.write("Report on dynamic used libraries by ELF executables\n\n")

        for arch, libs_data in sorted_arch_data.items():
            if not any(libs_data.values()):
                continue

            f.write(f"\n---------- {arch} ----------\n")

            sorted_libs = dict(
                sorted(libs_data.items(), key=lambda x: len(x[1]), reverse=True)
            )

            for lib, executables in sorted_libs.items():
                if not executables:
                    continue

                unique_executables = sorted(list(set(executables)))
                count = len(unique_executables)

                f.write(f"{lib} ({count} execs)\n")

                for exe in unique_executables:
                    f.write(f"    -> {exe}\n")

    print(f"[*] Отчет успешно сохранен в txt файл: {os.path.abspath(output_path)}")


def generate_pdf_report(data, output_path):
    sorted_arch_data = sorted(data.items())

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(
        0,
        10,
        txt="Report on dynamic used libraries by ELF executables",
        ln=True,
        align="C",
    )

    INDENT_WIDTH = 5

    for arch, libs_data in sorted_arch_data:
        if not any(libs_data.values()):
            continue

        pdf.set_fill_color(255, 255, 255)
        pdf.set_font("Arial", "B", 12)
        pdf.ln(5)
        pdf.cell(0, 10, txt=f"---------- {arch} ----------", ln=True, fill=True)

        pdf.set_font("Arial", "", 8)

        sorted_libs = sorted(libs_data.items(), key=lambda x: len(x[1]), reverse=True)

        for lib, executables in sorted_libs:
            if not executables:
                continue

            unique_executables = sorted(list(set(executables)))

            pdf.cell(0, 5, txt=f"{lib}({len(unique_executables)} execs)", ln=True)

            for exe in unique_executables:
                pdf.set_x(15 + INDENT_WIDTH)
                pdf.multi_cell(
                    w=0,  # w=0: использовать всю доступную ширину до правого края
                    h=4,  # h=4: высота строки
                    txt=f"-> {exe}",
                    border=0,  # border=0: без рамки
                    ln=1,  # ln=1: перевод курсора на новую строку после завершения ячейки
                )

    pdf.output(output_path)
    print(f"[*] Отчет сохранен в pdf файл: {os.path.abspath(output_path)}")


def get_output(data, output_path):
    if output_path is None:
        print_to_terminal(data)
    elif output_path.endswith(".txt"):
        generate_txt_report(data, output_path)
    elif output_path.endswith(".pdf"):
        generate_pdf_report(data, output_path)
    else:
        raise ValueError("Неподдерживаемый формат. Используйте .txt или .pdf")
