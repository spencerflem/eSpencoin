import pexpect
from pexpect import popen_spawn
import sys

child = pexpect.popen_spawn.PopenSpawn("dfrotz zork1.z5")

child.logfile = sys.stdout.buffer

child.expect('>')
print("LOL" + child.before.decode('utf-8') + "LOL2")
child.sendline('anonymous')
child.expect('>')
print("LOL" + child.before.decode('utf-8') + "LOL2")