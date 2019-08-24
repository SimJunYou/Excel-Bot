# Event Attendance Taking Bot (Python/Heroku)

Takes in user identification, returns assigned seating from an Excel file, and marks attendance in the Excel file.

## Getting Started

These instructions will help you get the bot up and running for your event, with custom messages and feedback questions.

### Finding the bot

Open your Telegram app and press the Search button. On Android, it is the magnifying glass symbol on the top right. On Apple, it is the Search text field on the top of the main screen.

Type in the following into the search:

```
wiipbot
```

You should find a bot named ___. Tap on the chat to enter.

### Becoming an admin

Only admins are capable of giving the bot commands, such as to download the feedback and attendance files.

To become an admin, please contact the last known admin.

### Customising the messages

Refer beneath for the instructions on how to customise the messages for your event.

## Commands
### Attendee's Commands
* Begin attendance-taking: `/seminar`
    * Runs through the attendance-taking for the event
* Begin feedback-taking: `/postevent`
    * Runs through the feedback-taking for the event
### Attendance and Feedback (requires admin)
* Attendance stats: `/aStats`
    * Gives you the total and currently registered number of participants.
* Feedback stats: `/fStats`
    * Gives you the current number of feedback responses.
* Attendance file: `/aFile`
    * Sends you the most updated Excel file for attendance.
* Feedback file: `/fFile`
    * Sends you the most updated Excel file for feedback.
### Admin Editing Commands (requires admin)
* Add new admin: `/newAdmin`
    * Lets you add a new admin by sending their contact to the bot.
* List all admins: `/listAdmins`
    * Shows you all the current admins and their phone numbers.
* Remove an admin: `/removeAdmin`
    * Lets you remove an admin.
### Message Editing Commands (requires admin)
* Change messages: `/changeText`
    * Allows you to change the text of the messages. Just follow the prompts.
    * You can do `/changeText <number>` to change the following directly:
        * 1 - Start of attendance taking
        * 2 - NRIC is not found in provided list
        * 3 - End of attendance taking
        * 4 - Start of feedback
        * 5-7 - Feedback questions 1-3
        * 8 - End of feedback

## Built With

* [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot) - API for Python interface with Telegram's official bot API
* [Redis](https://redis.io/) - Online data structure for real-time storage
* [openpyxl](https://pypi.org/project/openpyxl/) - Used to interact with the Excel files

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

