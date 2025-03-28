import shutil
import os
import glob


def run(path, silent=False, **kwargs):
    """Delete a file or directory."""

    # Check if wildcard pattern matches multiple files
    
    path = os.path.abspath(path)
    
    files = glob.glob(path)
    if not files:
        print(f"⚠️ Warning: File or directory '{path}' not found!")
        return True
        
    if len(files) > 1:
        print(f"⚠️ Warning: Multiple files found matching '{path}'")
        for file in files:
            os.remove(file)
            if not silent:
                print(f"✔️ Deleted '{file}'")
        return True
    

    shutil.rmtree(path)
    if not silent:
        print(f"✔️ Deleted '{path}'")
    return True
