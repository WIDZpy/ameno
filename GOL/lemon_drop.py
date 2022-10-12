import tkinter as tk
from tkinter import ttk
'''la fenaitre tkinter'''


class lemon:
	
	def __init__(self):
		self.main_dic = {
			'start_camera': (16, 16),
			'start_shape': (0, 0),
			'max': (-1, -1),
			'import_adapt': {}
		}
		self.window = tk.Tk(className=" ")
		style = ttk.Style(self.window)
		style.configure("Button", background="red")
		style.map('Button', background=[('active', 'red')])
		self.window.tk.call('source', 'textures/azure dark 2/azure dark.tcl')
		style.theme_use('azure')
	
	def save(self):
		return
	
	def lunche(self):
		return
	
	def printttt(self):
		print(1)

	def aficher(self):
		frame_prinsipale = ttk.Frame(self.window).grid(row=0)
		
		# --------------------------------gros bouton-------------------------------------------------
		frame_grosbouton = ttk.Frame(frame_prinsipale)
		buton_load = ttk.Button(frame_grosbouton, command=lambda: buton_save.grid_forget(), text='load')
		buton_save = ttk.Button(frame_grosbouton, command=self.printttt, text='save')
		buton_clear = ttk.Button(frame_grosbouton, command=self.printttt, text='clear')

		frame_grosbouton.grid(row=0)
		buton_load.grid(row=0, column=0, padx=5, pady=5)
		buton_save.grid(row=0, column=1, padx=5, pady=5)
		buton_clear.grid(row=0, column=2, padx=5, pady=5)
		# ---------------------------------------------------------------------------------
		

if __name__ == '__main__':
	le = lemon()
	le.aficher()
	tk.mainloop()
