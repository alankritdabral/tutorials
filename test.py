import subprocess
import tempfile
import shutil
import os

def get_modified_pngs():
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        capture_output=True,
        text=True,
        check=True
    )
    files = result.stdout.strip().split("\n")
    return [f for f in files if f.endswith(".png")]

def compress_selected(files, repo_root):
    for rel_path in files:
        file_path = os.path.join(repo_root, rel_path)

        if not os.path.exists(file_path):
            print(f"⚠ Skipped (missing): {file_path}")
            continue

        try:
            original_size = os.path.getsize(file_path)

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                temp_output = tmp.name

            subprocess.run([
                "pngquant",
                "--quality=60-80",
                "--output", temp_output,
                "--force",
                file_path
            ], check=True)

            new_size = os.path.getsize(temp_output)

            if new_size < original_size:
                backup_path = file_path + ".bak"
                shutil.copy2(file_path, backup_path)
                shutil.move(temp_output, file_path)

                print(f"✔ Compressed: {file_path} ({original_size} → {new_size})")
            else:
                os.remove(temp_output)
                print(f"➜ Skipped (no gain): {file_path}")

        except Exception as e:
            print(f"✖ Error: {file_path} → {e}")

# Run
repo_path = "/home/alankrit/Desktop/tutorials"
files = get_modified_pngs()
compress_selected(files, repo_path)