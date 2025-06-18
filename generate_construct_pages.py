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
    
    construct_data = None
    with open(file_path, 'r', encoding='utf-8') as f:
        # Use safe_load_all to handle multiple documents in a single file
        # and find the first valid (non-empty) document.
        documents = yaml.safe_load_all(f)
        for doc in documents:
            if doc:  # Check if the document is not None or empty
                construct_data = doc
                break # Found the first valid document, stop looking

    # If no valid data was found in the file, skip it
    if not construct_data:
        print(f"Warning: No valid YAML document found in {file_path}. Skipping.")
        continue

    # The actual data is under the 'dct' key
    dct_data = construct_data.get('dct', {})

    # Extract construct ID from filename
    construct_id = os.path.basename(file_path).replace(".dct.yaml", "")
    
    # --- Create QMD content ---
    title = dct_data.get('label', 'No Label')

    # Create front matter as a Python dictionary
    front_matter_dict = {
        'title': title,
        'subtitle': f"UCID: {construct_id}",
        'format': 'html',
        'toc': True
    }

    # Use yaml.dump to create a correctly formatted and escaped YAML string.
    # This is much more robust than manual string formatting.
    qmd_front_matter = f"---\n{yaml.dump(front_matter_dict)}---\n\n"

    # Helper to create sections
    def create_section(section_title, content):
        text = None
        if content is None:
            return "" # Section doesn't exist, return empty string

        if isinstance(content, str):
            # Case 1: The content is just a direct string
            text = content
        elif isinstance(content, dict):
            # Case 2: The content is a dictionary.
            # We assume the text is the value of the *first* key in the dictionary.
            # This is robust and doesn't rely on hardcoded keys like 'definition' or 'instruction'.
            if content: # Check if dictionary is not empty
                text = next(iter(content.values()), None)

        if text and str(text).strip():
            return f"## {section_title}\n\n{text}\n\n"
        return ""

    # 2. Build sections by passing the direct object from the YAML
    qmd_definition = create_section("Definition", dct_data.get('definition'))
    qmd_measure_dev = create_section("Developing Measurement Instruments", dct_data.get('measure_dev'))
    qmd_measure_code = create_section("Coding Measurement Instruments", dct_data.get('measure_code'))
    qmd_aspect_dev = create_section("Eliciting Construct Content (Qualitative Research)", dct_data.get('aspect_dev'))
    qmd_aspect_code = create_section("Coding Qualitative Data", dct_data.get('aspect_code'))

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
