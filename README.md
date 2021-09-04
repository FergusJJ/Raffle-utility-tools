# Raffle utility tools
A tool to scrape links from email messages, also lets you generate jigged addresses.
Probably still a few bugs but I doubt I'll work on this further since it suits my needs for now, if you use it please star the repo :)
**Installation guide at the bottom**

### Tips:
**Raffle-Utility-Tools-Main\user_settings** is where you can save your addresses & emails.
You are now able to save keywords within **frequent_senders.txt** so you don't have to re-enter one every time.
> Example:
> _frequent_senders.txt_
> this_email_needs_no_keyword@email.com:keyword_here
> this_email_needs_a_keyword
If you don't specify a keyword by separating with a colon then you will be asked for one at runtime like before.



## How to install:

If you don't already have python 3 installed then install it here: [Download](https://www.python.org/downloads/)
Once you have python installed and have added pip to PATH ([How to add pip to PATH](https://appuals.com/fix-pip-is-not-recognized-as-an-internal-or-external-command/)) open up the command prompt and type in the following 2 commands:
pip install art
pip install termcolor

Now you can download the zip file and unzip it.
Open up the command prompt one more time and navigate to the folder which contains **main.py**
Type "**python main.py**" and the program will start 