# ConversationIM Database Migrations

The migration scripts and tools supporting ConversationIM are stored here.

## Initial Setup

You will need a local MySQL server (5.6.x) and the FlywayDB command-line tool (3.2.x) on your system.

#### Installing MySQL

If you are a Mac user, you should make sure to install MySQL via `brew`. The traditional MySQL installer puts components in places that do not play well with MySQL-Python, the database connector that we use.  If you are experiencing problems, check to be sure that you have followed all steps detailed in this [StackOverflow thread](http://stackoverflow.com/a/25491082/996249).

If you are a Windows, you should be able to install MySQL via the traditional installer. Of course, you might run into some problems, but we will have to troubleshoot those on a case-by-case basis.

Linux users should use the appropriate package manager to accomplish this task. Don't forget to check the package version!

#### Installing FlywayDB

FlywayDB is a Java-based migration tool. Fortunately, there are a [variety of options](http://flywaydb.org/getstarted/download.html) for getting Flyway's command-line tool onto your system.

You should choose the one that is most appropriate for you, but be sure that it is the _command-line_ tool. Note that if you already have JRE 6+ installed on your system, you can most likely pick a package that doesn't include a JRE. Indeed, if you've developed with Java before, chances are that you already have a JRE installed.

Naturally, if you have a package manager on your system, you can install flyway using that instead. Ensure that the version is correct so that we don't run into any compatibility issues.

## Schema Setup

You will need a schema called `conversationIM` present on your MySQL server in order for anything to work.

#### MySQL Visual Database Tools

If you do not have one already, you should find a visual database tool for MySQL that is compatible with your system. MySQL Workbench (Windows/Mac/Linux) and Sequel Pro (Mac) are two options.

#### Adding the Schema

Regardless of whether you or not you have installed a visual database tool, you must add the schema named above. Keep in mind that the name is case-sensitive, so creating `Conversationim` or `ConversationIM` will cause you to see plenty of errors later on.

## Running the Migrations

Once you have everything set up, you can keep your database in-sync very easily. Make sure that you have set the database-related environment variables described in the primary README, and then run the following command:

```
sh flyway.sh migrate
```

You should see Flyway run through all of the existing migrations, applying each chronologically. If an error occurs, you will see details as to what went wrong.

## New Migrations & Reverts

Since we are using the FlywayDB command-line tool, you can typically just copy-and-paste whatever SQL you used to perform your migrations locally into a migration script file. There are some things to keep in mind, however.

#### Migrations

The `migration` folder will keep track of all migrations, with each migration following this naming convention:
> [YYYYmmDD]\_[HHMM]\__[description].sql

For example, a migration that creates a new table called `foo` on 7/15/2015 at 12:00 PM might look like this:

> 20151507\_1200__createFooModel.sql

Since this is especially painful to type for every migration, use the shell script called `timestamp.sh` to generate this file name. To generate the above migration file name, run:

> sh timestamp.sh createFooModel

#### Reverts
Although FlywayDB does not have the ability to revert migrations for us, having a quick way to revert a previous migration may be useful in production hotfixes. The naming convention is exactly the same as that which is above, but should be placed in the `revert` folder, and have a `.revert.sql` ending:
> [YYYYmmDD]\_[HHMM]\__[description].revert.sql

You can typically just use the same output from the `migration.sh` script to name your revert, taking care to add the `.revert.sql` filename ending.

### Table and Column Naming
Let's have tables always represent the data that they hold collectively, that is, as a lowercase plural entity. For example, always make a table like `foos`, not like `foo` or `Foo`.

Column names should be somewhat of the opposite, just to make sure that we don't accidentally mix up column names and table names. Let's represent column
names like `Bar` or `Bar_Baz`, but not `bar` or `bar_baz`.

In any case, make sure to exchange places where spaces would normally be inserted with underscores.

### Cascading ON UPDATE/DELETE
As a reference, please read the marked answer to this [StackOverflow response](http://stackoverflow.com/questions/6720050/foreign-key-varraints-when-to-use-on-update-and-on-delete).

Overall, it's saying that you usually (but not always) want to cascade ON UPDATE. However, for ON DELETE operations, you need to really think. For
instance, if the foreign key is from a user to his/her organization, cascading on delete would be very bad -- deleting the organization would delete
the user as well!

If you're not sure which to pick, make your best guess and leave a justification with a TODO for you code reviewer to check out.
