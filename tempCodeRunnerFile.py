from tkinter import filedialog

filename = filedialog.askopenfilename()

with open(filename, "r") as file:
    uncompressed = file.read()

print(uncompressed) 

tags = []
tags.append({"pos":0, "len":0, "sym":"a"})
tags.append({"pos":0, "len":0, "sym":"b"})

for i in range(len(tags)):
  print(f"< {tags[i]["pos"]} , {tags[i]["len"]} , {tags[i]["sym"]} >")

with open("Output/new.txt", "w") as file:
  for i in range(len(tags)):
    file.write(f"< {tags[i]["pos"]} , {tags[i]["len"]} , {tags[i]["sym"]} >\n")