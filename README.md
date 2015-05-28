[![Build Status](https://travis-ci.org/nlindblad/ocarina.svg?branch=master)](https://travis-ci.org/nlindblad/ocarina)

ocarina
=====

Drop in script scheduling for Python.

### Dependencies

Only uses Python standard libraries. Developed using Python 2.7.6.

Optionally [pushnotify](https://pypi.python.org/pypi/pushnotify/0.5.1) is required for push notifications.

### Installation

    git clone https://github.com/nlindblad/ocarina.git
    cd ocarina
    cp config/main-example.ini config/main.ini

Edit ```config/main.ini```. Add the following crontab:

    0 * * * * bin/ocarina.py

### What is it?

Ocarina (named after the Ocarina of **Time**) is a simple way of scheduling Python scripts without having to constantly add and update crontab entries. It also supports scheduling not possible with cron, such as ```isClosestBankDay(day)```.

Instead, the main program ```bin/ocarina.py``` is scheduled to be run every hour through cron:

    0 * * * * bin/ocarina.py

When executed, Ocarina will traverse the ```chords``` directory and look for any Python scripts it can find.

Each script (or chord) should follow the format:

    def shouldRun(now):
        return now.isWeekDay() and now.hour == 11

    def main():
        print "It is 11 AM on a week day!"

The above script would run each weekday at 11 AM.

The ``Now`` class implements the following helper methods:

    isDay(day_name)
    isDaily()
    isWeekly()
    isMonthly()
    isHourly()
    isWeekDay()
    isWeekend()
    isMorning()
    isMidnight()
    isEvening()
    isWorkingHours()
    isClosestBankDay(day)

### Why?

During my final semester at universtiy and the following summer, I found myself enjoying tinkering with life stats from various sources such as Stackoverflow, Good Reads, Twitter, LinkedIn and [reverse engineering the API for Jawbone Up](https://niklaslindblad.se/2013/07/jawbone-up-api-updates/).

A common pattern emerged for the type of scripts:

 * Find a good interval (bi-daily, hourly, weekly, etc.)
 * Retrieve data and perform some post-processing
 * Act on the data (e.g. store it or report it)

My crontab quickly became cluttered and I felt the need for something simpler that was also easier to debug and maintain.

The breeze of adding a new script for scheduling (just implementing ```shouldRun(now)``` and ```main()```) has also made coding repeating jobs more fun. Adding a script that parses the menu for the canteen at work and sends me a digest with my favourite dishes highlighted suddenly became a 10 minute task.

### What is it not?

Ocarina runs all scripts in sequence (that may change in future versions) and due to the overhead of the traversing and evaluation of ```shouldRun(now)``` on **every** script, the trade-off is houly granuality. In other words, the test script above will not run at exactly 11:00 AM, but a bit delayed.

If you need finer control over at what time your scripts are running, Ocarina might not be for you.

### Debugging

The option ```--debug``` makes Ocarina. Consider our test script above, placed in ```chords/test.py```:

    ./bin/ocarina.py --debug

would output:

    2014-03-16 13:41:05,232 - ocarina - DEBUG - Using Python 2.7.6
    2014-03-16 13:41:05,236 - ocarina - DEBUG - Looking for chords in /home/ocarina/chords
    2014-03-16 13:41:05,237 - ocarina - DEBUG - Adding /home/ocarina/chords to path
    2014-03-16 13:41:05,238 - ocarina - DEBUG - Found chord test.py
    2014-03-16 13:41:05,299 - ocarina - DEBUG - Considering whether to run test
    2014-03-16 13:41:05,299 - ocarina - DEBUG - shouldRun() returned False

since the time was 13:41 on a Sunday.

By using the ```--tweak <TIME>``` option we can run Ocarina as if it had been invoked at a specific time:

    ./bin/ocarina.py --debug --tweak "2014-03-17 11:00:00"

would output:

    2014-03-16 13:46:33,642 - ocarina - DEBUG - Using Python 2.7.6
    2014-03-16 13:46:33,647 - ocarina - DEBUG - Applied tweak
    2014-03-16 13:46:33,647 - ocarina - DEBUG - Looking for chords in /home/ocarina/chords
    2014-03-16 13:46:33,647 - ocarina - DEBUG - Adding /home/ocarina/chords to path
    2014-03-16 13:46:33,647 - ocarina - DEBUG - Found chord test.py
    2014-03-16 13:46:33,647 - ocarina - DEBUG - Considering whether to run test
    2014-03-16 13:46:33,647 - ocarina - DEBUG - shouldRun() returned True
    2014-03-16 13:46:33,647 - ocarina - DEBUG - Running main method on test
    It is 11 AM on a week day!

### Built-in notifications targets

By importing ```core.report```, each script can notify the user(s) through different means.

#### Push notifications
Requires [pushnotify](https://pypi.python.org/pypi/pushnotify/0.5.1).

    core.report.sendNotification(application, description, event)

#### E-mail
Uses the built-in smtplib to send HTML e-mails.

    core.report.sendMail(recipients, subject, body)

#### Graphite
[Graphite](http://graphite.wikidot.com/) is a highly scalable metrics data store that supports graphing and time series analysis.

    core.report.sendToGraphite(path, value)

### License

Licensed under the [MIT License](http://opensource.org/licenses/MIT), see MIT-LICENSE.txt.
