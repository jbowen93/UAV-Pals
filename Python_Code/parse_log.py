f1 = open("flight_4_mod.log", "r")
lines = f.readlines()

f2 = open("parsed_log_4", "w")

for i in range (0, int(len(lines))):
    line = line.replace('Commanded RC Throttle is ', '', 1)
    line = line.replace('Error z is ', '', 1)
    f2.write(line)

f1.close()
f2.close()
