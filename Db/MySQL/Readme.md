# Overview
The SQL scripts in this folder are intended to be run in sequence, first creating the DB and then applying any updates needed (including structure + data changes).

# Q&A
### Question: What if I need to create a new table or add a new column?
*Answer:* Write up a new SQL script, with a prefix of "SQL_nnn...", where <nnn> is the next number in seqence after the last script.

### Question: What if I need to make a change to an existing column (defined in a prior script)?
*Answer:*  Generally you'd still write up a new script, as described above, so that once all the scripts have been run in sequence, you wind up with the DB structure you need.
