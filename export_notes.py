#!/usr/bin/env python3

import os
import sys
import zipfile
import subprocess
import shutil
from trilium_py.client import ETAPI

TRILIUM_API_TOKEN = os.environ.get("TRILIUM_API_TOKEN")
TRILIUM_SERVER_URL = os.environ.get("TRILIUM_URL", "http://localhost:8080")
NOTE_ID_TO_EXPORT = os.environ.get("TRILIUM_NOTE_ID", "root")
OUTPUT_FILE_PATH = "/home/tm/ccie-notes/trilium-export.zip"
EXTRACT_TO_DIRECTORY = "/home/tm/ccie-notes/"
EXTRACT_ROOT_FOLDER = "/home/tm/ccie-notes/root/"

print(f"Connecting to Trilium at {TRILIUM_SERVER_URL}...")

def export_trilium():
    try:
        ea = ETAPI(TRILIUM_SERVER_URL, TRILIUM_API_TOKEN)

        # connect to the server
        app_info = ea.app_info()
        print(f"Successfully connected to Trilium version {app_info.get('appVersion')}.")

        # export the notes to zip file
        ea.export_note(
                noteId=NOTE_ID_TO_EXPORT,
                format='md',
                save_path=OUTPUT_FILE_PATH
                )

        print(f"Exported notes")

        # empty extraction directory
        print(f"Preparing target directory: '{EXTRACT_ROOT_FOLDER}'...")
        if os.path.exists(EXTRACT_ROOT_FOLDER):
            try:
                shutil.rmtree(EXTRACT_ROOT_FOLDER)
                print(" Removed existing directory and its contents.")
            except OSError as e:
                print(f" Error: Could not remove directory {EXTRACT_ROOT_FOLDER}: {e}")
                return False 
        else:
            print(" Directory does not exist, no cleanup needed.")

        # extract zip file
        print(f"Extracting '{OUTPUT_FILE_PATH}' to '{EXTRACT_TO_DIRECTORY}'...")
        with zipfile.ZipFile(OUTPUT_FILE_PATH, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_TO_DIRECTORY)
        print("extraction complete")

        # create index files
        create_directory_indexes(EXTRACT_ROOT_FOLDER)

        add_frontmatter(EXTRACT_ROOT_FOLDER)

        # delete old zip file
        print("delteing zip file")
        os.remove(OUTPUT_FILE_PATH)
        print("delted zip file")
        
        print("finished")
        return True

    except Exception as e:
        print(f"An error occured during the export: {e}") # fix to display error
        return False

def add_frontmatter(root_folder):
    """ Adds frontmatter to each note in tree """
    print("Adding Jekyll front matter to Md files")

    for root, dirs, files in os.walk(root_folder):
        for file in files:
            # only do md files
            if not file.endswith(".md") or file == "index.md":
                continue
            
            file_path = os.path.join(root, file)
            title = os.path.splitext(file)[0]

            relative_dir_path = os.path.relpath(root, root_folder)
            parent_name = None

            if relative_dir_path != ".":
                # set parent to name of dir
                parent_name = os.path.basename(relative_dir_path)
            else:
                parent_name = "Root"

            front_matter_lines = ["---", "layout: default", f"title: {title}", f"parent: {parent_name}", "---", ""]

            front_matter = "\n".join(front_matter_lines)

            try:
                # read original content
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()

                # write new frontmatter
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(front_matter + original_content)

            except Exception as e:
                    print(f" Could not process {file_path}: {e}")


def create_directory_indexes(root_folder):
    """ Walks the dir tree and adds an index.md for each folder to support Jekyll tree structures """
    print("Creating directory index files...")

    for root, dirs, files in os.walk(root_folder):
        index_file_path = os.path.join(root, "index.md")

        if os.path.exists(index_file_path):
            print(f" Skipping creation, {index_file_path} already exists.")
            continue

        relative_dir_path = os.path.relpath(root, root_folder)

        if relative_dir_path == ".":
            title = "Root"
            parent_name = None
        else:
            title = os.path.basename(root)
           
            parent_dir = os.path.dirname(relative_dir_path)
            if parent_dir == ".":
                parent_name = "Root"
            else:
                parent_name = os.path.basename(parent_dir)
            
            has_md_files = any(f.endswith(".md") and f != "index.md" for f in files)
            has_subdirs = len(dirs) > 0
            has_children = has_md_files or has_subdirs

            front_matter_lines = ["---", "layout: default", f"title: {title}"]
            if parent_name:
                front_matter_lines.append(f"parent: {parent_name}")

            if has_children:
                front_matter_lines.append(f"has_children: true")

            front_matter_lines.append("---")
            front_matter_lines.append("")

            try:
                with open(index_file_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(front_matter_lines))
            except Exception as e:
                print(f" Could not create {index_file_path}: {e}")

            print("Finished creating index files.")

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
    if export_trilium():
        git_push_changes("Content Update")
    else:
        print("Export failed. Will not git push")
        sys.exit(1)
