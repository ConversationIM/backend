# Migrations

Since we are using the FlywayDB command-line tool, you can typically just copy-and-paste whatever SQL you used to perform your migrations locally into a migration script file. There are some things to keep in mind, however.

## Creating New Migrations

The `migration` folder (this folder) will keep track of all migrations, with each migration following this naming convention:
> [YYYYmmDD]\_[HHMM]\__[description].sql

For example, a migration that creates a new table called `foo` on 7/15/2015 at 12:00 PM might look like this:

> 20151507\_1200__createFooModel.sql

Since this is especially painful to type for every migration, use the shell script called `timestamp.sh`(in the db directory) to generate this file name. To generate the above migration file name, run:

> sh timestamp.sh createFooModel

## Table and Column Naming
Let's have tables always represent the data that they hold collectively, that is, as a lowercase plural entity. For example, always make a table like `foos`, not like `foo` or `Foo`.

Column names should be somewhat of the opposite, just to make sure that we don't accidentally mix up column names and table names. Let's represent column
names like `Bar` or `Bar_Baz`, but not `bar` or `bar_baz`.

In any case, make sure to exchange places where spaces would normally be inserted with underscores.

## Cascading ON UPDATE/DELETE
As a reference, please read the marked answer to this [StackOverflow response](http://stackoverflow.com/questions/6720050/foreign-key-varraints-when-to-use-on-update-and-on-delete).

Overall, it's saying that you usually (but not always) want to cascade ON UPDATE. However, for ON DELETE operations, you need to really think. For
instance, if the foreign key is from a user to his/her organization, cascading on delete would be very bad -- deleting the organization would delete
the user as well!

If you're not sure which to pick, make your best guess and leave a justification with a TODO for you code reviewer to check out.
