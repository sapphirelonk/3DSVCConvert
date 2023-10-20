# BIG THANKS and a general shoutout to https://gbatemp.net/threads/research-snes-virtual-console-save-files.498334/
# for the documentation! This wouldn't have been possible without that post!

# Please, dear user, set these variables accordingly.
SAVE_FILE = "input.srm"  # Please enter the filename of the file containing your emulator save.
OUTPUT_FILE = "output.ves"
DONOR_FILE = "output.ves"  # Please enter the filename of a file that is known to be a working VC save.
# DONOR_FILE may be the same as OUTPUT_FILE if it you want it to be overwritten.

# END OF USER-VARIABLES

header = []  # Creating the empty "header" (in this case a list) ...
for i in range(48):  # ... with 48 ...
    header.append(0x00)  # "empty" "bytes".
# I know that the above is bad programming practice and really inefficient,
# but since the code only has to be run once for every conversion, it's hopefully not that bad...

header[0] = 0x01  # Change the first byte to 0x01 (required).


# Read the game's preset id (Whatever that may be, I never really looked it up, it's just required...)
# and move it into the according position of the header.

with open(DONOR_FILE, 'rb') as file:
    file.seek(4)
    temp = file.read(2).hex()
    header[4] = int(temp[:2], 16)
    header[5] = int(temp[2:4], 16)

# Change bytes 17-24 to 0xC13586A565CB942C
header[16], header[17], header[18], header[19], header[20], header[21], header[22], header[23] \
    = 0xC1, 0x35, 0x86, 0xA5, 0x65, 0xCB, 0x94, 0x2C
# Please r/ProgrammingHorror, don't kill me...

# Write the header to the output file ...
with open(OUTPUT_FILE, 'wb') as file:
    for part in header:
        file.write(bytes((part,)))
    with open(SAVE_FILE, 'rb') as file2:
        file.write(file2.read())  # ... and append the savefile's content.

# Generate a "Checksum-16" (Found in HxD under this name...) for the entire save file
# (including the header, but "excluding" (leaving blank) bytes for the checksum).
checksum = 0
with open(OUTPUT_FILE, 'rb') as file:
    for byte in file.read():
        checksum += byte
checksum = str(hex(checksum % 65536))  # turn the checksum into a string for string slicing on line 38&39.
# Quote: Reverse the byte order (might be called "little endian" encoding?) and decrease the first byte down a single hex value.
header[2] = int(checksum[-2:], 16) - 1
header[3] = int(checksum[-4:-2], 16)
# Write this to the 3rd and 4th byte of the header
with open(OUTPUT_FILE, 'r+b') as file:
    file.seek(2)
    for part in header[2:4]:
        file.write(bytes((part,)))
