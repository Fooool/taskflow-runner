import os


def run(dir, **kwargs):
    """Create a directory or directories"""
    # Check if dir is a list of directories
    if isinstance(dir, list):
        for d in dir:
            try:
                os.makedirs(d, exist_ok=True)
                print(f"📂 Created directory: '{d}'")
            except Exception as e:
                print(f"❌ Error: {e}")
                return False
    else:
        try:
            os.makedirs(dir, exist_ok=True)
            print(f"📂 Created directory: '{dir}'")
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    return True
