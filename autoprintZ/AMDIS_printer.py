from pywinauto import Application
from pywinauto.keyboard import send_keys
import pygetwindow as gw
import time

def main():

    app = Application(backend="uia").connect(title_re="AMDIS Chromatogram.*", class_name="GCMSANAL")

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

    # def printer(main_window, process_list, counter):
    #     counter += 1
    #     main_window.set_focus()

    #     all_windows = gw.getAllTitles()
    #     target_windows = [w for w in all_windows if w.startswith("AMDIS Chromatogram")]
    #     sample_name = target_windows[0].split(' - ')[2].strip()
    #     print(f'printing report #{counter} - {sample_name}')

    #     file = main_window.child_window(title="File", control_type = "MenuItem", found_index = 0, visible_only=False)
    #     file.click_input()

    #     send_keys("%m")
    #     send_keys("t")
    #     send_keys("%f")
    #     send_keys("p")
    #     send_keys("%p")
    #     send_keys("%p")

    #     process_list.set_focus()
    #     time.sleep(1)
    #     process_list_window = gw.getActiveWindow()
    #     print(f"current window = {process_list_window.title}")

    #     send_keys("{DOWN}")

    #     time.sleep(5)
    #     window = gw.getActiveWindow()
    #     print(f"current window = {window.title}")
    #     if process_list_window == window:
    #         print('processing complete')
    #         return
    #     else:
    #         printer(main_window, process_list, counter)


    #printer(main_window, process_list, counter)
    


    # target_mode = main_window.child_window(auto_id="1132", control_type="MenuItem", found_index=0)
    # target_mode.click_input()

    # #main_window.wait("ready", timeout=1)

    # file = main_window.child_window(title="File", control_type = "MenuItem", found_index = 0, visible_only=False)
    # file.click_input()

    # print_dialog = main_window.child_window(auto_id="161", control_type = "MenuItem", found_index = 0)
    # print_dialog.invoke()

    # Access child elements, like "Results of Last Batch Job"
    # results_dialog = main_window.child_window(title="Results of Last Batch Job", control_type="Window")
    # results_dialog.print_control_identifiers()  # Lists all child elements


if __name__ == '__main__':

    main()