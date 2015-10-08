# Reverts

Although FlywayDB does not have the ability to revert migrations for us, having a quick way to revert a previous migration may be useful in production hotfixes. The naming convention is exactly the same as that which is used for migrations, but should be placed in the `revert` folder (this folder) and have a `.revert.sql` ending:
> [YYYYmmDD]\_[HHMM]\__[description].revert.sql

You can typically just use the same output from the `migration.sh` script to name your revert, taking care to add the `.revert.sql` filename ending.
