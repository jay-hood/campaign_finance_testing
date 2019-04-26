# DB Upgrade Utility
## Motivation for utility

1. **Secure access to DDL changes.**  Security will be very important for this project, to limit the access of unauthorized parties to the database, and one important way to do this is to carefully limit the permissions given out regarding the DB.  One important permission is DDL access (Data Definition Language) statements that fundamentally change the DB structure:  CREATE, ALTER, and DROP.
The only time DDL should be used is when authorized, controlled DB upgrade scripts are being applied.  Given that, we'd like to have a utility defined which applies DB upgrade scripts to the database (incremental updates, such as adding a table/column), and ensure that all DDL changes are made using this DB upgrade utility. Then we could have this utility run under a service identify that has DDL permission, and other users would be limited to READ/WRITE/DML permissions, as appropriate.

2. **Minimize risk of accidental changes.**  By routing DDL changes through a defined process with SQL scripts and a DB upgrade utility, we reduce the footprint for DDL changes to the database, thus minimizing the risk of unintended changes.

## Overview
Although the details will vary, here's the general recipe for a DB Upgrade Utility.
1. All DB upgrades (DDL) handled through SQL scripts (probably stored in a GitHub repo, but other options are possible).  The first SQL script for the baseline for the database, creating the primary tables.  Additional scripts represent incremental delta changes (e.g. adding tables, adding columns, increasing column widths, etc.)  Anytime a change is needed to the DB structure, the DDL is written as a SQL script that can be applied to the DB, to make that change.
1. The SQL scripts should follow a naming convention that clearly indicates their sequence, e.g.  
   1. SQL_update_001_Baseline.sql
   1. SQL_update_002_Add_contributors_table.sql
   1. SQL_update_003_Rename_Cntributes_table_to_Donors.sql
   1. ...and so on...
1. Database upgrades will be applied to the DB as part of the same delivery pipeline as code, so when an application update is deployed, it will include both code and DB upgrades. 
1. The DB upgrades will be handled by running a DB Upgrade Utility, which will pull the latest copies of the DB upgrade scripts, determine which ones need to be run, and automatically run them.
1. The DB should contain a "versions" table, where every row in the table represents an incremental update to the DB, identified by a single SQL script.
   1. Version table should include at least the following info:  Script name, version #, date/time applied, hash of script at the time it was applied.

## Options to Consider
1. Use a hash to identify if the script has changed, and re-apply if so?  This would allow us the option of fixing a script that has a problem.  (Should be rare, but possible.)

## Limitations / Exclusions
1. This story only involves the creation of the utility, which should be callable independently.  It does not include fitting it into the deployment pipeline.  The description above (deploying Db updates in conjunction with code updates) is given simply to provide context, to help people see how the DB utility will be used.  A separate story will be needed to fit this utility into the deployment process.
