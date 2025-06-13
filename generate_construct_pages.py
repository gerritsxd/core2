import os
import yaml
import glob
import json

# Get the directory of the current script, which is the project root
project_root = os.path.dirname(os.path.abspath(__file__))

# Define paths relative to the project root
specs_dir = os.path.join(project_root, "repo", "data", "dctSpecs")
output_dir = os.path.join(project_root, "repo", "constructs")

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get list of YAML files
yaml_files = glob.glob(os.path.join(specs_dir, "*.yaml"))

# List to hold search index entries
search_index = []

# Loop through each YAML file and create a QMD file
for file_path in yaml_files:
    
    with open(file_path, 'r', encoding='utf-8') as f:
        construct_data = yaml.safe_load(f)

    # The actual data is under the 'dct' key
    dct_data = construct_data.get('dct', {})

    # Extract construct ID from filename
    construct_id = os.path.basename(file_path).replace(".dct.yaml", "")
    
    # --- Create QMD content ---
    title = dct_data.get('label', 'No Label')
    qmd_front_matter = f"""---
title: "{title}"
subtitle: "UCID: {construct_id}"
format: html
toc: true
---

"""

    # Helper to create sections
    def create_section(section_title, content_dict, key):
        text = None
        if isinstance(content_dict, dict):
            # It's a dictionary, get the text using the provided key
            text = content_dict.get(key)
        elif isinstance(content_dict, str):
            # It's a string, so that's our text
            text = content_dict

        if text and text.strip():
            return f"## {section_title}\n\n{text}\n\n"
        return ""

    # 2. Build sections
    qmd_definition = create_section("Definition", dct_data.get('definition', {}), 'definition')
    qmd_measure_dev = create_section("Developing Measurement Instruments", dct_data.get('measure_dev', {}), 'instruction')
    qmd_measure_code = create_section("Coding Measurement Instruments", dct_data.get('measure_code', {}), 'instruction')
    qmd_aspect_dev = create_section("Eliciting Construct Content (Qualitative Research)", dct_data.get('aspect_dev', {}), 'instruction')
    qmd_aspect_code = create_section("Coding Qualitative Data", dct_data.get('aspect_code', {}), 'instruction')

    # Combine all parts
    qmd_content = (
        qmd_front_matter +
        qmd_definition +
        qmd_measure_dev +
        qmd_measure_code +
        qmd_aspect_dev +
        qmd_aspect_code
    )
    
    # Define output path
    output_file_path = os.path.join(output_dir, f"{construct_id}.qmd")
    
    # Write to file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(qmd_content)
    
    print(f"Generated: {output_file_path}")

    # Add entry to search index
    search_index.append({
        'title': title,
        'subtitle': f"UCID: {construct_id}",
        'url': f"/repo/constructs/{construct_id}.html"
    })

# Write the search index to a file in the overview directory
search_index_path = os.path.join(project_root, "repo", "overview", "search_index.json")
with open(search_index_path, 'w', encoding='utf-8') as f:
    json.dump(search_index, f, indent=2)

print(f"Generated search index: {search_index_path}")
print("Done generating construct pages.")
