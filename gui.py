#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class GridWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Configurar um Domínio AD")
		Gtk.Window.set_default_size(self,340,150)
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
		self.add(box)

		labelDomain = Gtk.Label(label="Domínio",xalign=0.2)
		self.entryDomain = Gtk.Entry(text="escola.seduc")
		inputDomain = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=6)
		inputDomain.pack_start(labelDomain, True, True, 0)
		inputDomain.pack_start(self.entryDomain, True, True, 0)

		labelUser = Gtk.Label(label="Usuário ",xalign=0.2)
		self.entryUser = Gtk.Entry(text="administrator")
		inputUser = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=6)
		inputUser.pack_start(labelUser, True, True, 0)
		inputUser.pack_start(self.entryUser, True, True, 0)

		labelPass = Gtk.Label(label="Senha   ",xalign=0.2)
		self.entryPass = Gtk.Entry(text="manager")
		inputPass = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=6)
		inputPass.pack_start(labelPass, True, True, 0)
		inputPass.pack_start(self.entryPass, True, True, 0)

		buttonInsert = Gtk.Button(label="Juntar-se ao Domínio")
		buttonInsert.connect("clicked", self.buttonInsertClicked)

		box.pack_start(inputDomain, True, True, 0)
		box.pack_start(inputUser, True, True, 0)
		box.pack_start(inputPass, True, True, 0)
		box.pack_start(buttonInsert, True, True, 0)

	def buttonInsertClicked(self, widget):
		domain = self.entryDomain.get_text()
		user = self.entryUser.get_text()
		passwd = self.entryPass.get_text()
		os.system('echo -n '+domain+' > /tmp/domain.ad')
		os.system('echo -n '+user+' > /tmp/user.ad')
		os.system('echo -n '+passwd+' > /tmp/passwd.ad')
		Gtk.main_quit()

win = GridWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()