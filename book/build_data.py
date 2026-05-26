import json
import os

def load_file_content(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return f"[Error reading file: {e}]"
    return ""

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    metadata_path = os.path.join(script_dir, "metadata.json")

    if not os.path.exists(metadata_path):
        print(f"Error: {metadata_path} not found.")
        return

    with open(metadata_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    book_data = []

    for category_item in data:
        category_name = category_item["category"]
        folder_name = category_item["folder"]
        folder_path = os.path.join(project_root, folder_name)

        if not os.path.exists(folder_path):
            print(f"Warning: Week folder '{folder_path}' does not exist.")
            continue

        processed_category = {
            "category": category_name,
            "topics": []
        }

        print(f"Processing category: {category_name}...")

        for topic in category_item["topics"]:
            topic_name = topic["name"]
            theory_filename = topic.get("theory_file")
            
            md_content = ""
            if theory_filename:
                theory_path = os.path.join(folder_path, theory_filename)
                md_content = load_file_content(theory_path)
            
            code_content = ""

            # 1. Single code file
            code_filename = topic.get("code_file")
            if code_filename:
                code_path = os.path.join(folder_path, code_filename)
                if os.path.exists(code_path):
                    code_content += f"// --- {code_filename} ---\n" + load_file_content(code_path) + "\n\n"

            # 2. List of specific code files
            code_filenames = topic.get("code_files", [])
            for c_file in code_filenames:
                code_path = os.path.join(folder_path, c_file)
                if os.path.exists(code_path):
                    code_content += f"// --- {c_file} ---\n" + load_file_content(code_path) + "\n\n"

            # 3. Whole folder of code recursively (e.g. experiment directories)
            code_folder = topic.get("code_folder")
            if code_folder:
                code_folder_path = os.path.join(folder_path, code_folder)
                if os.path.exists(code_folder_path):
                    for root, dirs, files in os.walk(code_folder_path):
                        # Skip virtual envs, node_modules, caches, system files
                        dirs[:] = [d for d in dirs if not d.startswith('.') and d.lower() not in ['bootstrap', 'node_modules', '__pycache__', 'instance']]
                        for file in files:
                            if file.startswith('.') or file.endswith('.map') or file.endswith('.db') or file.endswith('.pyc') or file.endswith('.png') or file.endswith('.pdf'):
                                continue
                            if file.endswith((".py", ".js", ".css", ".html", ".sql", ".yaml", ".yml", ".sh", ".txt", ".env", ".md")):
                                full_file_path = os.path.join(root, file)
                                rel_path = os.path.relpath(full_file_path, code_folder_path)
                                # Prepend the folder name to maintain clarity in UI code view
                                display_path = os.path.join(code_folder, rel_path).replace("\\", "/")
                                code_content += f"// --- {display_path} ---\n" + load_file_content(full_file_path) + "\n\n"

            processed_topic = {
                "name": topic_name,
                "description": topic.get("description", ""),
                "theory": md_content,
                "code": code_content.strip()
            }
            processed_category["topics"].append(processed_topic)

        book_data.append(processed_category)

    # Save to book_data.js
    output_js = os.path.join(script_dir, "book_data.js")
    with open(output_js, 'w', encoding='utf-8') as f:
        f.write("const SOURCE_DATA = ")
        json.dump(book_data, f, indent=2)
        f.write(";")
        
    print(f"Successfully generated {output_js}!")

if __name__ == "__main__":
    main()
