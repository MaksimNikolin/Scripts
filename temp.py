import subprocess
import tkinter as tk

def get_temperature():
    result = subprocess.run(['sensors'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    temperatures = []
    for line in output.splitlines():
        if "°C" in line:
            if "Tctl" in line:
                temperatures.append("CPU: " + line.split(":")[1].strip())
            elif "edge" in line:
                temperatures.append("GPU: " + line.split(":")[1].strip())
            elif "temp1" in line:
                temperatures.append("ACPI: " + line.split(":")[1].strip())
            else:
                temperatures.append(line.strip())
    
    return temperatures

def update_temperatures():
    temperatures = get_temperature()
    while len(temperature_labels) < len(temperatures):
        label = tk.Label(temperature_frame, fg="black", bg="grey", font=("Helvetica", 10))
        label.pack()
        temperature_labels.append(label)
    for i, temp in enumerate(temperatures):
        temperature_labels[i].config(text=temp)
    for i in range(len(temperatures), len(temperature_labels)):
        temperature_labels[i].pack_forget()
    window.after(1000, update_temperatures)

window = tk.Tk()
window.title("Temperature")
window.geometry("380x125+10+500")
window.configure(bg='grey')
temperature_frame = tk.Frame(window, bg="grey")
temperature_frame.place(x=10, y=10)
temperature_labels = []
update_temperatures()
window.mainloop()
