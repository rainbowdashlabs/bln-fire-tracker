# BLN-Fire-Tracker

A simple python script which reads the current emergency count data from the website of the berlin [fire and rescue department](https://www.berliner-feuerwehr.de/).
The data is refreshed every minute and that's why the script checks for new numbers every minute as well

Instead of scraping the website the script uses an internal endpoint.
While scraping the website is allowed by the robots.txt the internal endpoint is forbidden.
So sadly while this script works we should not use it, because we are not evil people c:
