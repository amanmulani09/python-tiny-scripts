from pathlib import Path

old_file = Path("old_file.txt")
new_file = Path("new_file.txt")

try:
    old_file.rename(new_file)
    print("File renamed successfully!")
except Exception as e:
    print(f"Error: {e}")