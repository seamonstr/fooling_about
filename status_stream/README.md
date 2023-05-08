= Status Stream

A simple method for sending a text output stream to a minimally authenticated browser.

Example use cases are for an appliance-based product that is performing OS-level
maintenance tasks while the application software is shut down; the user will want to see
what's going on, but the application's web server may not be available.

This is conceived as a "let me see what's going on on my appliance" mechanism, not as a
way to get access to the log files for archiving or troubleshooting.  As such, the UI
(and its associated API) give access to the most recent log items, but older data may no
longer be available.

To use, include the output snippet in your script file, initialise it and then write all
output to stdout as usual. 

== Architecture

The mechanism has two parts:
1. **A bash snippet** that can be imported into a larger script, providing a log
   function.  The log can write to whichever log file you specify, and to the console,
   but will also write its output to a location where it can be accessed by the web UI.
2. **A simple web UI** that allows viewing of the log. 

Both of these items are written in bash script, because that is a low-ish common
denominator technology that will be available in appliance-based products' OSes.  

=== The stdout pipe

The output functionality is implemented as a bash function that can be included and used
by the script to run on the appliance. 

The initialisation step creates a named pipe, and a subshell that reads from it.

The subshell writes all output to the stdout that it inherits from the running script.

Additionally, all output is placed into a downloadable location. This location is a
directory that the script has write access to.

The output for download will be written into chunk files. The size of the chunks is
configurable, and defaults to 10 lines. Each chunk is identified by an integer number
which forms part of the filename.

The lines will be written to an "in progress" chunk file which is rolled once the number
of lines is reached. If the in-progress chunk becomes older than 5 seconds, it will be
automatically rolled by a watcher sub-shell.

A configurable number of chunks is kept available at any one time, defaulting to 20.
This is to prevent connecting clients from having to process all of the log output from
the beginning if they connect part way through a process.

=== The web UI

The web UI comprises two parts.  

==== A web page

The web page is basic HTML file, and an associated .js script.  The js script will call
the API on a three-second polling cycle to get new log output, and display it in the web
page.

==== A web API

The API is written as a bash CGI script.

The API is invoked by the web page to get a new batch of log messages. As a parameter,
the API takes the integer identifier of the last log chunk that it recieved.


The API will then return a new batch of logs, up to ten chunks in length:
* Either the log chunk after the last chunk identified by the parameter to the API, or
* The chronologically-first chunk available. 

The data format of the batch is a JSON document formatted as: { // The ID of the last
chunk in this document. Send this ID to the API next time to get the following chunk.
    last_chunk_id = 10, lines = [ "Line1", "Line2", "Line3", "..." ] }

If fewer than ten chunks are available after the chunk identified, the API will return
all available chunks.

If no chunks are available after the chunk identified, the API will return 204 No
Content.
