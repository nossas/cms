# Nossas CMS - Feature Adp-Observatorio

Welcome to the Nossas CMS project, with features related to the Adp-Observatorio.

## Overview

This repository contains modules and submodules related to the Adp-Observatorio feature within the Nossas CMS project. Below, you'll find an overview of each module and submodule along with installation instructions and usage guidelines.

## Modules and Submodules

### [contrib/ds](https://github.com/nossas/cms/tree/feature/adp-observatorio/app/contrib/ds)

This module contains utilities and tools for data science tasks within the Nossas CMS project.

- **preprocessing**: Provides preprocessing utilities for data cleaning and transformation.
- **feature_extraction**: Contains feature extraction algorithms and utilities.
- **modeling**: Provides machine learning models and tools for model training and evaluation.

### [contrib/observatorio](https://github.com/nossas/cms/tree/feature/adp-observatorio/app/contrib/observatorio)

This module contains features and functionalities specific to the Adp-Observatorio project.

- **api**: Implements the API endpoints for interacting with the Adp-Observatorio features.
- **views**: Contains Django views for rendering Adp-Observatorio related pages.

## Installation

To install the Nossas CMS project with the Adp-Observatorio feature, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/nossas/cms.git
    ```

2. Navigate to the `app` directory:

    ```bash
    cd cms/app
    ```

3. Install the project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Each module and submodule may have its own installation and usage instructions. Refer to the respective README files within each submodule directory for detailed instructions.

- Run tests

    ```bash
    pytest --ds=adp.settings.test
    ```

- Run tests with converage

    ```bash
    pytest --ds=adp.settings.test --cov
    ```

## Contributing

Contributions to the Nossas CMS project are welcome! If you'd like to contribute, please follow these guidelines:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and ensure all tests pass.
- Submit a pull request with a clear description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).