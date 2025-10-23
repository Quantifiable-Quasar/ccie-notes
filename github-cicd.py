#!/usr/bin/env python3

import os
import sys
import zipfile
from trilium_py.client import ETAPI

TRILIUM_API_TOKEN = "X6Q566RYx657_P7uojkhk14P7cEK8OML+9lIurnYbZxPU0zokCd/T4tU="
TRILIUM_SERVER_URL = os.environ.get("TRILIUM_URL", "http://localhost:8080")
NOTE_ID_TO_EXPORT = os.environ.get("TRILIUM_NOTE_ID", "root")
OUTPUT_FILE_PATH = "/home/tm/trilium-notes/trilium-export.zip"
EXTRACT_TO_DIRECTORY = "/home/tm/trilium-notes/"

print(f"Connecting to Trilium at {TRILIUM_SERVER_URL}...")

def export_trilium():
    try:
        ea = ETAPI(TRILIUM_SERVER_URL, TRILIUM_API_TOKEN)

        # connect to the server
        app_info = ea.app_info()
        print(f"Successfully connected to Trilium version {app_info.get('appVersion')}.")
        #print(f"Starting export for note ID '{NOTE_ID_TO_EXPORT'...")

        # export the notes to zip file
        ea.export_note(
                noteId=NOTE_ID_TO_EXPORT,
                format='md',
                save_path=OUTPUT_FILE_PATH
                )

        print(f"Exported notes")

        # extract zip file
        print(f"Extracting '{OUTPUT_FILE_PATH}' to '{EXTRACT_TO_DIRECTORY}'...")
        with zipfile.ZipFile(OUTPUT_FILE_PATH, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_TO_DIRECTORY)
        print("extraction complete")

        # delete old zip file
        print("delteing zip file")
        os.remove(OUTPUT_FILE_PATH)
        print("delted zip file")
        
        print("finished")
        sys.exit(0)

    except Exception as e:
        print(f"An error occured during the export: {e}") # fix to display error
        sys.exit(1)

def run_git_command(command_list):
    """Runs git command and checks for errors"""
    try:
        result = subprocess.run(
                command_list,
                check=True,
                text=True,
                capture_output=True
                )
        print(f"STDOUT: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command_list)}")
        print(f"STDERR: {e.stderr}")
        return False

def git_push_changes(commit_message):
    """ Adds all changes and commits with message as param """
    # Git Add
    if not run_git_command(["git", "add", "."]):
        print("Failed to add files")
        return

    # Git Commit
    if not run_git_command(["git", "commit", "-m", commit_message]):
        print("failed to commit")
        return

    # Git push
    if not run_git_command(["git", "push"]):
        print("failed to push")
        return

if __name__ == "__main__":
    export_trilium()
    git_push_changes("Daily Update")
