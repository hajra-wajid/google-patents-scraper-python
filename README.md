# google-patents-scraper-python
A high-performance Python web scraper using Scrapy and Selenium to extract over 500,000 patent records from Google Patents. Designed to handle anti-scraping defenses and dynamic content, delivering clean, structured data for analysis.
<br>
<br>
# Google Patents Data Scraper

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Scrapy](https://img.shields.io/badge/Scrapy-2.x-green.svg)
![Selenium](https://img.shields.io/badge/Selenium-4.x-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Project Overview

This repository contains a robust and scalable web scraping solution developed in Python to extract comprehensive patent data from Google Patents. The system is designed to efficiently collect over 500,000 patent records, including details such as patent title, abstract, inventors, assignees, publication dates, and claims.

## Key Features

-   **High-Performance Scraping:** Utilizes `Scrapy` for efficient, asynchronous data collection.
-   **Anti-Scraping Defense Bypass:** Integrates `Selenium` to navigate JavaScript-heavy pages and overcome anti-bot measures (e.g., dynamic content, CAPTCHAs, IP blocking).
-   **Structured Data Output:** Delivers clean, organized patent data in CSV format, ready for analysis.
-   **Scalable Architecture:** Built to handle large volumes of data, making it suitable for extensive research and intelligence gathering.
-   **Error Handling:** Includes mechanisms for robust error management and retry logic to ensure data integrity.

## Technologies Used

-   **Python 3.x**
-   **Scrapy 2.x**
-   **Selenium 4.x**
-   **Pandas** (for data processing and structuring)
-   **WebDriver Manager** (for easy WebDriver setup)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/google-patents-scraper-python.git
    cd google-patents-scraper-python
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

    _Note: A `requirements.txt` file will be provided in the actual repository containing `scrapy`, `selenium`, `pandas`, `webdriver_manager`._

4.  **Download WebDriver:**
    Selenium requires a WebDriver (e.g., ChromeDriver, GeckoDriver). `webdriver_manager` will handle this automatically, but ensure you have a compatible browser installed (e.g., Chrome, Firefox).

## Usage

1.  **Configure your scraper:**
    Open `settings.py` (if using Scrapy) or the main Python script and adjust any necessary settings (e.g., `DOWNLOAD_DELAY`, `USER_AGENT`, `CONCURRENT_REQUESTS`).

2.  **Run the scraper:**
    ```bash
    scrapy crawl patents_spider -o patents_data.csv
    ```
    (Replace `patents_spider` with the actual name of your Scrapy spider if different, or execute your main Python script directly.)

## Data Output

The extracted data will be saved in `patents_data.csv` (or your specified output file) with columns such as:

-   `patent_number`
-   `title`
-   `abstract`
-   `inventors`
-   `assignees`
-   `publication_date`
-   `filing_date`
-   `claims`
-   `description`
-   `classification`

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or collaborations, feel free to reach out:

-   (https://www.upwork.com/freelancers/hajrawajid?mp_source=share)
