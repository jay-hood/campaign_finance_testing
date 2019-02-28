# Overview
The SQL scripts in this folder are intended to be run in sequence, first creating the DB and then applying any updates needed (including structure + data changes).

**Important:** If you write any SQL scripts, make sure your scripts are **re-runnable**.  The idea here is we may have multiple copies of the DB (e.g. on developer machines) and you have no idea what state the DB is in when your script gets run.  You want to make sure your script will not blow up if it was already run once on that DB.  The general way to make a script re-runnable is to first have your code check to see if the change needs to be made.  e.g. If you are adding a column, first check to see if the column already exists. Only if it does not exist should you then add it. 

# Getting Started with MySQL
If you are developing a component on your local machine, you should install a local instance of MySQL database server on your machine, with a copy of the ElectionMoney database, to support your development work.  The following steps can be used to get that set up.
_(Note: This is just a rough draft of the installation steps, and needs to be verified/cleaned up.)_

1. Download and install [MySQL community edition](https://dev.mysql.com/downloads/mysql/) (no need to register with Oracle)
1. Run through [installation steps for MySQL server](https://dev.mysql.com/doc/refman/8.0/en/installing.html)
1. Download and install MySQL Workbench
1. Open MySQL Workbench
1. Create connection to your local MySQL server
1. In left panel, select schemas
1. Right-click and select "Creat new schema"
1. Name it "ElectionMoney", and use defaults
1. Click "Apply" to create
1. Once schema created, right-click on it and select "Make default schema'
1. In browser, go to our GitHub repo > [Db scripts folder](https://github.com/jay-hood/electionmoney/tree/master/Db/MySQL).
1. Find all of the SQL scripts in this folder (starting with "Sql_001_...") and run them in sequence.
   1. Open the script file and copy all the text out of it
   1. Back in MySQL Workbench, open a new SQL Query tab page
   1. Paste the SQL from the above script into it, and run that (click on lightening bolt)
1. Right click on the "ElectionMoney" schema (in schema panel) and select "Refresh"
1. You should now be able to drill down to see the tables for that schema (about 6 or so?)

# Q&A
### Question: What if I need to create a new table or add a new column?
*Answer:* Write up a new SQL script, with a prefix of "`SQL_<nnn>_`", where `<nnn>` is the next number in seqence after the last script.  After that prefix, the rest of the file name can be (briefly) descriptive of the change.   e.g. "`SQL_002_Add_election_type.sql`"

### Question: What if I need to make a change to an existing column (defined in a prior script)?
*Answer:*  Generally you'd still write up a new script, as described above, so that once all the scripts have been run in sequence, you wind up with the DB structure you need.  If you just edit an existing script, another developer who already ran that script might assume his DB is updated because there are no new scripts.
