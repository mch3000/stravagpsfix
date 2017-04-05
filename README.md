# stravagpsfix
A very simple script to fix some gps time errors in Strava files. Initially mentioned in a post on the Strava support page:
https://support.strava.com/hc/en-us/articles/216942247-How-to-Fix-GPX-File-Errors

Original post:

I thought I'd share my problems, and how I fixed them. I hope this helps anyone else having trouble uploading their activities.

Every now and then, one of my runs wouldn't upload - the automatic sync (from my android phone) would fail, and the manual upload would give an error.

After exporting the file (to a .gpx on the sd card), transferring it to my computer, and studying it with a text editor, I realised there were problems with the times recorded:

 

1) some data points had incorrectly formatted times, eg:

(WRONG) <time>2013-01-15T08:015:52.822Z</time>  instead of:

(RIGHT) <time>2013-01-15T08:15:52.822Z</time>  (the extra character causes the time to be invalid)

2) the time itself would occasionally jump forward or backwards by anywhere from 30 seconds to 2 hours, which causes problems.

e.g. the times for successive points would be something like this:

<time>2013-01-15T08:15:36.822Z</time>
<time>2013-01-15T07:29:06.822Z</time>
<time>2013-01-15T08:15:38.822Z</time>

I fixed these errors by simply deleting any entry with an incorrect time. After doing this, the manual upload worked. Of course, the hard part is finding all the errors. I used this tool to find invalid XML entries: http://www.validome.org/xml/validate/

I then wrote a python program that read in the gpx file, and checked all the times, deleting any entries that were more than a few seconds different from the surrounding ones. I have put the code here: http://pastebin.com/LbTFXJ00

The cause of this problem is almost certainly my dodgy phone going crazy when recording times.
