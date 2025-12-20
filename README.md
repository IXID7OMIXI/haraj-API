# Haraj Explorer UI

A modern web interface for browsing Haraj.com.sa listings, built with Flask and Python.

## Features

- **Modern UI**: Dark mode, split-view design.
- **Smart Filters**: Filter by Manual/Auto transmission and custom keywords.
- **Auto-Auth**: Automatically attempts to fetch the required Client ID (with fallback).

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

1. Run the Flask server:
   ```bash
   python app.py
   ```
2. Open your browser to:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usage

- **Search**: Enter a tag (e.g., "BMW", "Camry") and press Search.
- **Filters**: Toggle "Manual" to see only manual transmission cars.
- **Load More**: Scroll down or click "Load More" to fetch the next page.
