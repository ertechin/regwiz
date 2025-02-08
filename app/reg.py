import winreg
import sys
import os
import importlib.util
import keyboard

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(_file_)

# Windows registry root keys mapping
ROOT_KEYS = {
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
    "HKEY_USERS": winreg.HKEY_USERS,
    "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG
}

def set_reg_value(root, path, name, value, reg_type=winreg.REG_SZ):
    """Set a registry value"""
    try:
        with winreg.OpenKey(root, path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, name, 0, reg_type, value)
        print(f" [- OK -] Successfully set => '{name}' to '{value}' in '{path}'")
    except FileNotFoundError:
        print(f" [- FAILED -] Registry key not found in => '{name}' to '{value}' in '{path}'")
    except PermissionError:
        print(f" [- FAILED -] Error: Permission denied. Run as administrator for => '{name}' to '{value}' in '{path}'")
    except Exception as e:
        print(f" [- FAILED -]- Error setting '{name}' to '{value}' in '{path}': {e}")
          
def find_non_static_path(base_path, after_dynamic_path, values):
    """Find a dynamic GUID-like folder inside a given registry path and ensure all required values exist."""
    print("-----> [- OK -] Starting search for dynamic paths")

    found_any_guid = False

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base_path) as base_key:
            index = 0
            while True:
                try:
                    guid = winreg.EnumKey(base_key, index)
                    dynamic_path = f"{base_path}\\{guid}\\{after_dynamic_path}"

                    try:
                        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, dynamic_path) as sub_key:
                            print(f"-----> [- OK -] Checking path => {dynamic_path}")
                            missing_values = []
                            for value in values.keys():
                                try:
                                    winreg.QueryValueEx(sub_key, value)
                                    print(f"-----> [- OK -] Value found: {value}")
                                except FileNotFoundError:
                                    missing_values.append(value)
                                    print(f"-----> [- FAILED -] {value} NOT found in => {dynamic_path}")

                            if missing_values:
                                print(f"-----> [- FAILED -] Skipping {dynamic_path}, missing values: {', '.join(missing_values)}")
                                continue

                            print(f"-----> [- OK -] Found valid dynamic path: {dynamic_path}")
                            found_any_guid = True
                            return dynamic_path

                    except FileNotFoundError:
                        print(f"-----> [- FAILED -] Subfolder '{after_dynamic_path}' missing under {base_path}\\{guid}")

                except OSError:
                    print(f"-----> [- OK -] No more subkeys to enumerate, stopping search")
                    break

                index += 1

    except FileNotFoundError:
        print(f"-----> [- FAILED -] Error: Base registry path not found: {base_path}")

    if not found_any_guid:
        print(f"-----> [- FAILED -] No valid dynamic path found for {base_path}")

    return None


def load_registry_changes():
    """Load registry files and handle dynamic paths inside SYSTEM paths"""
    reg_dir = os.path.join(BASE_DIR, "reg_paths")

    allowed_files = {
        "HKEY_CLASSES_ROOT.py": "HKEY_CLASSES_ROOT",
        "HKEY_CURRENT_USER.py": "HKEY_CURRENT_USER",
        "HKEY_LOCAL_MACHINE.py": "HKEY_LOCAL_MACHINE",
        "HKEY_USERS.py": "HKEY_USERS",
        "HKEY_CURRENT_CONFIG.py": "HKEY_CURRENT_CONFIG"
    }

    all_changes = []

    for filename, root_key_name in allowed_files.items():
        reg_file_path = os.path.join(reg_dir, filename)

        if not os.path.exists(reg_file_path):
            continue

        root_key = ROOT_KEYS[root_key_name]

        spec = importlib.util.spec_from_file_location(root_key_name, reg_file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "changes"):
            for change in module.changes:
                path = change.get("path")

                if "static_base_path" in change and "after_dynamic_path" in change:
                    base_path = change["static_base_path"]
                    after_dynamic_path = change["after_dynamic_path"]
                    values = change["values"]

                    detected_path = find_non_static_path(base_path, after_dynamic_path, values)

                    if detected_path:
                        path = detected_path
                    else:
                        print(f"⚠️ Skipping {base_path} (No valid dynamic path found)")
                        continue

                change["root"] = root_key
                change["path"] = path
                all_changes.append(change)

    return all_changes
    
def wait_for_exit():
    """Keep the script running until CTRL + Q is pressed."""
    print("\n Press 'CTRL + Q' to exit the program...")
    keyboard.wait("ctrl+q")

def main():
    print("\n STARTING THE EDITING REGISTRY")
    """Read registry changes from all files and apply them"""
    registry_changes = load_registry_changes()

    for change in registry_changes:
        root = change["root"]
        path = change["path"]

        if "values" not in change:
            print(f" Skipping entry in '{path}' (No 'values' found)")
            continue

        for name, value in change["values"].items():
            set_reg_value(root, path, name, value)

if __name__ == '__main__':
    main()
    wait_for_exit()
