# ConversationIM Database

The migration scripts and tools supporting ConversationIM are stored here.

## Initial Setup

You will need a local MySQL server (5.6.x) and the FlywayDB command-line tool (3.2.x) on your system.

#### Installing MySQL

If you are a Mac user, you should make sure to install MySQL via `brew`. The traditional MySQL installer puts components in places that do not play well with MySQL-Python, the database connector that we use.  If you are experiencing problems, check to be sure that you have followed all steps detailed in this [StackOverflow thread](http://stackoverflow.com/a/25491082/996249).

If you are on Windows, you should be able to install MySQL via the traditional installer. Of course, you might run into some problems, but we will have to troubleshoot those on a case-by-case basis.

Linux users should use the appropriate package manager to accomplish this task. Don't forget to check the package version!

#### Installing FlywayDB

FlywayDB is a Java-based migration tool. Fortunately, there are a [variety of options](http://flywaydb.org/getstarted/download.html) for getting Flyway's command-line tool onto your system.

You should choose the one that is most appropriate for you, but be sure that it is the _command-line_ tool. Note that if you already have JRE 6+ installed on your system, you can most likely pick a package that doesn't include a JRE. Indeed, if you've developed with Java before (or even used a Java application), chances are that you already have a JRE installed.

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

#### New Migrations

If you're creating a new migration, you should be sure to check out the [migration README](migration/README.md) and the [revert README](revert/README.md) to be sure that you are taking the correct steps.
