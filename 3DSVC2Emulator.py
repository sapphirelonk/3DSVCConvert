# Although this could be achieved much more easily with any Hex-Editor,
# if you like having all the scripts in one place, here you go!
INPUT_FILE = "input.ves"
OUTPUT_FILE = "output.srm"
# END OF USER_VARIABLES
with open(INPUT_FILE, 'rb') as file:
    file.seek(48)
    with open(OUTPUT_FILE, 'wb') as file2:
        file2.write(file.read())
