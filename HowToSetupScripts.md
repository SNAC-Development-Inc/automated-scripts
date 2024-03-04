# Setup Cron Job and PMSet

- crontab, this runs a shell script at a certain time

  - `crontab -e`
  - replace PATH_TO_APPLESCRIPT in the following line
  - press `i` enter the following in the editor `0 6 * * * PATH_TO_APPLESCRIPT` to set the computer to run this script everyday at 6am, computer should be on central time or update the time to 6am CT in the time current zone

- pmset, tells your computer to wake up at a given time
  - enter in the terminal:
  - `sudo pmset repeat wake MTWRFSU 5:50:00` to set your computer to wake at 5:50am CT everyday to run the cron job

# Scripts

- getTextAndNumbers.py
  1. Gets and parses the text in Weather Texts: Historical Texts, to get the first text to send
  2. Gets the phone numbers from the first column from both Sheet1 and Sheet2 in the google sheet Weather Text // Master
  3. Runs the twilio python script (twilioScript.py) shortening the text message to 150 characters and sends the message to the phone numbers in the participants.csv file.
- getAndSendTextMessage.applescript
  1. Runs the getTextAndNumbers.py script and then sends the text to the phone numbers via iMessage + SMS
