This is a little bit of scaffolding to do quick-and-dirty  server-side CI; the cron job
in bs/files/etc/cron.d runs the update script in bin/update.sh, which checks to see if
there are changes to the branch defined as ROLE at the top of the script; if there
are changes, it checks out a new copy of the repo locally and then runs the scripts
in bs/update/ in lexical order (which is why they're named NN_script.sh).


