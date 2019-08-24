# Redesign Seminar Attendance Taking Bot (Python/Heroku)

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

Only admins are capable of giving the bot admin commands, such as to download the feedback and attendance files.

To become an admin, please contact the last known admin.

### Customising the messages

Refer beneath for the instructions on how to customise the messages for your event.

## Commands

### Attendance and Feedback
* Attendance stats: `/aStats`
    * Gives you the total and currently registered number of participants.
* Feedback stats: `/fStats`
    * Gives you the current number of feedback responses.
* Attendance file: `/aFile`
    * Sends you the most updated Excel file for attendance.
* Feedback file: `/fFile`
    * Sends you the most updated Excel file for feedback.
### Admin Editing Commands
* Add new admin: `/newAdmin`
    * Lets you add a new admin by sending their contact to the bot.
* List all admins: `/listAdmins`
    * Shows you all the current admins and their phone numbers.
* Remove an admin: `/removeAdmin`
    * Lets you remove an admin.
### Admin Editing Commands
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

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
