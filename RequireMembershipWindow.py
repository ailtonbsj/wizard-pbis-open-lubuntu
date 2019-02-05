#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class RequireMembershipWindow(Gtk.Window):

	selectedGroup = ''
	listBoxGroup = {}

	def addItemBoxGroup(self, item):
		print(self.selectedGroup)
		print(dir(self.listBoxGroup[self.selectedGroup]))

	def __init__(self):
		Gtk.Window.__init__(self, title="Restringir a um grupo")
		Gtk.Window.set_default_size(self,320,150)
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
		self.add(box)

		labelInfo = Gtk.Label()
		labelInfo.set_markup("<b>Você pode restringir essa máquina \n para um grupo de segurança</b>");

		labelSGroup = Gtk.Label(label="Grupo",xalign=0.2)
		
		with open('/tmp/sGroups','r') as file:
			sGroupRaw = file.read()
		sGroupList = sGroupRaw.split('\n')
		sGroupList.pop()
		sGroupList.insert(0,'--Sem Restrição--')

		sGroupStore = Gtk.ListStore(str)
		for group in sGroupList:
			sGroupStore.append([group])

		sGroupCombo = Gtk.ComboBox.new_with_model(sGroupStore)
		sGroupCombo.connect("changed", self.sGroupComboChanged)
		renderer_text = Gtk.CellRendererText()
		sGroupCombo.pack_start(renderer_text, True)
		sGroupCombo.add_attribute(renderer_text, "text", 0)
		sGroupCombo.set_active(0)

		inputSGroup = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=6)
		inputSGroup.pack_start(labelSGroup, True, True, 0)
		inputSGroup.pack_start(sGroupCombo, True, True, 0)

		self.boxListGroup = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)

		buttonFinish = Gtk.Button(label="Finalizar")
		buttonFinish.connect("clicked", self.buttonFinishClicked)

		box.pack_start(labelInfo, True, True, 0)
		box.pack_start(inputSGroup, True, True, 0)
		box.pack_start(self.boxListGroup, True, True, 0)
		box.pack_start(buttonFinish, True, True, 0)

	def sGroupComboChanged(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter is not None:
			model = combo.get_model()
			group = model[tree_iter][0]
			self.selectedGroup = group

	def buttonFinishClicked(self, widget):
		os.system('echo -n '+self.selectedGroup+' > /tmp/restric.ad')
		Gtk.main_quit()

win = RequireMembershipWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()