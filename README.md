## About The Project

A utility written in Python for quickly extracting object schema data from Salesforce and saving it in Microsoft Excel format

### Built With

Python 3.9+

## Getting Started

To get a local copy up and running follow these simple steps.

1. Clone this repository or download the source files.
2. Ensure Python 3.9+ is installed
3. Install the required libraries (see the Prerequisite section)

### Prerequisites

- Python 3.9+
- [Requests](https://pypi.org/project/requests/) Library
- [XlsxWriter](https://pypi.org/project/XlsxWriter/) Library

### Installation

1. Clone the repo
   ```sh
   git clone git@github.com:codysechelski/Salesforce-Schema-Downloader.git
   ```
2. Install Requests
   ```sh
   pip install requests
   ```
3. Install XlsxWriter
   ```sh
   pip install xlsxwriter
   ```

## Usage

From a terminal, navigate to the directory created when you cloned this repo and run the `sf_describe.py` file

```sh
python sf_describe.py
```

Follow the on screen prompts

## Roadmap

1. Add more error checking
2. Add testing
3. Adding a feature to list all object for an org
4. Option to download the schema for all objects using a wildcard `*` or something
5. Implement a feature to allow for fuzzy object name matching
6. Integrate SFDX-CLI for authentication and describe
7. Support some sort of structured format that could be imported into Vizio or something like it to automatically build a graphical ERD

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Cody Sechelski - codysechelski@gmail.com

Project Link: [https://github.com/codysechelski/Salesforce-Schema-Downloader](https://github.com/codysechelski/Salesforce-Schema-Downloader)
