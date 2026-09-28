# Checklists generator

Python script to dynamically generate the bioinfo production checklists for QC, Delivery and Close of NGI sequencing projects. The script uses Quarto to generate the checklists in HTML or markdown format. The checklists are based on templates that can be customized to fit the needs of different projects.

The templates are based on the following internal documents and versions:

- Bioinfo QC: _1617:**6**_
- Delivery: _1286:**23**_
- Close: _1262:**18**_

## Requirements

- Python 3.10 or higher
- Python dependencies: `pip install -r requirements.txt`
- [Quarto](https://quarto.org/docs/get-started/) installed

## Usage

Clone the repository and run the following minimal command in the root directory:

```bash
python generate_checklists.py --output-path . --format html
```

This will generate three checklists (i.e. QC, Delivery and Close) in HTML format in the current directory. It will also generate the corresponding `.qmd` files with the same base name, and place them in the `qmds` folder. A `.qmd` file is a Quarto document that can be edited and rendered to generate a new HTML file with the updated checklist.

To re-generate any of the checklists after having modified its `.qmd` file, run the following command:

```bash
quarto render qmds/<qmd_file> --to html --embed-resources --standalone
```

Instead, if you want to generate the checklists in markdown format, run:

```bash
quarto render qmds/<qmd_file> --to markdown --embed-resources --standalone
```

## Options

- `--help`: Show the help message and exit.
- `--templates-path`: The path to the template files. The default is `templates`. The script will look for three files in this directory: `QC_template.qmd`, `Delivery_template.qmd`, and `Close_template.qmd`. These files are used to generate the QC checklist, delivery checklist, and close checklist, respectively.
- `--format`: The output format for the checklist: `markdown` or `html`. This is required, either via this option or the `format` key in the configuration file.
- `--name`: The project name (format: `<username>_<year>_<index>`). If not provided, the script will leave a generic placeholder (`<project_name>`) in the output file.
- `--project`: The project ID for which the QC checklist will be generated. If not provided, the script will leave a generic placeholder (`<project_id>`) in the output file.
- `--flowcell`: The flowcell ID for the project. If not provided, the script will leave a generic placeholder (`<flowcell_id>`) in the output file.
- `--slide`: The slide ID (used by the Visium best practice checklist). If not provided, the script will leave a generic placeholder (`<slide_id>`) in the output file.
- `--genome-path`: The path to the genome files. If not provided, the script will leave a generic placeholder (`<genome_path>`) in the output file.
- `--transcriptome-path`: The path to the transcriptome files. If not provided, the script will leave a generic placeholder (`<transcriptome_path>`) in the output file.
- `--author`: The full name of the author. If not provided, the script will not include the author in the output file.
- `--signature`: The author signature (initials) used in the running notes. If not provided, the signature placeholders are removed from the output file.
- `--email`: The email address of the author. If not provided, the script will not include the email in the output file.
- `--instrument`: The instrument type: `illumina` (default) or `aviti`.
- `--best-practice`: Set to `visium` to also generate the Visium data analysis checklist.
- `--ngi-path`: The path to the NGI folder on Miarka. This is used to generate the path to the project folders. If not provided, the script will leave a generic placeholder (`<ngi_path>`) in the output file.
- `--incoming-path`: The path to the incoming data folder. If not provided, the script will leave a generic placeholder (`<incoming_path>`) in the output file.
- `--visium-base-path`: The path to the Visium base folder (probe sets, feature references). If not provided, the script will leave a generic placeholder (`<visium_base_path>`) in the output file.
- `--config-path`: The path to the TACA configuration folder. This is used to generate the path to the project folders. If not provided, the script will leave a generic placeholder (`<config_path>`) in the output file.
- `--genstat-url`: The URL for the Genomics Status page. If not provided, the script will leave a generic placeholder (`<genstat_url>`) in the output file.
- `--charon-url`: The URL for the Charon page. If not provided, the script will leave a generic placeholder (`<charon_url>`) in the output file.
- `--quarto-path`: The path to the Quarto executable. If not provided, or if the executable is not found at the given path, the script will attempt to search for `quarto` in the system path.
- `--output-path`: The directory where the output files will be saved. The default is the current directory.
- `--local-reports-path`: The local path where the MultiQC and reports folders are saved. If not provided, the script will leave a generic placeholder (`<local_reports_path>`) in the output file.
- `--timestamp`: Whether to include a timestamp in the output file name. The default is `False`. If `True`, the output files will be named `<YYYYMMDD>_<project_id>_<Label>.{html,md,qmd}` (e.g. `20260127_P37871_QC.html`).
- `--output-structure`: The structure of the output. The default is `flat`. The other option is `nested`. If `nested` is selected, the output files will be saved in a subdirectory named after the timestamp and project ID.
- `--script-assets-path`: The path to the assets folder used by the templates. The default is the `assets` folder in this repository.
- `--force`: Force overwrite of existing files. If not provided and the output file already exists, the script will not overwrite it and will exit with an error message.
- `--log-level`: The logging level. The default is `INFO`. Other options are `DEBUG`, `WARNING`, `ERROR`, and `CRITICAL`. This can be set to `DEBUG` for more detailed logging information.

## Configuration file

If a `config.json` file is present in the same directory as the script, it will be used to set the default values for all or some of the options. The configuration file should be in JSON format and can include the following keys:

- `templates_path [string]`
- `format [string]`
- `project [string]`
- `flowcell [string]`
- `author [string]`
- `email [string]`
- `ngi_path [string]`
- `incoming_path [string]`
- `config_path [string]`
- `genstat_url [string]`
- `charon_url [string]`
- `quarto_path [string]`
- `output_path [string]`
- `timestamp [bool]`
- `output_structure [string]`
- `force [bool]`
- `log_level [string]`
- `slide [string]`
- `genome_path [string]`
- `transcriptome_path [string]`
- `instrument [string]`
- `visium_base_path [string]`
- `local_reports_path [string]`
- `script_assets_path [string]`

> Note: `config.json` is gitignored and will not be tracked. To get started, copy `config.json.example` to `config.json` and fill in the values that apply to your environment. Any keys omitted from `config.json` will fall back to their command-line argument counterparts.

### Example of `config.json` file:

```json
{
  "author": "Your Name",
  "email": "your.name@scilifelab.se",
  "format": "markdown",
  "output_path": "/path/to/output/directory",
  "output_structure": "nested",
  "quarto_path": "/usr/local/bin/quarto",
  "ngi_path": "/path/to/NGI/folder",
  "incoming_path": "/path/to/incoming/folder",
  "genstat_url": "https://genomics-status.example.com",
  "charon_url": "https://charon.example.com",
  "config_path": "/path/to/conf/TACA",
  "log_level": "INFO"
}
```
