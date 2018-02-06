Davinci Resolve PostgreSQL Database backup utility.

Run the script on the PostgreSQL server. It is possible to run the script on any host on the network with properly configured .pgpass file.

The script supports Windows, OS X, and Linux versions of Resolve.

Known Issues

A .pgpass configuration file leftover from another PostgreSQL user may not contain the necessary information for this script to function. In that case you can either delete the existing .pgpass or combine it with 127.0.0.1:5432:*:dbUser:dbPassword.

Resolve's database dumps are not OS portable between Windows and Mac. I have inconclusive evidence it's possible to restore the Windows dump into Linux. I'm not sure if Mac and Linux dumps are OS portable. I have a feeling some Windows specific encoding may be the culprit.
