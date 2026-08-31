---
title: init_v3_man
date: '2026-03-11'
tags:
- 进程管理
- Unix历史
aliases:
- /init_v3_man/
source: /Users/huyi/Projects/unix-history-docs/init_v3_man.md
---

INIT (VII)                    6/15/72                    INIT (VII)


NAME        init  --  process control initialization

SYNOPSIS    /etc/init

DESCRIPTION
     init is invoked inside UNIX as the last step in the boot
     procedure.  Generally its role is to create a process for
     each typewriter on which a user may log in.

     First, init checks to see if the console switches contain
     173030.  (This number is likely to vary between systems.)
     If so, the console typewriter tty is opened for reading
     and writing and the shell is invoked immediately.  This
     feature is used to bring up a test system, or one which
     does not contain DC-11 communications interfaces.  When
     the system is brought up in this way, the getty and login
     routines mentioned below and described elsewhere are not
     needed.

     Otherwise, init does some housekeeping: the mode of each
     DECtape file is changed to 17 (in case the system crashed
     during a tap command); directory /usr is mounted on the
     RK0 disk; directory /sys is mounted on the RK1 disk.
     Also a data-phone daemon is spawned to restart any jobs
     being sent.

     Then init forks several times to create a process for
     each typewriter mentioned in an internal table.  Each of
     these processes opens the appropriate typewriter for
     reading and writing.  These channels thus receive file
     descriptors 0 and 1, the standard input and output.
     Opening the typewriter will usually involve a delay,
     since the open is not completed until someone is dialled
     in (and carrier established) on the channel.  Then the
     process executes the program /etc/getty (q.v.).  Getty
     will read the user's name and invoke login (q.v.) to log
     in the user and execute the shell.

     Ultimately the shell will terminate because of an end-of-
     file either typed explicitly or generated as a result of
     hanging up.  The main path of init, which has been waiting
     for such an event, wakes up and removes the appropriate
     entry from the file utmp, which records current users, and
     makes an entry in wtmp, which maintains a history of
     logins and logouts.  Then the appropriate typewriter is
     reopened and getty reinvoked.

FILES        /dev/tap?, /dev/tty, /dev/tty?, /tmp/utmp, /tmp/wtmp

SEE ALSO    login(I), login(VII), getty(VII), sh(I), dpd(VII)

DIAGNOSTICS  none possible

BUGS         none possible
