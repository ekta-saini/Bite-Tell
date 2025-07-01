# Bite & Tell - Food Blog

A simple and elegant food blog built with pure Python. This blog allows you to create posts with text and images, and manage your content easily.

## Live Demo

Visit our blog at: `http://localhost:8000`

To run locally:
1. Clone this repository
2. Run `python server.py`
3. Open your browser and navigate to `http://localhost:8000`

## Features

- Clean, modern UI with a responsive design
- Create posts with text and images
- Image preview before posting
- Delete posts functionality
- Posts stored as JSON files
- No database required

## Requirements

- Python 3.x

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ekta-saini/Bite-Tell.git
cd Bite-Tell
```

2. Run the server:
```bash
python server.py
```

3. Open your web browser and visit:
```
http://localhost:8000
```

## Usage

- Visit the homepage to view all posts
- Click "Create Post" to add a new post
- Add images to your posts (optional)
- Delete posts using the × button in the top-right corner of each post

## Project Structure

```
Bite-Tell/
├── server.py          # Main server file
├── templates/         # HTML templates
│   ├── index.html    # Homepage template
│   └── create.html   # Create post template
├── static/           # Static files
│   └── style.css     # Stylesheet
└── posts/            # Post storage directory
```

## Contributing

Feel free to fork this project and submit pull requests with improvements! 