#-*- coding: utf-8 -*-
import os
import glob
from embeddings import create_embedding
from ye_logger_of_yor import get_logger

logger = get_logger()

def run_embed_project(file_path):
    project_folder = file_path
    output_folder = 'embeddings'
    # Get all .py files in the project folder and its subdirectories
    project_files = glob.glob(os.path.join(project_folder, '**/*.py'), recursive=True)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    logger.info("Converting files to Markdown")


    def convert_files(project_files):
        count = 0
        # Convert each .py file to a Markdown
        for python_file in project_files:
            count += 1

            # Read the file content
            with open(python_file, 'r', encoding='UTF-8', errors='ignore') as f:
                file_content = f.read()

            # Create a Markdown version of the code with syntax highlighting
            code_md = f"```python\n{file_content}\n```\n"

            # Set output file path
            output_file = os.path.join(output_folder, os.path.relpath(python_file, project_folder))
            output_file = os.path.splitext(output_file)[0] + '.md'

            # Ensure the directory for the output file exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            # Write the Markdown file
            with open(output_file, 'w') as f:
                f.write(code_md)

            # Print progress to the console
            logger.info(f"File {count}/{len(project_files)} saved: {os.path.relpath(python_file, project_folder)}")

            # Create the embedding
            logger.info("Creating embedding...")
            create_embedding(output_file)
    result = convert_files(project_files)
    logger.info("Done!")
    return result