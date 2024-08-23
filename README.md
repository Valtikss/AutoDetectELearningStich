# Notification Script for Availability Check on Stych.fr

This Python script is designed to automate the process of checking availability on the website [Stych.fr](https://www.stych.fr) and sends an email notification if availability is found. The script uses Selenium for web automation, BeautifulSoup for parsing HTML, and the `smtplib` module to send email notifications.

## Features

- **Automated Login:** Logs into the Stych.fr website using Selenium.
- **Availability Check:** Navigates to the target page and checks for availability.
- **Email Notifications:** Sends an email notification if availability is found.
- **Scheduled Execution:** The script is scheduled to run between 8 AM and 8 PM every 30 minutes.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- `requests` module: `pip install requests`
- `beautifulsoup4` module: `pip install beautifulsoup4`
- `schedule` module: `pip install schedule`
- `selenium` module: `pip install selenium`
- ChromeDriver: [Download ChromeDriver](https://sites.google.com/chromium.org/driver/) compatible with your Chrome browser version.

## Setup

1. **Install Python Dependencies:**
   Run the following command to install the necessary Python packages:

   ```bash
   pip install requests beautifulsoup4 schedule selenium
   ```

2. **Download and Install ChromeDriver:**
   Download the ChromeDriver from the [official website](https://sites.google.com/chromium.org/driver/) and ensure it's in your system's PATH or specify the path in the script.

3. **Configure Email Notifications:**
   Update the `notify_user` function in the script with your Gmail address and an app password. To generate an app password, follow the instructions at [Google Account Security](https://myaccount.google.com/apppasswords).

   ```python
   server.login("your_email@gmail.com", "your_app_password")
   ```

4. **Update Login Credentials:**
   Replace the placeholder credentials in the script with your Stych.fr login information:

   ```python
   username_field.send_keys("your_email@example.com")
   password_field.send_keys("your_password")
   ```

## Usage

1. **Run the Script:**
   Execute the script by running:

   ```bash
   python script_name.py
   ```

2. **Automated Execution:**
   The script will automatically check the availability every 30 minutes between 8 AM and 8 PM. If an availability is found, an email will be sent to the specified recipients.

## Customization

- **Change the Frequency:**
  To change the frequency of checks, modify the line:

  ```python
  schedule.every(30).minutes.do(job)
  ```

  You can adjust the interval as needed.

- **Update Email Recipients:**
  Add or change the recipients of the email notification by updating the `recipients` list:

  ```python
  recipients = ["recipient1@example.com", "recipient2@example.com"]
  ```

## Notes

- Ensure that the credentials and app passwords are kept secure and not shared publicly.
- The script is configured to run in a headless mode, which means it will not open a visible browser window.

## Troubleshooting

- **WebDriver Errors:** Ensure that your ChromeDriver version matches your installed version of Chrome.
- **Login Issues:** Double-check your Stych.fr login credentials.
- **Email Delivery Issues:** Verify that you have correctly set up the Gmail app password and that your email settings allow for less secure apps or app passwords.

## License

This project is open-source and available under the MIT License.