import tkinter as tk
import pickle
import os.path
import CALENDARWIDGET as cal
import calendar

# Setup Window
root = tk.Tk()
root.title("RECORDER")

# Configure Columns
root.columnconfigure(0, weight=1)
root.columnconfigure(3, weight=1)

# Show Loading Label
loadlabel = tk.Label(root, text="Loading data...")
loadlabel.grid(row=0, column=0)
root.update()

# Load Data
if not os.path.exists("RECORDER.dat"):
    with open("RECORDER.dat", "wb") as f:
        pickle.dump(list(), f)
    data = list()
else:
    with open("RECORDER.dat", "rb") as f:
        data = pickle.load(f)

# Hide Loading Label
loadlabel.destroy()

# Save function
def saverecord(title, desc, date):
    global data, addtitle, adddesc, adddate, r, frame
    data.append({"title": title, "description": desc, "date": date})
    with open("RECORDER.dat", "wb") as f:
        pickle.dump(data, f)
    addtitle.delete(0, "end")
    adddesc.delete(0.0, "end")
    itemframe = tk.Frame(frame, relief="raised", bd=1)
    itemframe.grid(row=r, sticky="ew")
    titlelabel = tk.Label(itemframe, text=title, fg="red")
    titlelabel.pack(fill="x")
    desclabel = tk.Message(itemframe, text=desc, width=380)
    desclabel.pack(fill="x")
    r += 1

# Setup "New" form
addframe = tk.Frame(root)
addframe.grid(row=0, column=1, sticky="ew")
addlabel = tk.Label(addframe, text="Add Record")
addlabel.grid(row=0, columnspan=2, sticky="ew")

addtitlelabel = tk.Label(addframe, text="Record Title")
addtitlelabel.grid(row=1, column=0)
addtitle = tk.Entry(addframe)
addtitle.grid(row=1, column=1, sticky="ew")
adddesclabel = tk.Label(addframe, text="Record Description")
adddesclabel.grid(row=2, columnspan=2, sticky="ew")
adddesc = tk.Text(addframe)
adddesc.grid(row=3, columnspan=2, sticky="ew")
adddatelabel = tk.Label(addframe, text="Select Date")
adddatelabel.grid(row=4, sticky="ew")
adddate = cal.Calendar(addframe)
adddate.grid(row=4, column=1, sticky="ew")
addsubmit = tk.Button(addframe, text="Save", command=lambda: saverecord(addtitle.get(), adddesc.get(0.0, tk.END), adddate.selection))
addsubmit.grid(row=5, columnspan=2, sticky="ew")

# Setup View Area
seeframe = tk.Frame(root)
seeframe.grid(row=0, column=2, sticky="nesw")
seelabel = tk.Label(seeframe, text="See Records")
seelabel.grid(row=0, sticky="ew")

seeframescrollarea = tk.Frame(seeframe)
seeframescrollarea.grid(row=1, sticky="nesw")
canvas=tk.Canvas(seeframescrollarea, height=500)
frame=tk.Frame(canvas)
frame.columnconfigure(0, weight=1)
scrollbar=tk.Scrollbar(seeframescrollarea, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="y")
canvas.create_window((0,0), window=frame, anchor="nw")

sorteddata = sorted(data, key=lambda k: k["date"], reverse=True)
r = 0
for dataitem in sorteddata:
    itemframe = tk.Frame(frame, relief="raised", bd=1)
    itemframe.grid(row=r, sticky="ew")
    titlelabel = tk.Label(itemframe, text=dataitem["title"], fg="red")
    titlelabel.pack(fill="x")
    desclabel = tk.Message(itemframe, text=dataitem["description"], width=380)
    desclabel.pack(fill="x")
    r += 1


# Mainloop
root.mainloop()
