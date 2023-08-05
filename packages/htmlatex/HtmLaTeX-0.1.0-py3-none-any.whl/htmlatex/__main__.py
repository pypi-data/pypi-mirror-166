import argparse
from pathlib import Path

from htmlatex import TreeWalker


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert HTML to LaTeX")
    parser.add_argument('html_file', type=Path, help="The HTML file to convert")
    return parser.parse_args()


def main():
    args = parse_args()
    html_file: Path = args.html_file
    latex_file = html_file.with_suffix('.tex')

    html_code = html_file.read_text()
    soup = BeautifulSoup(html_code, "html.parser")
    html_node = soup.html
    if html_node is None:
        raise ValueError("No <html> tag found")

    with open(latex_file, 'w+') as output_file:
        TreeWalker(output=output_file, handlers=handlers).walk(html_node)


if __name__ == "__main__":
    main()