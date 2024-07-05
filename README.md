# Keka Web Clocking Automation

This project automates the process of web clocking in and out using the Keka web application. It provides a Python script that can be run automatically on the start and stop of your computer using system services.

## Prerequisites

- Python 3.x
- Selenium WebDriver
- ChromeDriver

## Installation

1. Clone the repository or download the project files.

2. Install the required dependencies:
   ```
   pip install selenium python-dotenv
   ```

3. Install ChromeDriver and ensure it is available in your system's PATH.

## Configuration

1. Create a `.env` file in the project directory and provide the following configuration:
   ```
   KEKA_EMAIL=your_email@example.com
   KEKA_PASSWORD=your_password
   KEKA_URL=https://changeme.keka.com/ui/#
   ```
   Replace the values with your actual Keka credentials and the appropriate URL.

2. Open the `keka_script.py` file and make sure the path to ChromeDriver is correct.

## Usage

### Manual Execution

To run the script manually, use the following command:
```
python keka_script.py
```

By default, the script will perform a web check-in action. To perform a web check-out, set the `KEKA_CHECK` environment variable to `out`:
```
export KEKA_CHECK=out
python keka_script.py
```

### System Services

To automate the web clocking process on the start and stop of your computer, you can create system services. The following steps outline the process for Linux using systemd:

1. Copy the service files `keka-web-clock-in.service` and `keka-web-clock-out.service` from the `services` directory of this repository to the systemd service directory. 

The systemd service directory is typically `/etc/systemd/system/`. Please note that the systemd service directory may be different on your Linux distribution. Make sure to check the documentation or consult your system administrator if you encounter any issues.


2. Reload the systemd daemon:
   ```
   sudo systemctl daemon-reload
   ```

3. Enable the services to start automatically on boot:
   ```
   sudo systemctl enable keka-web-clock-in.service
   sudo systemctl enable keka-web-clock-out.service
   ```

4. Start the `keka-web-clock-in` service manually (optional):
   ```
   sudo systemctl start keka-web-clock-in.service
   ```

With the system services set up, the web check-in action will be triggered automatically when your computer starts, and the web check-out action will be triggered when your computer shuts down.

## Troubleshooting

- If the script fails to run, ensure that you have installed all the prerequisites and configured the `.env` file correctly.
- Check the ChromeDriver path in the `keka_script.py` file and make sure it matches your system's configuration.
- Verify that the Keka credentials and URL provided in the `.env` file are correct.
- If the system services fail to start, review the service files for any misconfigurations and ensure they are placed in the correct directory.

## License

This project is licensed under the [MIT License](LICENSE).
