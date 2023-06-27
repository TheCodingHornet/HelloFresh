# Recipe Downloader

## Overview

Recipe Downloader is an application built to automatically download recipes from the HelloFresh API and store them in a
Neo4j graph database. This application is ideal for anyone interested in obtaining a large amount of recipe data for
analysis or development purposes.

## Features

- Downloads recipe data directly from the HelloFresh API.
- Stores recipe data in a Neo4j graph database, allowing for complex queries and relationships.
- Includes a caching system to prevent redundant requests to the API.
- Supports test mode for development and debugging.

## Getting Started

First, clone the repository to your local machine:

```bash
git clone https://github.com/TheCodingHornet/HelloFresh.git
```

Then, navigate to the project directory and install the necessary dependencies:

```bash
cd HelloFresh
pip install -r requirements.txt
```

After installation, you can run the application:

```bash
python main.py
```

Note: Ensure that you have a running Neo4j instance, and you've configured the connection settings in the application.

## License

This project is licensed under the terms of the GNU General Public License v3.0.

## Contributing

We welcome all contributions. If you're interested in contributing, please fork the repository and make your changes,
then create a pull request to the main branch.

## Contact

For questions, issues, or feedback, please open an issue on the GitHub repository.

## Aknowledgements

This README provides an overview of the application, how to install and run it, its licensing terms, and information on
how to contribute. You can expand this with more specific information, such as a detailed guide to using the
application, specific contribution guidelines, screenshots of the application in use, or anything else you think would
be beneficial for users and potential contributors to know.