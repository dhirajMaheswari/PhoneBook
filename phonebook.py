"""
A simple Phonebook Application
taken from the book Tkinter GUI Application Development Hotshot
and modified a little!
Dhiraj Maheswari
""" 

from tkinter import *
from tkinter import ttk
import sqlite3


class PhoneBook:
	def __init__(self, master):
		
		photo = PhotoImage(file='phonebookicon.gif')
		label = Label(image=photo)
		label.image = photo
		label.grid(row=0, column=0)

		fr = LabelFrame(master, text= 'Create/Find Record')
		fr.grid(row=0, column=1, padx=2,pady=8, sticky='ew')
		
		Label(fr, text='Name:').grid(row=1, column=1, sticky=W, pady=2)
		self.name= StringVar()
		self.namefield = Entry(fr, textvariable= self.name)
		self.namefield.grid(row=1, column=2, sticky=W, padx=5, pady=2)
		Label(fr, text='Contact Number:').grid(row=2, column=1,sticky=W,  pady=2)
		self.num= IntVar()
		self.numfield = Entry(fr, textvariable= self.num)
		self.numfield.grid(row=2, column=2, sticky=W,padx=5, pady=2)
		ttk.Button(fr, text= 'Add Record', command=self.create_record).grid(row=3, column=2, sticky=E,padx=5, pady=2)
		showbtn = ttk.Button(fr,text="Show Records", command = self.view_records)
		showbtn.grid(row=3, column=0, sticky=W, padx=15,pady=2)
		
		self.msg=Label(text='', fg='red')
		self.msg.grid(row=3, column=1, sticky=W)

		self.tree = ttk.Treeview(height=4, columns=2)
		self.tree.grid(row=4, column=0, columnspan=2, sticky=E)
		self.tree.heading('#0', text='Name', anchor=W)
		self.tree.heading(2, text='Phone Number', anchor=W)

		fr1 = LabelFrame(master, text="Available Actions-")
		fr1.grid(row=4, column=3, sticky='w', padx=15, pady = 5)

		delbtn = ttk.Button(fr1,text="Delete Selected", command = self.delete_record)
		delbtn.grid(row=5, column=0, sticky='w', padx=5,pady=2)
		
		updtbtn = ttk.Button(fr1,text="Modify Selected", command = self.open_modify_window)
		updtbtn.grid(row=6, column=0, sticky='w', padx=5,pady=2)

		findbtn = ttk.Button(fr1,text = "Find",command = self.find_records)
		findbtn.grid(row=7, column=0, sticky='w', padx=5,pady=2) 
		#self.view_records()
		
						
	def create_record(self):
		name = self.namefield.get()
		num = self.numfield.get()
		if name == "":
			self.msg["text"] = "Please Enter name"
			return
		if num == "":
			self.msg["text"] = "Please Enter Number"
			return
		conn = sqlite3.connect('phonebook.db')
		c = conn.cursor()
		c.execute("INSERT INTO contacts VALUES(NULL,?, ?)", (name, num))
		conn.commit()                  
		c.close()
		self.namefield.delete(0, END)
		self.numfield.delete(0, END)
		self.msg["text"] = "Phone Record of %s Added" %name
		self.view_records()
			
	def view_records(self):
			self.msg['text']=''
			x = self.tree.get_children()
			for item in x: 
				self.tree.delete(item)
			conn = sqlite3.connect('phonebook.db')
			c = conn.cursor()
			list = c.execute("SELECT * FROM contacts ORDER BY name desc")

			#print(type(list))
			#print(list)
			for row in list:
					self.tree.insert("",0,text=row[1],values=row[2])
			
			c.execute("SELECT * FROM contacts")
			totRowsCount = len(c.fetchall())
			self.msg['text'] = "Total Records: " + str(totRowsCount)
			c.close()


	def delete_record(self):
			self.msg["text"] = ""
			conn = sqlite3.connect('phonebook.db')
			c = conn.cursor()
			name = self.tree.item(self.tree.selection())['text']
			query = "DELETE FROM contacts WHERE name = '%s';" %name
			c.execute(query)
			conn.commit()
			c.close()
			self.msg["text"] = "Phone Record for %s Deleted" %name
			self.view_records()
			
			
	def open_modify_window(self):
			try:
				self.msg["text"] = ""
				name = self.tree.item(self.tree.selection())['text']
				oldphone = self.tree.item(self.tree.selection())['values'][0]
				
				self.tl = Tk()
				self.tl.resizable(False,False)
				self.tl.attributes("-toolwindow",-1)
				self.tl.title("Modify: %s." %name)
				
				Label(self.tl,text='Name:').grid(row=0, column=1, sticky=W)
				ne = Entry(self.tl)
				ne.grid(row=0, column=2, sticky=W)
				ne.insert(0,name)
				ne.config(state='readonly')
			
				Label(self.tl, text='Old Phone Number:').grid(row=1, column=1,sticky=W)
				ope = Entry(self.tl)
				ope.grid(row=1, column=2, sticky=W)
				ope.insert(0,str(oldphone))
				ope.config(state='readonly')
			
				Label(self.tl, text='New Phone Number:').grid(row=2, column=1,sticky=W)
				newph = StringVar()
				newphe = Entry(self.tl, textvariable=newph)
				newphe.grid(row=2, column=2, sticky=W)
			
				upbtn = Button(self.tl, text= 'Update Record', command=lambda:self.update_record(newphe.get(),oldphone, name))
				upbtn.grid(row=3, column=2, sticky=E)
				
				self.tl.mainloop()
			
			except IndexError as e:
				self.msg["text"] = "Please Select Item to Modify"
			
	def update_record(self, newphone,oldphone, name):
			conn = sqlite3.connect('phonebook.db')
			c = conn.cursor()
			c.execute("UPDATE contacts SET contactnumber=? WHERE contactnumber=? AND name=?", (newphone, oldphone, name)) 
			conn.commit()
			c.close()
			self.tl.destroy()
			self.msg["text"] = "Phone Number of %s modified" %name
			self.view_records()

	def find_records(self):
			self.msg['text'] = ''
			x = self.tree.get_children()
			for item in x:
				self.tree.delete(item)
			naam = self.namefield.get()
			#self.msg['text'] = 'Showing results for: ' + naam
			conn = sqlite3.connect('phonebook.db')
			c = conn.cursor()

			list = c.execute("SELECT * FROM contacts WHERE name = '%s';" %naam)

			check = c.fetchall()
			print(check)

			if check:
				for row in check:
					self.msg['text'] = "Showing result for: %s" %naam	
					self.tree.insert("",0,text=row[1],values = row[2])
				c.close()
				return
			else:
				self.msg['text'] = "No match found for %s." %naam.strip()
				c.close()
				return
			
			

   
	
root = Tk()
root.title("PhoneBook")
root.attributes("-toolwindow",1) # remove the maximize and minimize buttons
root.resizable(False,False)
application = PhoneBook(root)
root.mainloop()