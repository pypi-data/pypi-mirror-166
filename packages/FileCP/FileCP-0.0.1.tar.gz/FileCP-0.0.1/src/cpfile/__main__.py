def cpfile():
	from rich.console import Console
	from rich.markdown import Markdown
	from rich import print
	from rich.text import Text
	import os
	import argparse
	import pyperclip

	console = Console()
	parser = argparse.ArgumentParser(prog='FileCP:  Copy Files Content Instantly')
	parser.add_argument("file", help="Enter File Path (Strict or Relative)")
	parser.add_argument('-v','--version', action='version', version='%(prog)s 0.1')
	parser.add_argument("-a", help="About cpfile and license", action='store_true')
	args = parser.parse_args()

	if args.a:
		about_content = "# FileCP"
		about_md = Markdown(about_content)
		console.print(about_md)
		console.print("\n :zap: Made by [link=https://newtoallofthis123.github.io/About]NoobScience[/link]")
		quit()
	file_path = args.file
	with open(file_path, "r") as file_open:
		file_content = file_open.read()
		pyperclip.copy(str(file_content))

if __name__ == '__main__':
	cpfile()