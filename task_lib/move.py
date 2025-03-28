import shutil
import os
import glob


def run(src, dest, **kwargs):
    """Move files to a destination directory or rename them in the process."""

    files = glob.glob(src)  # Expand wildcard patterns

    if not files:
        print(f"❌ Error: No files found matching '{src}'")
        return False

    # If multiple files match, dest must be a directory
    if len(files) > 1 and not os.path.isdir(dest):
        print(
            f"❌ Error: Destination '{dest}' must be a directory when moving multiple files.")
        return False

    # If dest is a directory, ensure it exists
    if not os.path.isdir(dest):
        dest_dir = os.path.dirname(dest)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            print(f"📂 Created directory: '{dest_dir}'")

    for src_file in files:
        if os.path.isdir(dest):
            dest_path = os.path.join(dest, os.path.basename(
                src_file))  # Move into directory
        else:
            dest_path = dest  # Rename file while moving

        try:
            shutil.move(src_file, dest_path)
            print(f"✔️ Moved '{src_file}' → '{dest_path}'")
        except shutil.SameFileError:
            print(
                f"⚠️ Warning: Source and destination are the same for '{src_file}'")
        except PermissionError:
            print(f"❌ Error: Permission denied for '{src_file}'")
            return False
        except FileNotFoundError:
            print(f"❌ Error: File not found '{src_file}'")
            return False

    return True
