import argparse
import json
import logging
import pathlib
import re
import subprocess
from datetime import datetime

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a list of files in a directory."
    )
    parser.add_argument(
        "--template",
        type=pathlib.Path,
        help="Path to the template file.",
        default=pathlib.Path("QC_template.qmd"),
    )
    parser.add_argument(
        "--format",
        type=str,
        help="Output format for the checklist.",
        default="markdown",
        choices=["markdown", "html"],
    )
    parser.add_argument(
        "--project",
        type=str,
        help="Project name.",
        default=None,
    )
    parser.add_argument(
        "--flowcell",
        type=str,
        help="Flowcell identifier.",
        default=None,
    )
    parser.add_argument(
        "--author",
        type=str,
        help="Author name.",
        default=None,
    )
    parser.add_argument(
        "--email",
        type=str,
        help="Author email.",
        default=None,
    )
    parser.add_argument(
        "--md-path",
        type=pathlib.Path,
        help="Path to the markdown destination directory.",
        default=None,
    )
    parser.add_argument(
        "--ngi-path",
        type=pathlib.Path,
        help="Path to the NGI folder.",
        default=None,
    )
    parser.add_argument(
        "--genstat-url",
        type=str,
        help="Base URL for Genomics Status.",
        default=None,
    )
    parser.add_argument(
        "--charon-url",
        type=str,
        help="Base URL for Charon.",
        default=None,
    )
    parser.add_argument(
        "--quarto-path",
        type=pathlib.Path,
        help="Path to the Quarto executable.",
        default=pathlib.Path("/usr/local/bin/quarto"),
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        help="Path to the output directory.",
        default=pathlib.Path("."),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite of existing files.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        help="Set the logging level. Default is INFO.",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    return parser.parse_args()


def set_run_parameters(args):
    """Set the run parameters based on the command-line arguments."""
    config = {}
    # Load the config file if it exists
    if pathlib.Path("config.json").is_file():
        with open("config.json", "r") as f:
            config = json.load(f)
        # Check for alien keys in the config file
        not_found = {key for key in config.keys() if key not in vars(args).keys()}
        if not_found:
            logging.warning(
                f"One or more keys in the config file are not among the expected keys: {not_found}"
            )
        for key, value in config.items():
            if "path" in key or "dir" in key:
                # Convert string paths to pathlib.Path objects
                config[key] = pathlib.Path(value)

    # Re-set the config parameters based on command-line arguments
    for key, value in vars(args).items():
        if key not in config or value is not None:
            # Update the config with command-line arguments
            config[key] = value

    # Set the output directory and file basename
    prefix = datetime.now().strftime("%Y%m%d")
    config["basename"] = (
        f"{prefix}_{config['project']}_QC_checklist"
        if config["project"]
        else f"{prefix}_QC_checklist"
    )

    return config


def validate_project_id(project_id: str):
    """Validate the project ID format."""
    if not re.match(r"^P[0-9]{5}$", project_id):
        raise ValueError(
            "Project ID must start with 'P' followed by 4 or 5 digits (e.g., P1234 or P12345)."
        )


def validate_flowcell_id(flowcell_id: str):
    """Validate the flowcell ID format."""
    if not re.match(
        r"^[0-9]{6,8}_[A-Z]{1,2}[0-9]{5}_[0-9]{3,4}_[A-Z0-9]{9,10}(-[A-Z0-9]{5})?$",
        flowcell_id,
    ):
        raise ValueError(
            "Flowcell ID is not in the expected format. Please check the ID."
        )


def prepare_markdown_header(config: dict):
    """Prepare the markdown header with project and author information."""
    md_header = "---\n"
    md_header += (
        f"title: {config['project']} QC and delivery\n"
        if config["project"]
        else "title: Bioinformatic QC and delivery\n"
    )
    md_header += (
        f"author: {config['author']} <{config['email']}>\n"
        if config["author"] and config["email"]
        else f"author: {config['author']}\n"
        if config["author"]
        else ""
    )
    md_header += "\n".join(
        [
            "subtitle: 'Bioinformatic Sample QC and Preparation for Data Delivery'",
            "description: 'Automatically generated QC checklist'",
            "date: today",
            "lang: en-GB",
            "format:",
            "  html:",
            "    page-layout: full",
            "    anchor-sections: true",
            "    tbl-cap-location: bottom",
            "    theme:",
            "      light: flatly",
            "      dark: darkly",
            "  commonmark:",
            "    wrap: none",
            "version: 1.0",
            "---",
            "",
        ]
    )
    return md_header


def write_markdown_template(config: dict):
    """Write the markdown template with project and author information."""
    # Prepare the markdown header
    header = prepare_markdown_header(config)
    with open(f"{config['basename']}.qmd", "w") as output_file:
        output_file.write(header)
        # Write the template content
        with open(config["template"], "r") as template_file:
            for line in template_file:
                if config["project"]:
                    line = re.sub(r"<project_id>", f"{config['project']}", line)
                if config["flowcell"]:
                    line = re.sub(r"<flowcell_id>", f"{config['flowcell']}", line)
                if config["author"]:
                    line = re.sub(r"<author_name>", f"{config['author']}", line)
                if config["ngi_path"]:
                    line = re.sub(r"<ngi_path>", f"{config['ngi_path']}", line)
                if config["genstat_url"]:
                    line = re.sub(r"<genstat_url>", f"{config['genstat_url']}", line)
                if config["charon_url"]:
                    line = re.sub(r"<charon_url>", f"{config['charon_url']}", line)
                output_file.write(line)


def cleanup_temporary_data(config: dict):
    """Remove temporary files and directories created during the process."""
    files_list = list(pathlib.Path().glob(f"**/{config['basename']}*.md"))
    for tmp_md in files_list:
        if tmp_md.is_file():
            logging.debug(f"Removing temporary file: {tmp_md}")
            tmp_md.unlink()

    paths_list = list(pathlib.Path().glob(f"**/{config['basename']}_files"))
    for tmp_path in paths_list:
        for path, dirs, files in tmp_path.walk(top_down=False):
            for file in files:
                file_path = pathlib.Path(path).joinpath(file)
                if file_path.is_file():
                    logging.debug(f"Removing temporary file: {file_path}")
                    file_path.unlink()
            logging.debug(f"Removing temporary directory: {path}")
            path.rmdir()


if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()

    # Set the logging level based on the command-line argument
    logging.getLogger().setLevel(args.log_level)

    # Set the run parameters according to the command-line arguments and config file
    config = set_run_parameters(args)

    # Validate the project ID
    if args.project:
        validate_project_id(args.project)

    # Validate the flowcell ID
    if args.flowcell:
        validate_flowcell_id(args.flowcell)

    # Check if the Quarto executable exists and is accessible
    status, quarto_version = subprocess.getstatusoutput(
        f"{config['quarto_path']} --version"
    )
    if status != 0:
        logging.error(
            "Quarto not found in the specified path. Attempting to find it in the system path."
        )
        # Attempt to find Quarto in the system path
        status, quarto_path = subprocess.getstatusoutput("which quarto")
        if status != 0:
            logging.error("Quarto not found in the system path.")
            exit(1)
        else:
            # Update the config with the correct Quarto path
            config["quarto_path"] = pathlib.Path(quarto_path)
            status, quarto_version = subprocess.getstatusoutput(
                f"{quarto_path} --version"
            )
    # Check if the template file exists
    if not config["template"].is_file():
        logging.error("The specified template file does not exist.")
        exit(1)
    # Check if the markdown output directory exists
    if config["md_path"]:
        if not config["md_path"].is_dir():
            logging.error(
                "The specified markdown output path does not exist. Skipping markdown generation."
            )
            exit(1)

    # Check if the output directory exists
    if not args.force:
        files_list = []
        if (
            config["md_path"].joinpath(f"{config['basename']}.md").is_file()
            and config["format"] == "markdown"
        ):
            files_list.append(config["md_path"].joinpath(f"{config['basename']}.md"))
        if (
            config["output_dir"].joinpath(f"{config['basename']}.html").is_file()
            and config["format"] == "html"
        ):
            files_list.append(
                config["output_dir"].joinpath(f"{config['basename']}.html")
            )
        if config["output_dir"].joinpath(f"{config['basename']}.qmd").is_file():
            files_list.append(
                config["output_dir"].joinpath(f"{config['basename']}.qmd")
            )
        if files_list:
            logging.error(
                "The following files already exist and will not be overwritten:"
            )
            for file in files_list:
                logging.error(f"    '{file}'")
            logging.error(
                "Use --force to overwrite existing files or specify a different output directory."
            )
            exit(1)

    # Summarise the run parameters
    logging.debug("-" * 40)
    logging.debug("Run Parameters:")
    logging.debug(f"    Quarto Path: {config['quarto_path']}")
    logging.debug(f"    Quarto Version: {quarto_version}")
    logging.debug(f"    Template: {config['template']}")
    logging.debug(f"    Project ID: {config['project']}")
    logging.debug(f"    Flowcell ID: {config['flowcell']}")
    logging.debug(f"    NGI Path: {config['ngi_path']}")
    logging.debug(f"    Author: {config['author']}")
    logging.debug(f"    Author Email: {config['email']}")
    logging.debug(f"    Output Directory: {config['output_dir']}")
    logging.debug(f"    Output Format: {config['format']}")
    if config["format"] == "markdown":
        logging.debug(f"    Markdown Output Path: {config['output_dir']}")
        logging.debug(f"    Markdown Filename: {config['basename']}.md")
    else:
        logging.debug(f"    HTML Output Path: {config['output_dir']}")
        logging.debug(f"    HTML Filename: {config['basename']}.html")
    logging.debug("-" * 40)

    # Write the markdown template, including the dynamic content
    write_markdown_template(config)

    # Prepare the base command to run Quarto
    cmd = f"{config['quarto_path']} render {config['basename']}.qmd"
    cmd += f" --output-dir {config['output_dir']} --execute-dir {config['output_dir']}"

    if config["format"] == "markdown":
        # Generate the Markdown file and place it in the specified directory
        logging.debug("Generating QC checklist markdown via Quarto...")
        cmd2 = cmd + f" --to commonmark --output {config['basename']}.md"
        try:
            out = subprocess.run(cmd2, shell=True, check=True, capture_output=True)
            if config["md_path"]:
                with open(
                    config["md_path"].joinpath(f"{config['basename']}.md"), "w"
                ) as output_file:
                    with open(
                        config["output_dir"].joinpath(f"{config['basename']}.md"), "r"
                    ) as input_file:
                        for line in input_file:
                            if line.startswith("<"):
                                # Remove some HTML tags for aesthetic purposes
                                line = re.sub(r"<div>", "", line).strip()
                                line = re.sub(r"</div>", "", line).strip()
                            output_file.write(line)
            logging.info("Markdown file generated successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error generating markdown: {e}")
            exit(1)

    elif config["format"] == "html":
        try:
            # Generate the HTML file
            logging.debug("Generating QC checklist HTML via Quarto...")
            cmd2 = (
                cmd
                + f" --to html --output {config['basename']}.html --embed-resources --standalone --debug"
            )
            out = subprocess.run(cmd2, shell=True, check=True, capture_output=True)
            logging.info("HTML file generated successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error generating HTML: {e}")
            exit(1)
    else:
        logging.error("Invalid format specified. Use 'markdown' or 'html'.")
        exit(1)

    logging.debug("-" * 40)

    logging.debug("Cleaning up temporary files and folders...")
    cleanup_temporary_data(config)

    logging.debug("-" * 40)
