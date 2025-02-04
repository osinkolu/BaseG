# Base.G -  Baseball Stat Extractor with AI ⚾🚀

## Overview

This project is built for the **Google Cloud x MLB Hackathon – Building with Gemini Models**, specifically for **Challenge 4: Generate Statcast Data from Old Videos**.

The goal of this project is to create an AI-powered tool that extracts fundamental **Statcast metrics** (e.g., **pitch speed, exit velocity, player stats, scores**) from archival baseball game videos using **computer vision and Gemini AI**. The extracted data is then structured into a tabular format, allowing users to interact with and query it.

## Features

- **Upload Baseball Videos or Images** 📹🖼️
- **Scene Detection & Key Frame Extraction** 🎞️
- **OCR & AI-Powered Data Extraction with Gemini** 🤖
- **Automatic SI Unit Formatting (e.g., mph for pitch speed)** ⚡
- **Structured & Clean Data Representation** 📊
- **Chat with Your Data – Ask Questions in Natural Language** 💬
- **Optimized Caching to Avoid Reprocessing Images on Queries** 🚀

## How It Works

1. **Upload a Video or Image** – The user uploads a baseball game video (`.mp4`, `.avi`, `.mov`) or an image (`.jpg`, `.png`, `.jpeg`).
2. **Scene Detection** – Key frames are extracted from the video using **SceneDetect** to capture meaningful game moments.
3. **OCR & AI Processing** – Each frame is sent to **Google Gemini AI**, which extracts and structures relevant **game statistics** (e.g., **pitch speed, player names, scores, etc.**).
4. **Data Structuring** – Extracted data is consolidated and formatted to ensure consistent column names and SI units.
5. **Display & Interaction** – Users can view structured stats in a table and **chat with the data**, asking specific questions about the game.

## Installation & Setup

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- `pip` package manager
- `Streamlit`
- `OpenCV`
- `SceneDetect`
- `Pandas`
- `Google Generative AI SDK`

### Installation Steps

1. Clone the repository:

   ```sh
   git clone https://github.com/your-repo/baseball-stat-extractor.git
   cd baseball-stat-extractor
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up Google Gemini API key:

   ```sh
   export GEMINI_API_KEY="your_api_key_here"
   ```

4. Run the Streamlit app:

   ```sh
   streamlit run app.py
   ```

## Usage

1. **Upload a Baseball Video or Image**.
2. **View Extracted Frames** in an expandable section.
3. **View the structured statistics** in a tabular format.
4. **Chat with Your Data** by typing natural language queries.

## Example Queries

- *"What was the pitch speed in the 3rd inning?"*
- *"Who was the batter at timestamp 00:15?"*
- *"Show me the exit velocity of all home runs."*

## Tech Stack

- **Frontend**: Streamlit
- **AI Processing**: Google Gemini API
- **Computer Vision**: OpenCV, SceneDetect
- **Data Processing**: Pandas

## Future Enhancements

- **Enhanced Player Recognition** – Improve name detection via facial recognition models.
- **More Advanced Queries** – Support multi-frame aggregation for deeper insights.
- **Live Streaming Support** – Process live baseball footage in real time.

## Contributors

- **Victor Olufemi**
- **Moshood Kausar**
- **Ogunmuyiwa Stephen**

## License

This project is open-source under the MIT License.

## Acknowledgments

- **Google Cloud x MLB Hackathon** for organizing this challenge.
- **OpenAI & Google AI** for providing powerful AI tools.

---
✨ Built with AI & Love for Baseball ⚾❤️
