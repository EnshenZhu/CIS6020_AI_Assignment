import os
import shutil

protected_folder_location_list = [
    '../.idea',
    '../venv',
    '../input_assets',
    '../forbid'
]


def is_protected(test_folder_location):
    if test_folder_location in protected_folder_location_list:
        return True
    else:
        return False


def to_empty(folder_location):
    folder = folder_location

    # identify if the target folder is protected, which should not be emptied
    if is_protected(test_folder_location=folder):
        print('%s folder should not be emptied' % folder)
        return
    else:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
