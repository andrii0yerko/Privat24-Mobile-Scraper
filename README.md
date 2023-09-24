# Privat24 Mobile Scraper

This project is a scraper designed for the Privat24 mobile app, enabling the extraction and export of historical transactional data into structured formats such as xlsx.

# Overview
## Problem Statement

In Privat24's web interface, exporting data to Excel is possible. However, the limitation arises in the capability to export transactions from only one card at a time and from a 3 month period, rather than the entire transaction history. The problem lies in the fact that if the card no longer exists, there is no transaction history associated with it.

On the mobile application, the full transaction history is available, but unfortunately, there is no export functionality.

Primarily, I wish to automate this process to avoid the manual effort of exporting data. Manually entering expenses and incomes as they occur is a tedious task, and I would prefer to have an automated system in place. The objective is to streamline the analytical aspect, allowing for comprehensive financial insights without the need for manual data entry.


## Demo
[demo.webm](https://github.com/andrii0yerko/Privat24-Mobile-Scraper/assets/46103860/bbb0c4ac-a3b8-42cb-ac91-291aa1b11191)

And result

![demo_result](https://github.com/andrii0yerko/Privat24-Mobile-Scraper/assets/46103860/15557110-8d45-4f15-a274-2308c266d00a)


# Documentation

## Prerequisites

- [Appium](http://appium.io/docs/en/2.1/quickstart/) installed and running (see [installation/environment](#environment) for details)
- USB connected Android device with:
    - USB Debugging mode enabled
    - granted access to your PC
    - [Privat24](https://play.google.com/store/apps/details?id=ua.privatbank.ap24) installed and launched (currently, the transaction history page must be open)
- Python or Docker to run the scraper

## Installation

### Environment
To run the scraper you need to have the appium server running.

Make sure to export the Appium server URL into the `APPIUM_SERVER_URL` environment variable or pass it as `--appium-server-url` to the application.
The default URL is `http://localhost:4732`.

#### Using Docker

Start the environment using Docker Compose:

```bash
docker compose up
```

#### Without Docker

If you choose not to use Docker, follow these steps:

1. Install the Android SDK (the easiest way is to install Android Studio).
2. Install Appium globally using npm:
   
   ```bash
   npm i --global appium
   ```

3. Install the uiautomator2 driver for Appium:
   
   ```bash
   appium driver install uiautomator2
   ```

4. Start Appium:
   
   ```bash
   appium
   ```

Refer to [Appium Quickstart Guide](https://appium.io/docs/en/2.1/quickstart) for a complete guide.

### Scraper

To install and use this application, follow the steps below:

#### **Using Docker:**
1. Build an image
    ```bash
    docker build . -t privat-exporter
    ```
   
2. Run the container
   ```bash
   docker run --rm -it --network=host -v $(pwd):/outputs privat-exporter --end-date 2023-09-22
   ```

#### **Using Poetry:**

0. Have [poetry](https://python-poetry.org/) installed

1. Install dependencies
   ```bash
   poetry install
   ```
2. Run the application
    ```
   poetry run python run.py --end-date="2023-09-21" --export-format="xlsx"
    ```

#### **Using Pip:**
0. Create a virtual environment
    ```
    python -m venv env
    source env/bin/activate
    ```

1. Install dependencies
    ```
    pip install .
    ```

2. Run the application
    ```
    python run.py --end-date="2023-09-21" --export-format="xlsx"
    ```

#### Development installation
This project's codebase is managed by [Poetry](https://python-poetry.org/), [Pre-commit](https://pre-commit.com/), and utilizes [black](https://github.com/psf/black), [Isort](https://pycqa.github.io/isort/), and [Flake8-pyproject](https://pypi.org/project/Flake8-pyproject/). Ensure that you integrate them with your IDE for efficient development.


1. Install project dependencies (including dev dependencies)
    ```
    poetry install --with dev
    ```

2. Set up pre-commit hooks
    ```
    pre-commit install
    ```

3. Make sure to integrate Black, Isort, and Flake8 with your IDE to adhere to the project's code style guidelines and maintain consistent code quality.

## Troubleshooting

### Socket hang up
**Problem**:
```
...
selenium.common.exceptions.WebDriverException: Message: An unknown server-side error occurred while processing the command. Original error: Could not proxy command to the remote server. Original error: socket hang up
...
```

**Solution**: Try to reboot the device
