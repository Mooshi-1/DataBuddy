from pywinauto import Application
from pywinauto.keyboard import send_keys
import pygetwindow as gw
import time
import sys

def main():
    try:
        app = Application(backend="uia").connect(title_re="AMDIS Chromatogram.*", class_name="GCMSANAL")
    except Exception as e:
        print(f'An Error Ocurred: Unable to establish connection to AMDIS | {e}',flush=True)
        print(f'Is this program running on the same computer as AMDIS?', flush=True)
        return
    main_window = app.window(title_re="AMDIS Chromatogram.*")
    print('found AMDIS application; starting loop')
    process_list = main_window.child_window(title="Results of Last Batch Job")
    main_window.set_focus()


    children_list = process_list.child_window(control_type="List")
    items = children_list.children()

    filtered_items = [item for item in items if item.element_info.control_type != "ScrollBar"]
    try:
        filtered_items[0].click_input()
    except Exception as e:
        print(f"an error occured | {e}")
        print("the first item in the reprocessing list is not on the screen")

    print(f"printing {len(filtered_items)} reports")
    counter = 0

    file = main_window.child_window(title="File", control_type = "MenuItem", found_index = 0, visible_only=False)
    main_window.set_focus()

    for item in filtered_items:
        start_time = time.time()
        counter += 1
        item_string = str(item)
        print(f"{counter} / {len(filtered_items)}, {item_string.split("'")[1]}")

        print('starting ready check')
        main_window.wait("ready", timeout=10)
        print('ready')
        file.click_input()

        send_keys("%m")
        send_keys("t")
        send_keys("%f")
        send_keys("p")
        time.sleep(0.5)
        send_keys("%p")
        time.sleep(0.5)
        send_keys("%p")

        process_list.set_focus()
        time.sleep(1)
        send_keys("{DOWN}")

        end_time = time.time()

        elapsed_time = end_time - start_time
        print(f"{elapsed_time:.2f} seconds this loop")
        remaining_items = len(filtered_items) - (counter)
        expected_time = elapsed_time * remaining_items / 60
        print(f"expected {expected_time:.2f} minutes remaining to complete", flush=True)

    main_window.minimize()

if __name__ == '__main__':
    print(f"sys.argv: {sys.argv}", flush=True)
    main()
    print("SCRIPT END")
