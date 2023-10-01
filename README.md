# runner_tracker_to_csv
Convert data exported from Runner Tracker Race Control to the same CSV format used by Bear100Win.exe

## Video demonstration

This video demonstrates logging a bib number with Runner Tracker, selecting all records, 
transmitting the data, viewing the data that was sent, shared to clipboard. Then in the Python app,
paste the data and retrieve the created CSV file.
[Watch the video demonstration](https://youtu.be/HfJbVxb7Csc)

## About

The point of this conversion script is to enable smartphone users (iPhone and Android) to use the
Runner Tracker Race Control app to contribute to the Bear 100 data team. It aims to create a
compatible CSV file that would be indistinguishable to the data team from CSV created by the
current Bear100Win.exe software.

## Installation Instructions
The main prerequisite is having Python3 installed. It will use modules `sys`, `csv`, `datetime`, 
and `json`. To use the `runner_tracker_to_csv` tool:

1. Clone this repository to your local machine.
2. Open a terminal or command prompt.
3. Navigate to the directory where you cloned the repository.
4. Run the script using one of the following methods:
   - From the Pydroid3 app, simply open `rt2bear100.py` and select the Run button.
   - From a command line, use the following commands:
     ```
     python3 rt2bear100.py
     ```
     or if you make it executable first:
     ```
     ./rt2bear100.py
     ```
   - It also supports data from a pipe, so you could do things like:
     ```
     cat data.txt | ./rt2bear100.py
     ```
   These commands assume your working directory is the same directory as `rt2bear100.py`.

## Runner Tracker data

Native runner tracker data is very terse. It starts with a shortened version of the Unix epoch,
which represents the time stamp of the earliest record in its dataset. That is then followed by
data for each runner, where the first digit is the bib number, the second digit is the In Time
expressed in the number of minutes since the epoch. The third number represents the Out Time in
minutes since the epoch. Notice that the In and Out times are whole minutes, not capturing the
number of seconds after the minute. If the optional fourth field is present, it signifies the
runner did not finish (DNF) at the station and the field is used to capture the reason.

Example of Runner Tracker data:
```
{"epoch":28266707}
1,0,1
40,3,,Twisted ankle
200,1,
300,,2
```

The above example is equivalent to the following CSV from Bear100Win.exe:
```
"BEAR 100 Race - 2023","Aid Station #4 - Right Hand Fork","All times are based off of the system they were recorded on"
"Sequence","X","Runner#","In Time","Out Time","Notes"
"1","","1","09:47:00 29 Sep","09:48:00 29 Sep",""
"2","","40","09:50:00 29 Sep","DNF","Twisted ankle"
"3","","200","09:48:00 29 Sep","",""
"4","","300","","09:49:00 29 Sep",""
```

## Epoch conversion

To get the real Unix epoch timestamp from Runner Tracker's shortened epoch, multiply it by 60,000. 
That's 60 for seconds and another 1000 for milliseconds. From the above example, `28266707 * 60 * 
1000 = 1696002420000 = 09:47:00 29 Sep`.

## Initial setup

The `rt2bear100.py` script has some user-definable variables. Use those to set the name and number of
your Aid Station. 

## Ways to run

1. Ideally, the Addilas software to which the data team submits the CSV files would simply accept
native Runner Tracker data. If they aren't doing that by the time you read this, the next best way
would be...
2. The data team runs the conversion themselves. That way, less technical app users could simply
transmit Runner Tracker data in its native format to the data team. That won't happen, so...
3. The way I did it at the 2023 Bear 100, which is to install the Pydroid3 app on my phone along
with `rt2bear100.py` and run the script on my own phone. It prompts for data then converts it to the
properly named CSV file (e.g., `AID04_01.csv`, `AID04_02.csv`, ...`AID04_99.csv`).

## Runner Tracker export steps

Go to the Records page, select All and Transmit. Then back on the Send / Receive page, you can click
the More button next to the sent item and click View, then click the Copy icon. 

The Copy icon isn't actually working for my device, so I use the Share icon to copy it to my
clipboard instead, which does work.

## My wish list

I would have liked to use the Share icon to select Pydroid3 to send it to `rt2bear100.py` directly,
but I don't know how to make Pydroid3 appear as a choice in the Share menu yet.

## Contact Information
For questions or inquiries, you can reach out to the project maintainer:
- Roger Brown
- Email: rogerpbrown@gmail.com

## License
This work uses the MIT License. See [LICENSE](LICENSE) in this repository for details.

