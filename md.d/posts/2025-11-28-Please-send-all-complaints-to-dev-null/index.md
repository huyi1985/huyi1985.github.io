---
title: Please send all complaints to /dev/null
date: '2025-11-28'
---

Game

https://en.wikipedia.org/wiki/Vampire:_The_Masquerade_%E2%80%93_Redemption

# Please send all complaints to /dev/null

## How a nerd joke let to a computer science info nugget.
https://medium.com/@ishitasinha/please-send-all-complaints-to-dev-null-557e3fb3b40e

I was recently in conversation with my friend who works mostly on bash scripting and with the ongoing corona crisis, he decided to dye his hair hot pink. Following was the caption to the picture he posted on instagram — “Please send all complaints to /dev/null”.

Being a computer engineer myself, I was still bewildered by this joke and I started researching what exactly is /dev/null. This came from a very weird place of wanting to be accepted on instagram but Hey, knowledge is knowledge!

## Get Ishita Sinha’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

So here is what the line means:

1. It is used in UNIX and UNIX like systems to refer to an unbuffered virtual device or a special file.
2. It is used to dispose of unwanted output streams. Think of it as a black hole for output streams which when written to it, are discarded forever and never seen again.
3. It is also used to empty a file and only have the file with EOF character.
4. The file size is always 0 and created time is the same as boot time.
5. You can use it with the redirection operation ‘>’ as follows:

![](img1.png)

Example Code

So that’s it folks, hope it helps you to understand all future /dev/null jokes like the one below taken from [https://wiki.c2.com/?DevNull](https://wiki.c2.com/?DevNull=)

Press enter or click to view image in full size

![](img2.webp)

## Wikipedia

# Null device

From Wikipedia, the free encyclopedia

For the electropop band, see [Null Device](https://en.wikipedia.org/wiki/Null_Device "Null Device").

Not to be confused with [/dev/zero](https://en.wikipedia.org/wiki//dev/zero "/dev/zero").

In some [operating systems](https://en.wikipedia.org/wiki/Operating_system "Operating system"), the **null device** is a [device file](https://en.wikipedia.org/wiki/Device_file "Device file") that discards all data written to it but reports that the write operation succeeded. This device is called `/dev/null` on [Unix](https://en.wikipedia.org/wiki/Unix "Unix") and [Unix-like](https://en.wikipedia.org/wiki/Unix-like "Unix-like") systems, `NUL:` (see [TOPS-20](https://en.wikipedia.org/wiki/TOPS-20 "TOPS-20")) or `NUL` on [CP/M](https://en.wikipedia.org/wiki/CP/M "CP/M") and [DOS](https://en.wikipedia.org/wiki/DOS "DOS") (internally `\DEV\NUL`), `nul` on [OS/2](https://en.wikipedia.org/wiki/OS/2 "OS/2") and newer [Windows](https://en.wikipedia.org/wiki/Windows "Windows") systems[[1]](https://en.wikipedia.org/wiki/Null_device#cite_note-1) (internally `\Device\Null` on [Windows NT](https://en.wikipedia.org/wiki/Windows_NT "Windows NT")), `NIL:` on [Amiga](https://en.wikipedia.org/wiki/Amiga "Amiga") operating systems,[[2]](https://en.wikipedia.org/wiki/Null_device#cite_note-2) and `NL:` on [OpenVMS](https://en.wikipedia.org/wiki/OpenVMS "OpenVMS").[[3]](https://en.wikipedia.org/wiki/Null_device#cite_note-3) In [Windows Powershell](https://en.wikipedia.org/wiki/Windows_Powershell "Windows Powershell"), the equivalent is `$null`.[[4]](https://en.wikipedia.org/wiki/Null_device#cite_note-4) It provides no data to any [process](https://en.wikipedia.org/wiki/Process_\(computing\) "Process (computing)") that reads from it, yielding [EOF](https://en.wikipedia.org/wiki/End-of-file "End-of-file") immediately.[[5]](https://en.wikipedia.org/wiki/Null_device#cite_note-uxman-5) In IBM operating systems [DOS/360 and successors](https://en.wikipedia.org/wiki/DOS/360_and_successors "DOS/360 and successors")[[a]](https://en.wikipedia.org/wiki/Null_device#cite_note-6) and also in [OS/360 and successors](https://en.wikipedia.org/wiki/OS/360_and_successors "OS/360 and successors")[[b]](https://en.wikipedia.org/wiki/Null_device#cite_note-7) such files would be assigned in [JCL](https://en.wikipedia.org/wiki/Job_control_language "Job control language") to `DD DUMMY`.

In programmer jargon, especially Unix jargon, it may also be called the [bit bucket](https://en.wikipedia.org/wiki/Bit_bucket "Bit bucket")[[6]](https://en.wikipedia.org/wiki/Null_device#cite_note-8) or [black hole](https://en.wikipedia.org/wiki/Black_hole_\(networking\) "Black hole (networking)").

## History

/dev/null is described as an empty regular file in [Version 4 Unix](https://en.wikipedia.org/wiki/Version_4_Unix "Version 4 Unix").[[7]](https://en.wikipedia.org/wiki/Null_device#cite_note-9)

The [Version 5 Unix](https://en.wikipedia.org/wiki/Version_5_Unix "Version 5 Unix") manual describes a /dev/null device with modern semantics.[[8]](https://en.wikipedia.org/wiki/Null_device#cite_note-10)

## Usage

The null device is typically used for disposing of unwanted output [streams](https://en.wikipedia.org/wiki/Stream_\(computing\) "Stream (computing)") of a process, or as a convenient empty [file](https://en.wikipedia.org/wiki/Computer_file "Computer file") for input streams. This is usually done by [redirection](https://en.wikipedia.org/wiki/Redirection_\(computing\) "Redirection (computing)"). For example, `tar -c -f /dev/null "example directory"` can be used to dry-run the [TAR file archiving utility](https://en.wikipedia.org/wiki/Tar_\(computing\) "Tar (computing)") to see if any errors would occur but without writing any file.

The `/dev/null` device is a [special file](https://en.wikipedia.org/wiki/Device_file#Character_devices "Device file"), not a [directory](https://en.wikipedia.org/wiki/Directory_\(file_systems\) "Directory (file systems)"), so one cannot move a whole file or directory into it with the Unix `[mv](https://en.wikipedia.org/wiki/Mv_\(Unix\) "Mv (Unix)")` command.

`[cat](https://en.wikipedia.org/wiki/Cat_\(command\) "Cat (command)") /dev/null` may be replaced with `[:](https://en.wikipedia.org/wiki/True_and_false_\(commands\)#Null_smileys "True and false (commands)")`

## References in computer culture

This entity is a common inspiration for technical [jargon](https://en.wikipedia.org/wiki/Jargon "Jargon") expressions and [metaphors](https://en.wikipedia.org/wiki/Metaphor "Metaphor") by Unix programmers, e.g. "please send complaints to `/dev/null`", "my mail got archived in `/dev/null`", and "redirect to `/dev/null`"—being jocular ways of saying, respectively: "don't bother sending complaints", "my mail was deleted", and "go away". The [iPhone Dev Team](https://en.wikipedia.org/wiki/IPhone_Dev_Team "IPhone Dev Team") commonly uses the phrase "send donations to `/dev/null`", meaning they do not accept donations.[[9]](https://en.wikipedia.org/wiki/Null_device#cite_note-11) The fictitious person name "Dave (or Devin) Null" is sometimes similarly used (e.g., "send complaints to Dave Null").[[10]](https://en.wikipedia.org/wiki/Null_device#cite_note-Goodman_2004_p._170-12) In 1996, [Dev Null](https://en.wikipedia.org/wiki/Dev_Null "Dev Null") was an animated [virtual reality](https://en.wikipedia.org/wiki/Virtual_reality "Virtual reality") character created by [Leo Laporte](https://en.wikipedia.org/wiki/Leo_Laporte "Leo Laporte") for MSNBC's computer and technology TV series _[The Site](https://en.wikipedia.org/wiki/The_Site "The Site")_. Dev/null is also the name of a vampire hacker in the computer game [Vampire: The Masquerade – Redemption](https://en.wikipedia.org/wiki/Vampire:_The_Masquerade_%E2%80%93_Redemption "Vampire: The Masquerade – Redemption"). A 2002 advertisement for the Titanium [PowerBook G4](https://en.wikipedia.org/wiki/PowerBook_G4 "PowerBook G4") reads "Sends other UNIX boxes to /dev/null."[[11]](https://en.wikipedia.org/wiki/Null_device#cite_note-macnn-13)

The null device is also a favorite subject of technical jokes,[[12]](https://en.wikipedia.org/wiki/Null_device#cite_note-14) such as warning users that the system's `/dev/null` is already 98% full. The 1995 [April Fool's](https://en.wikipedia.org/wiki/April_Fools%27_Day "April Fools' Day") issue of the [German](https://en.wikipedia.org/wiki/Germany "Germany") magazine _[c't](https://en.wikipedia.org/wiki/C%27t "C't")_ reported on an enhanced `/dev/null` [chip](https://en.wikipedia.org/wiki/Integrated_circuit "Integrated circuit") that would [efficiently dispose](https://en.wikipedia.org/wiki/Entropy "Entropy") of the incoming data by converting it to a flicker on an internal glowing [LED](https://en.wikipedia.org/wiki/Light-emitting_diode "Light-emitting diode").

Dev/Null is also the name of an electronic dance music producer and jungle DJ.[[13]](https://en.wikipedia.org/wiki/Null_device#cite_note-15)


# Null device

From Wikipedia, the free encyclopedia

For the electropop band, see [Null Device](https://en.wikipedia.org/wiki/Null_Device "Null Device").

Not to be confused with [/dev/zero](https://en.wikipedia.org/wiki//dev/zero "/dev/zero").

In some [operating systems](https://en.wikipedia.org/wiki/Operating_system "Operating system"), the **null device** is a [device file](https://en.wikipedia.org/wiki/Device_file "Device file") that discards all data written to it but reports that the write operation succeeded. This device is called `/dev/null` on [Unix](https://en.wikipedia.org/wiki/Unix "Unix") and [Unix-like](https://en.wikipedia.org/wiki/Unix-like "Unix-like") systems, `NUL:` (see [TOPS-20](https://en.wikipedia.org/wiki/TOPS-20 "TOPS-20")) or `NUL` on [CP/M](https://en.wikipedia.org/wiki/CP/M "CP/M") and [DOS](https://en.wikipedia.org/wiki/DOS "DOS") (internally `\DEV\NUL`), `nul` on [OS/2](https://en.wikipedia.org/wiki/OS/2 "OS/2") and newer [Windows](https://en.wikipedia.org/wiki/Windows "Windows") systems[[1]](https://en.wikipedia.org/wiki/Null_device?utm_source=chatgpt.com#cite_note-1) (internally `\Device\Null` on [Windows NT](https://en.wikipedia.org/wiki/Windows_NT "Windows NT")), `NIL:` on [Amiga](https://en.wikipedia.org/wiki/Amiga "Amiga") operating systems,[[2]](https://en.wikipedia.org/wiki/Null_device?utm_source=chatgpt.com#cite_note-2) and `NL:` on [OpenVMS](https://en.wikipedia.org/wiki/OpenVMS "OpenVMS").[[3]](https://en.wikipedia.org/wiki/Null_device?utm_source=chatgpt.com#cite_note-3) In [Windows Powershell](https://en.wikipedia.org/wiki/Windows_Powershell "Windows Powershell"), the equivalent is `$null`.[[4]](https://en.wikipedia.org/wiki/Null_device?utm_source=chatgpt.com#cite_note-4) It provides no data to any [process](https://en.wikipedia.org/wiki/Process_\(computing\) "Process (computing)") that reads from it, yielding [EOF](https://en.wikipedia.org/wiki/End-of-file "End-of-file") immediately.[[5]](https://en.wikipedia.org/wiki/Null_device?utm_source=chatgpt.com#cite_note-uxman-5) In IBM operating systems [DOS/360 and successors](https://en.wikipedia.org/wiki/DOS/360_and_successors "DOS/360 and successors")[[a]](https://en.wikipedia.org/wiki/Null_device?utm_source=chatgpt.com#cite_note-6) and also in [OS/360 and successors](https://en.wikipedia.org/wiki/OS/360_and_successors "OS/360 and successors")[[b]](https://en.wikipedia.org/wiki/Null_device?utm_source=chatgpt.com#cite_note-7) such files would be assigned in [JCL](https://en.wikipedia.org/wiki/Job_control_language "Job control language") to `DD DUMMY`.

In programmer jargon, especially Unix jargon, it may also be called the [bit bucket](https://en.wikipedia.org/wiki/Bit_bucket "Bit bucket")[[6]](https://en.wikipedia.org/wiki/Null_device?utm_source=chatgpt.com#cite_note-8) or [black hole](https://en.wikipedia.org/wiki/Black_hole_\(networking\) "Black hole (networking)").

## History

/dev/null is described as an empty regular file in [Version 4 Unix](https://en.wikipedia.org/wiki/Version_4_Unix "Version 4 Unix").[[7]](https://en.wikipedia.org/wiki/Null_device?utm_source=chatgpt.com#cite_note-9)

The [Version 5 Unix](https://en.wikipedia.org/wiki/Version_5_Unix "Version 5 Unix") manual describes a /dev/null device with modern semantics.[[8]](https://en.wikipedia.org/wiki/Null_device?utm_source=chatgpt.com#cite_note-10)

## Usage

The null device is typically used for disposing of unwanted output [streams](https://en.wikipedia.org/wiki/Stream_\(computing\) "Stream (computing)") of a process, or as a convenient empty [file](https://en.wikipedia.org/wiki/Computer_file "Computer file") for input streams. This is usually done by [redirection](https://en.wikipedia.org/wiki/Redirection_\(computing\) "Redirection (computing)"). For example, `tar -c -f /dev/null "example directory"` can be used to dry-run the [TAR file archiving utility](https://en.wikipedia.org/wiki/Tar_\(computing\) "Tar (computing)") to see if any errors would occur but without writing any file.

The `/dev/null` device is a [special file](https://en.wikipedia.org/wiki/Device_file#Character_devices "Device file"), not a [directory](https://en.wikipedia.org/wiki/Directory_\(file_systems\) "Directory (file systems)"), so one cannot move a whole file or directory into it with the Unix `[mv](https://en.wikipedia.org/wiki/Mv_\(Unix\) "Mv (Unix)")` command.

`[cat](https://en.wikipedia.org/wiki/Cat_\(command\) "Cat (command)") /dev/null` may be replaced with `[:](https://en.wikipedia.org/wiki/True_and_false_\(commands\)#Null_smileys "True and false (commands)")`

## References in computer culture

This entity is a common inspiration for technical [jargon](https://en.wikipedia.org/wiki/Jargon "Jargon") expressions and [metaphors](https://en.wikipedia.org/wiki/Metaphor "Metaphor") by Unix programmers, e.g. "please send complaints to `/dev/null`", "my mail got archived in `/dev/null`", and "redirect to `/dev/null`"—being jocular ways of saying, respectively: "don't bother sending complaints", "my mail was deleted", and "go away". The [iPhone Dev Team](https://en.wikipedia.org/wiki/IPhone_Dev_Team "IPhone Dev Team") commonly uses the phrase "send donations to `/dev/null`", meaning they do not accept donations.[[9]](https://en.wikipedia.org/wiki/Null_device?utm_source=chatgpt.com#cite_note-11) The fictitious person name "Dave (or Devin) Null" is sometimes similarly used (e.g., "send complaints to Dave Null").[[10]](https://en.wikipedia.org/wiki/Null_device?utm_source=chatgpt.com#cite_note-Goodman_2004_p._170-12) In 1996, [Dev Null](https://en.wikipedia.org/wiki/Dev_Null "Dev Null") was an animated [virtual reality](https://en.wikipedia.org/wiki/Virtual_reality "Virtual reality") character created by [Leo Laporte](https://en.wikipedia.org/wiki/Leo_Laporte "Leo Laporte") for MSNBC's computer and technology TV series _[The Site](https://en.wikipedia.org/wiki/The_Site "The Site")_. Dev/null is also the name of a vampire hacker in the computer game [Vampire: The Masquerade – Redemption](https://en.wikipedia.org/wiki/Vampire:_The_Masquerade_%E2%80%93_Redemption "Vampire: The Masquerade – Redemption"). A 2002 advertisement for the Titanium [PowerBook G4](https://en.wikipedia.org/wiki/PowerBook_G4 "PowerBook G4") reads "Sends other UNIX boxes to /dev/null."[[11]](https://en.wikipedia.org/wiki/Null_device?utm_source=chatgpt.com#cite_note-macnn-13)

The null device is also a favorite subject of technical jokes,[[12]](https://en.wikipedia.org/wiki/Null_device?utm_source=chatgpt.com#cite_note-14) such as warning users that the system's `/dev/null` is already 98% full. The 1995 [April Fool's](https://en.wikipedia.org/wiki/April_Fools%27_Day "April Fools' Day") issue of the [German](https://en.wikipedia.org/wiki/Germany "Germany") magazine _[c't](https://en.wikipedia.org/wiki/C%27t "C't")_ reported on an enhanced `/dev/null` [chip](https://en.wikipedia.org/wiki/Integrated_circuit "Integrated circuit") that would [efficiently dispose](https://en.wikipedia.org/wiki/Entropy "Entropy") of the incoming data by converting it to a flicker on an internal glowing [LED](https://en.wikipedia.org/wiki/Light-emitting_diode "Light-emitting diode").

Dev/Null is also the name of an electronic dance music producer and jungle DJ.[[13]](https://en.wikipedia.org/wiki/Null_device?utm_source=chatgpt.com#cite_note-15)


# [Why was /dev/null called that?](https://unix.stackexchange.com/questions/332906/why-was-dev-null-called-that)

Asked 8 years, 11 months ago

Modified [3 years, 4 months ago](https://unix.stackexchange.com/questions/332906/why-was-dev-null-called-that?lastactivity "2022-07-22 16:27:21Z")

Viewed 920 times

12

[](https://unix.stackexchange.com/posts/332906/timeline)

I'm looking for some historic info about the null device. Why was it called `/dev/null` instead of (for example) `/dev/empty`?

[FreeBSD's manual page](https://www.freebsd.org/cgi/man.cgi?null\(4\)) states that "A null device appeared in Version 7 AT&T UNIX" but I can't find any reference or hint about why that name was originally chosen.

If it turns out that the name was originally used in a more ancient OS, I'd like to know how the original device worked and why _that_ name was chosen.

- [devices](https://unix.stackexchange.com/questions/tagged/devices "show questions tagged 'devices'")
- [history](https://unix.stackexchange.com/questions/tagged/history "show questions tagged 'history'")

[Share](https://unix.stackexchange.com/q/332906/316247 "Short permalink to this question")

[Edit](https://unix.stackexchange.com/posts/332906/edit "Revise and improve this post")

Follow

Flag

[edited Dec 30, 2016 at 21:39](https://unix.stackexchange.com/posts/332906/revisions "show all edits to this post")

[

![Michael Homer's user avatar](img3.png)

](https://unix.stackexchange.com/users/73093/michael-homer)

[Michael Homer](https://unix.stackexchange.com/users/73093/michael-homer)

78.9k1717 gold badges221221 silver badges239239 bronze badges

asked Dec 26, 2016 at 22:18

[

![Giacomo Tesio's user avatar](img4.png)

](https://unix.stackexchange.com/users/301/giacomo-tesio)

[Giacomo Tesio](https://unix.stackexchange.com/users/301/giacomo-tesio)

98511 gold badge99 silver badges1919 bronze badges

- [](https://unix.stackexchange.com/questions/332906/why-was-dev-null-called-that?utm_source=chatgpt.com# "This comment adds something useful to the post")
    
    `/dev/null` is one of very few pathnames standardized by POSIX. And [even non-Unix-like systems call it that way](https://en.wikipedia.org/wiki/Null_device) (probably because Unix did it first). 
    
    – [Gilles 'SO- stop being evil'](https://unix.stackexchange.com/users/885/gilles-so-stop-being-evil "866,012 reputation")
    
     [CommentedDec 26, 2016 at 22:59](https://unix.stackexchange.com/questions/332906/why-was-dev-null-called-that?utm_source=chatgpt.com#comment586078_332906) 
    
- 1
    
    [](https://unix.stackexchange.com/questions/332906/why-was-dev-null-called-that?utm_source=chatgpt.com# "This comment adds something useful to the post")
    
    @Gilles ok but why? What the history behind this specific name? 
    
    – [Giacomo Tesio](https://unix.stackexchange.com/users/301/giacomo-tesio "985 reputation")
    
     [CommentedDec 27, 2016 at 14:42](https://unix.stackexchange.com/questions/332906/why-was-dev-null-called-that?utm_source=chatgpt.com#comment586330_332906)
    
- 2
    
    [](https://unix.stackexchange.com/questions/332906/why-was-dev-null-called-that?utm_source=chatgpt.com# "This comment adds something useful to the post")
    
    I've removed everything except the core question itself from here in the hope that that makes it clearer as a historical question; if I've interfered with what you wanted it to say please roll it back. 
    
    – [Michael Homer](https://unix.stackexchange.com/users/73093/michael-homer "78,928 reputation")
    
     [CommentedDec 30, 2016 at 21:40](https://unix.stackexchange.com/questions/332906/why-was-dev-null-called-that?utm_source=chatgpt.com#comment588006_332906)
    
- 2
    
    [](https://unix.stackexchange.com/questions/332906/why-was-dev-null-called-that?utm_source=chatgpt.com# "This comment adds something useful to the post")
    
    The FreeBSD manual page is correct but somewhat misleading.  The null device, called `/dev/null`, was present in Version 6 Unix, in the mid 1970s.  (BTW, `/dev/zero` was added much later.) Unfortunately, I have no supporting evidence. 
    
    – [G-Man Says 'Reinstate Monica'](https://unix.stackexchange.com/users/80216/g-man-says-reinstate-monica "24,058 reputation")
    
     [CommentedJan 1, 2017 at 23:12](https://unix.stackexchange.com/questions/332906/why-was-dev-null-called-that?utm_source=chatgpt.com#comment588685_332906)
    
- [](https://unix.stackexchange.com/questions/332906/why-was-dev-null-called-that?utm_source=chatgpt.com# "This comment adds something useful to the post")
    
    "on unix an "always blocking file" could be used to wait for signals." As it turns out, there's a system call that's used to wait for signals - `pause()`. 
    
    – [Mark Plotnick](https://unix.stackexchange.com/users/49439/mark-plotnick "26,053 reputation")
    
     [CommentedJan 5, 2017 at 15:52](https://unix.stackexchange.com/questions/332906/why-was-dev-null-called-that?utm_source=chatgpt.com#comment590481_332906)
    

[Add a comment](https://unix.stackexchange.com/questions/332906/why-was-dev-null-called-that?utm_source=chatgpt.com# "Use comments to ask for more information or suggest improvements. Avoid answering questions in comments.")  |  [Show **3** more comments](https://unix.stackexchange.com/questions/332906/why-was-dev-null-called-that?utm_source=chatgpt.com# "Expand to show all comments on this post")

Start a bounty


`null` was chosen because [it discards any data sent](https://en.wikipedia.org/wiki/Null_device), pretty much like a void place. That's why its also called black hole.

It is [a character device](https://www.kernel.org/doc/html/latest/admin-guide/devices.html), a stream that has no connection to a real space in memory. Fun fact is that [you can make your own personalized `/dev/null`](http://thelinuxstuff.blogspot.com.br/2012/08/how-do-you-create-devnull-device-and-use.html) with `mknod -m 666 /dev/null c 1 3`.

Additionally, [it sends `EOF` if you try to read from it](http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap10.html).

'null' means 'nothing', 'without value', and so on.

'empty' implies a container. For emptiness to exist we need a container.

In computer science in which zero is a value, we need a term for 'nothing'. So we have the 'null pointer' for example which is, functionally, a pointer to nothing.

'/dev/null' is the 'nothing device'. If we want something to disappear into nothingness, we give it to the nothing device.

If we give something to /dev/empty then the 'empty' device is no longer empty but is the container of the thing we sent to it.
