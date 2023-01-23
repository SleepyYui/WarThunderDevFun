import tkinter as tk
import json
import requests


URL="http://localhost:8111/"
AFTERURL="editor/fm_commands?cmd="
VALUEURL="&value="

class WindowManager(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("War Thunder Dev Fun")
        self.geometry("300x300")
        self._frame = None

        with open("variables.json", "r") as f:
            self._variables = json.load(f)[0]

        self._default_vars = self._variables["DefaultVars"]

        for name,var in self._default_vars.items():
            #print(var)
            #print(name)
            name = var["defname"]
            abtn = tk.Button(self, text=name, command=lambda name=name: self.open_value_setter_frame(name), state=var["working"])
            abtn.pack(side="top")

    def open_value_setter_frame(self, name):
        var = self._default_vars[name]
        nwindow = tk.Toplevel(self)
        nwindow.title(name)
        nwindow.geometry("200x185")
        label = tk.Label(nwindow, text=f"Enter a value for {name}").pack(side="top")
        textbox = tk.Entry(nwindow)
        textbox.pack(side="top")
        #print(textbox)
        rtext = tk.Text(nwindow, height=5, width=20)
        submitbutton = tk.Button(nwindow, text="Submit", command=lambda: self.submit_value(nwindow, name, var, textbox, rtext, False))
        submitbutton.pack(side="top")
        resetbutton = tk.Button(nwindow, text="Reset", command=lambda: self.submit_value(nwindow, name, var, textbox, rtext, True))
        resetbutton.pack(side="top")

    def submit_value(self, nwindow, name, var, value, rtext, reset):
        if reset != True:
            value = value.get()
        else:
            value = var["default"]
        #print(value)
        rtext.delete(1.0, tk.END)
        cmdvar = var["setter"]
        print(f"Setting: {cmdvar} to {value}")
        rresp = False
        try:
            try:
                response = requests.get(url=f"{URL}{AFTERURL}{cmdvar}{VALUEURL}{value}")
            except requests.exceptions.ConnectionError:
                try:
                    response = {"no_response": False, "response": f"{response}"}
                    rresp = True
                except:
                    response = {"no_response": True, "response": None}
                    rresp = True
        except Exception as e:
            print(e)
            print("Dev mode is not enabled, or you are not in a Test Flight.")
            exit()
        print(f"Got response: {response}")
        if not rresp is True:
            try:
                responsedata = response.json()
            except json.decoder.JSONDecodeError:
                responsedata = {"no_response": False, "response": f"{response}"}
        else:
            responsedata = response
        rtext.pack(side="top")
        rtext.insert(tk.END, responsedata)
        return responsedata


WM = WindowManager()
WM.mainloop()
