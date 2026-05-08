# Title

A Python project for bioinformatics tasks.

## Description

This project is set up for HackBio, a bioinformatics internship program for stage one submission. It includes essential libraries for bioinformatics, data analysis, and machine learning.

## Project Report
- [project_overview.md](docs/project_overview.md): Full project report — what we did, why, and what it means biologically. **Start here.**
- [concepts.md](docs/concepts.md): Core mathematical and scientific concepts used in this project.

## Requirements

- Python 3.8+ (We used 3.12.2 on our machine)
- Dependencies listed in `requirements.txt`

### Key Libraries Used
- **biopython**: Toolkit for reading, parsing, and analyzing biological data.
- **numpy**: Foundational library for numerical computing and array operations.
- **pandas**: Essential for data manipulation and working with structured data (DataFrames).
- **scikit-learn**: Machine learning library for clustering, PCA, and predictive modeling.
- **matplotlib**: Core library for creating detailed charts and visual plots.
- **seaborn**: High-level statistical data visualization library built on matplotlib.
- **scipy**: Provides algorithms for advanced statistics, optimization, and scientific computing.
- **openpyxl**: Backend library used by pandas to read and write modern Excel (`.xlsx`) files.

## Installation

1. Clone or download the repository.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the main script:
```
python .\src\main.py > .\outputs\script_output.txt
```

## Project Structure

- `src/`: Source code directory
- `data/`: GDSC xlsx data (Taken from Public Database)
- `docs/`: If you are new to the concepts used in this project, please read our docs first.
- `requirements.txt`: Python dependencies. A text file listing all the third-party Python tools we need (like pandas for handling data tables, seaborn for drawing charts, and openpyxl for reading Excel files). If we share this project with others, their computer doesn't know what supporting tools to use. They just run one command (pip install -r requirements.txt), and their computer installs everything automatically. It ensures everyone is using the exact same tools.
- `.gitignore`: Git ignore file
- `README.md`: This file. It’s the first thing anyone reads when they visit our project. It gives the context.