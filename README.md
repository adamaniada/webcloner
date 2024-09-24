# Website Cloning Script

This script is designed to clone a website by downloading its HTML content and associated resources such as images, stylesheets, and scripts.

## Features

- Downloads the main page and all linked pages within the same domain.
- Saves the HTML content and resources in a structured directory format.
- Handles absolute and relative URLs for resource downloading.
- Avoids downloading repeated content by keeping track of visited URLs.
- Implements a progress bar for visual feedback during the download process.

## Prerequisites

Before running this script, ensure you have the following installed:
- Python 3
- `requests` library
- `BeautifulSoup` library from `bs4` package
- `tqdm` library

You can install the required libraries using `pip`:

```bash
pip install requests beautifulsoup4 tqdm
```

## Usage
To use the script, simply call the clone_website function with the URL of the website you wish to clone and the output folder where you want to save the cloned content:

```Python
clone_website('https://www.example.com/', 'example_clone')
```

## Disclaimer
This script is for educational purposes only. Ensure you have permission to clone the website and that you comply with the website’s terms of service and copyright laws.

## License
This project is open-sourced under the MIT License. See the LICENSE file for more details.


Please replace `https://www.example.com/` with the actual URL you want to clone and `example_clone` with your desired output folder name. Also, make sure to check the legality of cloning a website and respect the terms of service and copyright laws of the source website.
