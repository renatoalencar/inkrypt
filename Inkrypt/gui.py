
import gtk
import os
import random
from Inkrypt import cipher

def generate_keyfile(filename):
	stat = os.stat(filename)
	fp = open('%s.key' % filename, 'w')

	for i in range(stat.st_size):
		fp.write(chr(random.randint(0, 255)))

	fp.close()

	return open('%s.key' % filename)

class FileFrame(gtk.Frame):

	def __init__(self, label, title):
		gtk.Frame.__init__(self, label=label)
		self.btn = gtk.FileChooserButton(title)
		self.add(self.btn)
		self.btn.set_border_width(5)

	def get_filename(self):
		return self.btn.get_filename()
		

class MainWindow(gtk.Window):

	def __init__(self):
		gtk.Window.__init__(self)
		self.set_title('Inkrypt')
		self.set_icon_from_file('inkrypt.png')

		vbox = gtk.VBox()
		vbox.set_spacing(10)
		vbox.set_border_width(5)

		self.file_btn = FileFrame('File to encrypt/decrypt',
			'Select the file')
		vbox.add(self.file_btn)

		self.keyfile_btn = FileFrame('The key file generated', 
			'Select key file')
		vbox.add(self.keyfile_btn)

		hbox = gtk.HBox()
		hbox.set_border_width(2)
		hbox.set_spacing(4)

		btn_crypt = gtk.Button(label='Crypt')
		btn_decrypt = gtk.Button(label= 'Decrypt')

		btn_crypt.connect('clicked', self.crypt)
		btn_decrypt.connect('clicked', self.decrypt)

		hbox.add(btn_crypt)
		hbox.add(btn_decrypt)
		vbox.add(hbox)

		vbox1 = gtk.VBox()
		vbox1.add(vbox)

		self.statusbar = gtk.Statusbar()
		vbox1.add(self.statusbar)

		self.connect('destroy', gtk.main_quit)
		self.add(vbox1)

	def crypt(self, obj):
		filename = self.file_btn.get_filename()
		
		if not filename:
			self.statusbar.push(0, 'Select the file to encrypt')
			return None

		self.statusbar.push(0, 'Generating key...')
		key = generate_keyfile(filename)
		fp = open(filename)

		ciph = cipher.Cipher(fp, key)
		outp = open('%s.ink' % filename, 'w')

		self.statusbar.push(0, 'Encrypting...')
		ciph(outp)
		self.statusbar.push(0, 'Done.')

	def decrypt(self, obj):
		filename = self.file_btn.get_filename()
		
		if not filename:
			self.statubar.push(0, 'Select the file to decrypt')
			return None

		keyfilename = self.keyfile_btn.get_filename()

		if not keyfilename:
			self.statusbar.push(0, 'Select the key file')
			return None

		key = open(keyfilename)
		fp = open(filename)

		ciph = cipher.Cipher(fp, key)
		outp = open(filename[-4] if filename.endswith('.ink') 
			else filename, 'w')

		self.statusbar.push(0, 'Decrypting...')
		ciph(outp)
		self.statusbar.push(0, 'Done.')


def main():
	gtk.main()
