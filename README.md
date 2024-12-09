# Web Scraper with GUI

A simple web scraper with a graphical user interface built in Python using tkinter. This program allows users to download web pages and their associated images through a user-friendly interface.

## Features

- Simple graphical user interface
- Downloads webpage HTML content
- Extracts and downloads images from the webpage
- Real-time status updates
- Folder selection dialog
- Thread-based scraping to prevent UI freezing

## Requirements

- Python 3.x
- No external libraries required (uses only built-in Python libraries)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/web-scraper-gui.git
```

2. Navigate to the project directory:
```bash
cd web-scraper-gui
```

## Usage

1. Run the program:
```bash
python scraper.py
```

2. Enter the URL of the webpage you want to scrape
3. Click "Browse" to select a destination folder
4. Click "Run Scraper" to start the process
5. Monitor progress in the status bar at the bottom

## How It Works

The scraper performs the following steps (referenced from scraper.py):
```python:scraper.py
startLine: 9
endLine: 113
```

1. Creates the specified folder if it doesn't exist
2. Connects to the website and downloads the HTML content
3. Saves the HTML content to a file
4. Extracts image URLs from the HTML
5. Downloads each image and saves it to the specified folder

## Interface Components

The GUI includes:
- URL input field
- Folder selection with browse button
- Run button
- Status bar showing current progress

## Limitations

- Basic URL parsing
- No support for JavaScript-rendered content
- Limited error handling
- Basic image URL extraction
- No support for authentication
- No respect for robots.txt
- No rate limiting

## Security Note

This is a basic implementation and doesn't include:
- SSL certificate verification
- Input sanitization
- Rate limiting
- Robot.txt compliance

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Always check a website's terms of service and robots.txt before scraping. Be respectful of websites' resources and implement appropriate delays between requests in production use.