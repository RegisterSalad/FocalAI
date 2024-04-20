# FocalAI

## Project Description

FocalAI is a Linux desktop application designed to facilitate the exploration, download, and execution of models from various AI model repositories. This tool aims to serve as the "Steam" of AI models, providing robust search capabilities and comprehensive model information, making it easy for AI enthusiasts to run a variety of models right out of the box. FocalAI utilizes paperswithcode to support its functionalities.

### Objective

Develop an application that allows users to:
- Browse and interact with AI models directly.
- Download and execute models securely and efficiently.
- Generate sample code snippets using GPT-4 for model interaction.

### Main Features

1. **Direct Model Interaction:** Explore, download, and interact with a selection of popular AI models within a secure sandbox environment in the app.
2. **Sample Code Generation:** Generate and provide sample code based on user prompts and model documentation.
3. **Comprehensive Search and Information System:** Search through models using keywords, datasets, associated papers, and publication years.
4. **Scalability and Flexibility:** Integrate with multiple AI model repositories and adapt based on user feedback and technological advancements.

## Repository Structure

- **`build.sh`**: Script to build and configure the application.
- **`LICENSE`**: The project's open-source license file.
- **`README.md`**: Documentation providing an overview and setup instructions.
- **`requirements.txt`**: List of Python libraries required to run the application.
- **`src/`**: Source directory containing Python scripts and frontend components:
  - **`api_caller.py`**, **`conda_env.py`**, **`database.py`**, etc.: Backend scripts for API calls, environment setup, and database management.
  - **`frontend_build/`**: Contains frontend components like model viewers, UI widgets, and style configurations.

## Installation Instructions

### Prerequisites

- **Anaconda**: Manages Python versions and dependencies.
- **Bash Shell**: Required for executing the build script.

### Step-by-Step Installation

1. **Install Anaconda**:
   - Download and install from [Anaconda's official site](https://www.anaconda.com/download).
   - Follow the website's instructions to integrate Anaconda with your bash profile.

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/RegisterSalad/FocalAI
   cd FocalAI
   ```

3. **Run the Build Script**:
   - To build normally:
     ```bash
     ./build.sh
     ```
   - To clean and build:
     ```bash
     ./build.sh -clean
     ```

4. **Verify Installation**:
   - Check the `./app` directory for the executable.
   - Consult the `build_log.log` for detailed output of the build process.

## Contributing

This project is open-source and we welcome contributions from the community. Please review the code documentation and user guide for details on how to contribute.
