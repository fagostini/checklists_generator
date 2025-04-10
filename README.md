# QC_checklist_generator

Python wrapper to automatically generate the bioinfo QC checklist

## Requirements

- Python 3.10 or higher
- [Quarto](https://quarto.org/docs/get-started/) installed

## Usage

Clone the repository and run the following command in the root directory:

```bash
python -m generate_checklist.py
```

This will generate the QC checklist in HTML format in the current directory. The checklist will be named `<project_id>_QC_checklist.html`. It will also generate a `.qmd` file with the same base name, which can be used to modify the checklist if needed. The `.qmd` file is a Quarto document that can be edited and rendered to generate a new HTML file with the updated checklist.

To re-generate the checklist after modifying the `.qmd` file, run the following command:

```bash
quarto render <project_id>_QC_checklist.qmd --to html --embed-resources --standalone
```

## Options

- `--help`: Show the help message and exit.
- `--template`: The path to the Quarto template file. The default template is the `QC_template.qmd` in the current directory.
- `--format`: The output format for the checklist. The default is `markdown`. The other option is `html`. If `markdown` is selected, the script can make use of the `md_path` option to save the markdown file in a specific location.
- `--project`: The project ID for which the QC checklist will be generated. If not provided, the script will leave a generic placeholder (`<project_id>`) in the output file.
- `--flowcell`: The flowcell ID for the project. If not provided, the script will leave a generic placeholder (`<flowcell_id>`) in the output file.
- `--author`: The full name of the author. If not provided, the script will not include the author in the output file.
- `--email`: The email address of the author. If not provided, the script will not include the email in the output file.
- `--md-path`: The path where the markdown file will be saved. If not provided, the script will not produce a markdown file.
- `--ngi-path`: The path to the NGI folder on Miarka. This is used to generate the path to the project folders. If not provided, the script will leave a generic placeholder (`<ngi_path>`) in the output file.
- `--genstat-url`: The URL for the Genomics Status page. If not provided, the script will leave a generic placeholder (`<genstat_url>`) in the output file.
- `--charon-url`: The URL for the Charon page. If not provided, the script will leave a generic placeholder (`<charon_url>`) in the output file.
- `--quarto-path`: The path where the Quarto file will be saved. The default is `/usr/local/bin/quarto`. If the executable is not found, the script will attempt to search for it in the system path.
- `--output-dir`: The directory where the output files will be saved. The default is the current directory.
- `--force`: Force overwrite of existing files. If not provided and the output file already exists, the script will not overwrite it and will exit with an error message.
- `--log-level`: The logging level. The default is `INFO`. Other options are `DEBUG`, `WARNING`, `ERROR`, and `CRITICAL`. This can be set to `DEBUG` for more detailed logging information.

## Configuration file

If a `config.json` file is present in the same directory as the script, it will be used to set the default values for all or some of the options. The configuration file should be in JSON format and can include the following keys:

- `template [string]`
- `format [string]`
- `project [string]`
- `flowcell [string]`
- `author [string]`
- `email [string]`
- `md_path [string]`
- `ngi_path [string]`
- `genstat_url [string]`
- `charon_url [string]`
- `quarto_path [string]`
- `output_dir [string]`
- `force [bool]`
- `log_level [string]`

> Note: The base path on Miarka and the URLs for Genomics Status and Charon have been replaced with generic placeholders (`<ngi_path>`, `<genstat_url>`, and `<charon_url>`) in the template file. This was done to avoid hardcoding sensitive information in the script. Therefore, it is highly recommended to set these values in the local configuration file or pass them as command line arguments when running the script. The script will use the provided values to replace the placeholders in the template file before generating the final output.

### Example of `config.json` file:

```json
{
  "author": "John Doe",
  "email": "john.doe@scilifelab.se",
  "ngi_path": "/path/to/NGI/folder",
  "genstat_url": "https://genstat.example.com",
  "charon_url": "https://charon.example.com",
  "quarto_path": "/usr/local/bin/quarto"
}
```
