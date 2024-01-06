import json
import re
import os
import tkinter as tk
from tkinter import filedialog

def manual_scan_json(log_lines):
    json_started = False
    json_lines = []
    bracket_level = 0
    for line in log_lines:
        if json_started:
            bracket_level += line.count('{')
            bracket_level -= line.count('}')
            json_lines.append(line.strip())
            if bracket_level == 0:  
                yield '\n'.join(json_lines)
                json_lines = []
                json_started = False 
        elif "GroupMatchInviteAccept" in line:
            json_started = True  

def extract_and_search(file_path, pattern, custom_text="Item found!"):
    with open(file_path, 'r', encoding='utf-8') as file:
        log_content = file.readlines()

    for json_str in manual_scan_json(log_content):
        try:
            json_data = json.loads(json_str)
            nickname = json_data.get("Info", {}).get("Nickname")
            if re.search(pattern, json_str):
                return custom_text, nickname
        except json.JSONDecodeError:
            continue

    return "String not found", None


if __name__ == "__main__":
    file_path = None
    regex_patterns = [
        (r"5c94bbff86f7747ee735c08f", "TerraGroup Labs access keycard"),
        (r"62a0a16d0b9d3c46de5b6e97", "Military flash drive"),
        (r"5ed51652f6c34d2cc26336a1", "M.U.L.E. stimulant injector"),
        (r"5ed515f6915ec335206e4152", "AHF1-M stimulant injector"),
        (r"5ed515ece452db0eb56fc028", "P22 (Product 22) stimulant injector"),
        (r"5ed515c8d380ab312177c0fa", "3-(b-TG) stimulant injector"),
        (r"637b612fb7afa97bfc3d7005", "SJ12 TGLabs combat stimulant injector"),
        (r"5fca13ca637ee0341a484f46", "SJ9 TGLabs combat stimulant injector"),
        (r"5c05308086f7746b2101e90b", "Virtex programmable processor"),
        (r"5c0530ee86f774697952d952", "LEDX Skin Transilluminator"),
        (r"57347ca924597744596b4e71", "Graphics card"),
    ]

    while True:
        if not file_path:
            root = tk.Tk()
            root.withdraw()
            print("Please select the log file.")
            file_path = filedialog.askopenfilename()
            if not file_path:
                print("No file selected. Exiting...")
                break
        if not os.path.exists(file_path):
            print("File does not exist. Please check the path and try again.")
            file_path = None
            continue

        found_any = False
        for pattern, description in regex_patterns:
            search_result, nickname = extract_and_search(file_path, pattern)
            if search_result != "String not found":
                print(f"{description} was found")
                print("Nickname of User:", nickname)
                found_any = True 
        if not found_any:
            print("No other items found")

        print("Do you want to:")
        print("1) Reload and re-search the file again")
        print("2) Select a new log file")
        print("3) Close")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            continue
        elif choice == "2":
            file_path = None
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

    print("Program exited. Thank you for using the tool!")