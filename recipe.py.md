# Recipe to Google Tasks

This project extracts recipe details (title, servings, and ingredients) from recipe websites and syncs them to Google Tasks.

## Features

- Extracts **recipe title**, **servings**, and **ingredients** from supported websites.
- Dynamically handles HTML and JSON-LD structures.
- Uses Selenium for dynamic content rendering.
- Automatically creates a Google Tasks list for the recipe and adds ingredients as tasks.

## Supported Websites

This project currently supports the following websites:

1. [BBC Good Food](https://www.bbcgoodfood.com)
2. [Drive Me Hungry](https://drivemehungry.com)
3. [China Sichuan Food](https://www.chinasichuanfood.com)
4. [Epicurious](https://www.epicurious.com)

More websites may be supported, as the project dynamically handles most common recipe structures.

## Requirements

1. **Python 3.7 or higher**
2. **Google Tasks API credentials**:
   - Enable the Google Tasks API in your [Google Cloud Console](https://console.cloud.google.com/).
   - Download the `credentials.json` file and place it in the project directory.

3. **Dependencies**:
   Install the required Python packages:
   ```bash
   pip install selenium beautifulsoup4 google-auth google-auth-oauthlib google-auth-httplib2


4. **Selenium**:
   - Selenium is used to fetch dynamic content from JavaScript-heavy websites.
   - The project uses Selenium's built-in driver management, so no manual setup of `chromedriver` is required. Make sure you have the latest version of Google Chrome installed.

## How to Use

1. Clone this repository:
   git clone <repository-url>
   cd <repository-folder>

2. Run the script:
   python RecipeToTasks.py

3. Enter the URL of the recipe you want to extract when prompted.

4. The recipe ingredients will be added to Google Tasks under a list named after the recipe title and servings.

## Notes

- The script uses fallback mechanisms to handle different website structures. However, some websites may still require adjustments for specific cases.
- If a website is not listed as supported, feel free to test it and submit an issue if it doesn’t work.
