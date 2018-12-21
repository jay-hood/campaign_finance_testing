# Overview
The SQL scripts in this folder are intended to be run in sequence, first creating the DB and then applying any updates needed (including structure + data changes).

**Important:** If you write any SQL scripts, make sure your scripts are **re-runnable**.  The idea here is we may have multiple copies of the DB (e.g. on developer machines) and you have no idea what state the DB is in when your script gets run.  You want to make sure your script will not blow up if it was already run once on that DB.  The general way to make a script re-runnable is to first have your code check to see if the change needs to be made.  e.g. If you are adding a column, first check to see if the column already exists. Only if it does not exist should you then add it. 

# Q&A
### Question: What if I need to create a new table or add a new column?
*Answer:* Write up a new SQL script, with a prefix of "`SQL_<nnn>_`", where `<nnn>` is the next number in seqence after the last script.  After that prefix, the rest of the file name can be (briefly) descriptive of the change.   e.g. "`SQL_002_Add_election_type.sql`"

### Question: What if I need to make a change to an existing column (defined in a prior script)?
*Answer:*  Generally you'd still write up a new script, as described above, so that once all the scripts have been run in sequence, you wind up with the DB structure you need.
