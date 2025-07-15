# COMMS Repository Template (CoRe)

This is a Quarto-based template for creating a "Construct Repository" (CoRe), a structured collection of academic constructs or concepts. It's designed to be easily extensible and publishable as a static website on services like GitHub Pages.

## How to Use This Template: A Step-by-Step Guide

This guide provides the full workflow for a new user to clone this repository, add their own content, and publish it online.

### 1. Prerequisites (One-time Setup)

Before you begin, make sure you have the following software installed on your computer:
- [Git](https://git-scm.com/downloads) (for version control)
- [Python](https://www.python.org/downloads/) (for data processing)
- [Quarto](https://quarto.org/docs/get-started/) (for building the website)

### 2. Get the Project

Open your terminal or command prompt and run the following commands:

```bash
# Clone the repository from GitHub (replace with your repository's URL)
git clone https://github.com/your-username/your-repository-name.git

# Navigate into the new project directory
cd your-repository-name
```

### 3. Set Up the Python Environment

It is highly recommended to use a Python virtual environment to manage project dependencies.

```bash
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install the required Python package
pip install pyyaml
```

### 4. Add Your Content

The core content of this repository lives in YAML files. To add a new construct:

1.  Navigate to the `repo/data/dctSpecs/` directory.
2.  Create a new file with a `.dct.yaml` extension (e.g., `my_new_concept.dct.yaml`).
3.  Add the content for your construct inside this file, following the established YAML structure (using keys like `dct`, `label`, `definition`, etc.).

### 5. Build and Preview Your Site

Once you've added your content, you can see what your website looks like.

```bash
# To build the entire site once:
# This runs the Python script and generates all HTML files in the 'docs/' directory.
quarto render

# To preview the site with live reloading:
# This starts a local web server so you can see your changes as you save them.
quarto preview
```
When you run `quarto preview`, it will provide a URL (like `http://localhost:1234`) to open in your web browser.

### 6. Publish to GitHub Pages

This project is configured to build the website into the `/docs` directory, which makes publishing with GitHub Pages very straightforward.

1.  Commit and push all your changes to your GitHub repository.
    ```bash
    git add .
    git commit -m "Add new constructs and update site"
    git push origin main
    ```
2.  In your repository on GitHub, go to `Settings` > `Pages`.
3.  Under `Build and deployment`, select the source as `Deploy from a branch`.
4.  Set the branch to `main` and the folder to `/docs`.
5.  Click `Save`. Your site will be published at `https://your-username.github.io/your-repository-name/`.


