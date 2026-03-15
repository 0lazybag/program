import os
import subprocess
import json
import sys

def create_project():
    # ПУТИ
    SUBLIME_PATH = r"E:\Sublime Text\sublime_text.exe"
    BASE_DIR = r"E:\program"

    # Ввод данных
    print("--- Проект создается... ---")
    lang_choice = input("1 - C++, 2 - Python: ").strip()
    project_name = input("Название проекта: ").strip()
    
    if not project_name:
        sys.exit()

    project_path = os.path.join(BASE_DIR, project_name)
    os.makedirs(project_path, exist_ok=True)

    # 1. Гит и Ридми
    with open(os.path.join(project_path, ".gitignore"), "w", encoding="utf-8") as f:
        f.write("*.exe\n*.o\n*.obj\n.sublime-workspace\n*.sublime-build\n__pycache__/\n")

    with open(os.path.join(project_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"# {project_name}\n\nАвтоматическая заготовка.")

    clean_path = project_path.replace('\\', '/')

    # 2. Настройка C++
    if lang_choice == '1':
        file_path = os.path.join(project_path, f"{project_name}.cpp")
        build_bat_path = os.path.join(project_path, "build.bat")
        
        cpp_template = (
            "#include <iostream>\n#include <windows.h>\n\n"
            "int main() {\n"
            "    SetConsoleCP(65001);\n"
            "    SetConsoleOutputCP(65001);\n\n"
            f"    std::cout << \"Проект {project_name} готов!\" << std::endl;\n\n"
            "    std::cout << \"Нажмите Enter...\" << std::endl;\n"
            "    std::cin.get();\n    return 0;\n}\n"
        )
        
        build_content = (
            f"@echo off\nchcp 65001 > nul\n"
            f"taskkill /F /IM \"{project_name}.exe\" >nul 2>&1\n"
            f"g++ \"{project_name}.cpp\" -o \"{project_name}.exe\"\n"
            f"if %errorlevel% equ 0 (\n    cls\n    \"{project_name}.exe\"\n) else (\n    pause\n)"
        )
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cpp_template)
        with open(build_bat_path, "w", encoding="utf-8") as f:
            f.write(build_content)

        sublime_build = {
            "shell_cmd": f"\"{build_bat_path}\"",
            "working_dir": clean_path,
            "encoding": "utf-8"
        }

    # 3. Настройка Python
    else:
        file_path = os.path.join(project_path, f"{project_name}.py")
        py_template = (
            "# -*- coding: utf-8 -*-\nimport sys, io\n"
            "sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')\n\n"
            f"print('Проект {project_name} (Python) запущен!')\n"
            "input('Нажмите Enter для выхода...')"
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(py_template)

        sublime_build = {
            "shell_cmd": f"start \"{project_name}\" cmd /c \"python -u {project_name}.py\"",
            "working_dir": clean_path,
            "encoding": "utf-8"
        }

    # 4. Файл сборки
    build_config_path = os.path.join(project_path, f"{project_name}.sublime-build")
    with open(build_config_path, "w", encoding="utf-8") as f:
        json.dump(sublime_build, f, indent=4)

    # 5. МГНОВЕННЫЙ ЗАПУСК И ВЫХОД
    # Используем DETACHED_PROCESS, чтобы процесс Sublime не был привязан к консоли скрипта
    subprocess.Popen([SUBLIME_PATH, project_path, file_path], 
                     creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    
    # Скрипт просто завершается, не ожидая ничего
    sys.exit()

if __name__ == "__main__":
    create_project()