# IKIWISI: An Interactive Visual Pattern Former

IKIWISI (pronounced "icky-wissy") stands for "I Know It When I See It." It is an interactive visual pattern-forming tool designed to evaluate the reliability of Vision-Language Models (VLMs) in multi-object recognition tasks, especially when ground truth is unavailable. Inspired by human visual perception, IKIWISI simplifies and enhances the process of model evaluation through binary heatmaps and user-friendly interactions.

## Features

- **Binary Heatmaps:** Visualize model predictions with color-coded cells (green for presence, red for absence).
- **Object and Video Selection:** Choose arbitrary objects and video frames for targeted model evaluation.
- **Interactive Corrections:** Adjust the heatmap cells to reflect corrections and observe performance changes.
- **Spy Objects:** Test model reliability with objects highly unlikely to appear.
- **User Ratings and Feedback:** Provide performance scores and detailed observations for iterative model improvement.
- **Bar Graphs and Patterns:** Summarize and highlight trends in model performance.

## System Architecture

IKIWISI is built using a client-server architecture:
- **Frontend:** Implemented in Plotly Dash for an intuitive and interactive interface.
- **Backend:** Deployed on a multi-threaded server with NVIDIA GPUs to support multiple vision-language models.

### Supported Models
- GPV-1
- BLIP
- GPT4V
- Ground Truth (for validation purposes)
- Random (baseline comparison)

## How It Works

1. **Object and Frame Selection:** Users select objects of interest and video frames from a dropdown menu.
2. **Heatmap Visualization:** Model predictions are represented in a binary heatmap.
3. **Corrections and Patterns:** Users can identify anomalies, inspect patterns, and adjust predictions interactively.
4. **Performance Feedback:** Users provide ratings and comments to guide model reliability assessments.

## User Studies

IKIWISI was evaluated through a user study involving 15 participants, ranging from machine learning experts to novices. Key findings demonstrate its usability, pattern-based decision-making support, and potential for democratizing model evaluation.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/IKIWISI.git
   cd IKIWISI
