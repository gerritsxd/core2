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

# --- 1. Read all YAML files into memory ---

all_constructs = []
yaml_files = glob.glob(os.path.join(specs_dir, "*.yaml"))

for file_path in yaml_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        # Use safe_load_all to handle multiple documents and get the first valid one.
        documents = yaml.safe_load_all(f)
        construct_data = next((doc for doc in documents if doc), None)

    if not construct_data:
        print(f"Warning: No valid YAML document found in {file_path}. Skipping.")
        continue

    # The actual data is under the 'dct' key.
    dct_data = construct_data.get('dct', {})
    if not dct_data:
        print(f"Warning: 'dct' key is missing or empty in {file_path}. Skipping.")
        continue

    construct_id = os.path.basename(file_path).replace(".dct.yaml", "")
    all_constructs.append({'id': construct_id, 'data': dct_data})

print(f"Loaded {len(all_constructs)} constructs from YAML files.")

# --- 2. Generate individual construct QMD pages and search index ---

search_index = []
for construct in all_constructs:

    # Get data from the pre-loaded list
    construct_id = construct['id']
    dct_data = construct['data']
    
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

# --- 3. Generate static listing pages ---

def generate_listing_page(title, filename, constructs, content_field, field_title):
    # Create a simple HTML table for the listing
    html_table = "<table>\n<thead><tr><th>Construct</th><th>" + field_title + "</th></tr></thead>\n<tbody>\n"
    for construct in constructs:
        content_data = construct['data'].get(content_field)
        if content_data:
            # Extract the text, whether it's a direct string or in a nested dict
            text = content_data if isinstance(content_data, str) else next(iter(content_data.values()), "")
            if text.strip():
                construct_link = f"<a href='/repo/constructs/{construct['id']}.html'>{construct['data'].get('label', 'No Label')}</a>"
                html_table += f"<tr><td>{construct_link}</td><td>{text}</td></tr>\n"
    html_table += "</tbody>\n</table>"

    # Create the QMD content with the static HTML table
    qmd_content = f"---\ntitle: \"{title}\"\n---\n\n::: {{=html}}\n{html_table}\n:::\n"

    # Write to the corresponding index.qmd file
    page_path = os.path.join(project_root, "repo", filename, "index.qmd")
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(qmd_content)
    print(f"Generated static listing page: {page_path}")

# Generate all the listing pages

generate_listing_page("Construct Definitions", "definitions", all_constructs, 'definition', 'Definition')
generate_listing_page("Developing Measurement Instruments", "measurement-instruments", all_constructs, 'measure_dev', 'Instructions')
generate_listing_page("Coding Measurement Instruments", "coding-measurement-instruments", all_constructs, 'measure_code', 'Instructions')
generate_listing_page("Eliciting Construct Content", "qualitative-data", all_constructs, 'aspect_dev', 'Instructions')
generate_listing_page("Coding Qualitative Data", "coding-qualitative-data", all_constructs, 'aspect_code', 'Instructions')

print("Done generating all pages.")
