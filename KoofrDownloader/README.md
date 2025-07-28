# KoofrDownloader

A customisable tool to scrape and download files from a public Koofr share link.

## Requirements

Install dependencies:

```
pip install -r requirements.txt
```

Contents of `requirements.txt`:

```
undetected-chromedriver
selenium
requests
```

## Usage

Run the script:

```
python KoofrDownloader.py
```

When prompted, enter the full Koofr public share URL, for example:

```
https://app.koofr.net/links/xxxxxxxx
```

The script will click through the initial "public sharing limit reached" gate and extract the actual shared folder title.
It then creates a folder using that title and saves all found media files inside.

## Customization

If you want to extract other types of files (e.g., `.pdf`, `.zip`, `.docx`), modify the `media_extensions` list in the script:

```python
media_extensions = ['.mp4', '.jpg', '.jpeg', '.png', '.pdf', '.zip']
```

## Notes

- The script runs headless using `undetected-chromedriver`
- Relative paths are converted to absolute URLs
- Retries downloads on failure (default: 3 attempts)
- Files are saved inside a folder named after the actual Koofr shared folder (not the warning page)

## Disclaimer

This tool is provided for educational and research purposes only. Do not use it to scrape or download content you do not have permission to access.
