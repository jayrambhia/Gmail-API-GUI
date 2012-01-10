#!/usr/bin/python2.7

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import time
import smtplib
import imaplib
import email
import os
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE
from email.MIMEBase import MIMEBase
from email.parser import Parser
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
import mimetypes

class GUIAPI:
  
  def get_login(self, widget):
    user = self.user_entry.get_text()
    passw = self.pass_entry.get_text()
    if user and passw :
      self.user_entry.set_text('')
      self.pass_entry.set_text('')
      self.userbox.destroy()
      self.passbox.destroy()
      self.vbox.destroy()
      server = login(user, passw, self.vbox)
      print 'server created'
      NewWindow(user, server, self.window)
      
    
  def __init__(self):
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_size_request(350, 70)
    self.window.set_title('Gmail API - 1.1')
    self.window.connect('delete_event', lambda w,e : gtk.main_quit())

    self.vbox = gtk.VBox(False, 0)
    self.window.add(self.vbox)
    self.vbox.show()
    
    self.userbox = gtk.HBox(False, 0)
    self.vbox.pack_start(self.userbox, False, False, 0)
    self.userbox.show()
    
    user_label = gtk.Label('username')
    user_label.show()
    self.userbox.pack_start(user_label, False, False, 5)
    
    self.user_entry = gtk.Entry()
    self.user_entry.set_max_length(30)
#    user_entry.set_text('Username')
    self.userbox.pack_start(self.user_entry, False, False, 5)
    self.user_entry.show()
    
    gmail_label = gtk.Label('@gmail.com')
    gmail_label.show()
    self.userbox.pack_start(gmail_label, False, False, 0)
    
    self.passbox = gtk.HBox(False, 0)
    self.vbox.pack_start(self.passbox, False, False, 0)
    self.passbox.show()
    
    pass_label = gtk.Label('password')
    pass_label.show()
    self.passbox.pack_start(pass_label, False, False, 7)
   
    self.pass_entry = gtk.Entry()
    self.pass_entry.set_max_length(30)
    self.pass_entry.set_visibility(False)
#    pass_entry.set_text('password')
    self.passbox.pack_start(self.pass_entry, False, False, 0)
    self.pass_entry.show()
    
    button = gtk.Button('Sign In')
    button.connect('clicked', self.get_login)
    self.passbox.pack_start(button, False, False, 3)
    button.set_flags(gtk.CAN_DEFAULT)
    button.grab_default()
    button.show()
    
    self.window.show()
    
 
class NewWindow(GUIAPI):

  def mailcontent(self, widget):
    fromaddr = self.fromaddr_entry.get_text()
    if not fromaddr:
      fromaddr = self.user
    to = self.to_entry.get_text()
    to_list = to.split()
    if to_list:
      for i in range(len(to_list)):
        if '@' not in to_list[i] or '.' not in to_list[i]:
          print 'incorrect email'
          return
    else:
      return
    sub = self.sub_entry.get_text()

    textbuffer = self.textview.get_buffer()
    startiter = textbuffer.get_start_iter()
    enditer = textbuffer.get_end_iter()
    body = textbuffer.get_text(startiter, enditer)
    filelist = self.att_filelist

    sendemail(self.user, self.server, fromaddr, to, sub, body, filelist)
    self.getNewWindow()
    
  def getNewWindow(self):
    self.fromaddr_entry.set_text('')
    self.to_entry.set_text('')
    self.textbuffer.set_text('')
    self.sub_entry.set_text('')
    self.att_filelist = []
    self.att_filelist_box.destroy()
    self.att_filelist_box = gtk.VBox(False, 0)
    self.att_filelist_box.show()
    self.att_filelist_box_main.pack_start(self.att_filelist_box, False, False, 0)
    return    
       
    
  def select_file(self, widget, data = None):
    self.filew = gtk.FileSelection('Attach file')
    self.filew.ok_button.connect('clicked', self.file_ok_sel)
    self.filew.cancel_button.connect("clicked", lambda w: self.filew.destroy())
    self.filew.set_filename('Attach File')
    self.filew.show()
    
  def file_ok_sel(self, w):
    filename = self.filew.get_filename()
    print filename, 'attached'
    self.att_filelist.append(filename)
    print self.att_filelist
    self.filew.destroy()
    
    file_label = gtk.Label(filename)
    file_label.show()
    self.att_filelist_box.pack_start(file_label, False, False, 0)
   
  def quit(self, widget):
    gtk.main_quit()
    self.server.close()
    
  def __init__(self, user, server, window):
    self.att_filelist = []
    self.user = user
    self.server = server
    self.window = window
    self.window.set_size_request(800,600)
    
    self.vbox = gtk.VBox(False, 2)
    self.vbox.set_size_request(800,600)
    
    self.hbox = gtk.HBox(False, 2)
    self.hbox.set_size_request(800,50)
    
    self.vbox.pack_start(self.hbox, False, False, 2)
    self.vbox.show()    
    
    self.vpaned = gtk.VPaned()
    self.vbox.add(self.vpaned)
    
    self.label = gtk.Label(user)
    self.vpaned.add1(self.label)
    self.label.show()
    
    self.panedbox = gtk.HBox(False, 2)
    self.vpaned.add2(self.panedbox)
    self.panedbox.show()

    button = gtk.Button('Quit')
    button.set_size_request(100,50)  
    button.connect('clicked', self.quit)
    self.hbox.pack_end(button, False, False, 2)
    button.show()        
    
    self.window.add(self.vbox)
    
    self.pvbox = gtk.VBox(False, 0)
    self.panedbox.add(self.pvbox)
    self.pvbox.show()
    
    self.hBox1 = gtk.HBox()
    self.hBox1.set_size_request(800,100)
    self.hBox1.show()
    self.pvbox.pack_start(self.hBox1, False, False, 0)

    self.vBox1 = gtk.VBox()
    self.vBox1.set_size_request(80,100)
    self.vBox1.show()
    self.hBox1.pack_start(self.vBox1, False, False, 0)
    
    self.fromaddr_label = gtk.Label('From')
    self.fromaddr_label.show()
    self.vBox1.pack_start(self.fromaddr_label, False, False, 5)
    
    self.vBox2 = gtk.VBox()
    self.vBox2.set_size_request(700,100)
    self.vBox2.show()
    self.hBox1.pack_start(self.vBox2, False, False, 5)  
    
    self.fromaddr_entry = gtk.Entry()
    self.fromaddr_entry.set_max_length(30)
    self.vBox2.pack_start(self.fromaddr_entry, False, False, 0)
    self.fromaddr_entry.show()
    
    self.toaddr_label = gtk.Label('To')
    self.toaddr_label.show()
    self.vBox1.pack_start(self.toaddr_label, False, False, 5)
    
    self.to_entry = gtk.Entry()
    self.vBox2.pack_start(self.to_entry, False, False, 0)
    self.to_entry.show()
    
    self.sub_label = gtk.Label('Subject')
    self.sub_label.show()
    self.vBox1.pack_start(self.sub_label, False, False, 5)
    
    self.sub_entry = gtk.Entry()
    self.sub_entry.set_max_length(30)
    self.vBox2.pack_start(self.sub_entry, False, False, 0)
    self.sub_entry.show()
    
    att_file_box = gtk.EventBox()
    att_file_box.set_size_request(30,20)
    self.pvbox.pack_start(att_file_box,False, False, 2)
    att_file_box.show()
    
    self.att_filelist_box_main = gtk.VBox(False, 0)
    self.att_filelist_box_main.show()
    
    self.att_filelist_box = gtk.VBox(False, 0)
    self.att_filelist_box.show()
    self.att_filelist_box_main.pack_start(self.att_filelist_box)
    
    
    self.att_file_label = gtk.Label('Attach a file')
    att_file_box.add(self.att_file_label)
    self.att_file_label.show()
    
    self.att_file_label.set_size_request(10,20)
    att_file_box.set_events(gtk.gdk.BUTTON_PRESS_MASK)
    att_file_box.connect("button_press_event", self.select_file)

    att_file_box.realize()

#    self.att_file_box.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))

        # Set background color to green
    att_file_box.modify_bg(gtk.STATE_NORMAL, att_file_box.get_colormap().alloc_color("orange"))
    
    self.pvbox.pack_start(self.att_filelist_box_main, False, False, 0)
    
    self.sw = gtk.ScrolledWindow()
    self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    self.textview = gtk.TextView()
    self.textbuffer = self.textview.get_buffer()
    self.sw.add(self.textview)
    self.sw.show()
    self.textview.show()

    self.pvbox.pack_start(self.sw)
    self.textbuffer.set_text('')
    
    self.send_button = gtk.Button('send')
    self.send_button.set_size_request(400,30)
    self.send_button.connect('clicked', self.mailcontent)
    self.pvbox.pack_end(self.send_button, False, False, 0)
    self.send_button.show()
    
    self.vpaned.show()
    self.pvbox.show()
    self.hbox.show()        
    
def sendemail(user, server, fromaddr, to, sub, body, filelist):
  msg = email.MIMEMultipart.MIMEMultipart()
  msg['From'] = fromaddr
  msg['To'] = to
  msg['Subject'] = sub
  tolist = to.split()  
  msg.attach(MIMEText(body))
  msg.attach(MIMEText('\nsent via python', 'plain'))
  for i in range(len(filelist)):
    msg = attach_files(msg, filelist[i]) 
  server.sendmail(user,tolist,msg.as_string())
  print 'sent'
  for i in range(len(filelist)):
    filelist.pop()
  return
  
def attach_files(msg, filename):
  
  ctype, encoding = mimetypes.guess_type(filename)
  
  if ctype is None or encoding is not None:
    ctype = 'application/octet-stream'
    
  maintype, subtype = ctype.split('/', 1)
  f = open(filename, 'rb')      
  if maintype == 'text':
    part = MIMEText(f.read(), _subtype=subtype)
  elif maintype == 'image':
    part = MIMEImage(f.read(), _subtype=subtype)
  elif maintype == 'audio':
    part = MIMEAudio(f.read(), _subtype=subtype)
  else:
    part = MIMEBase(maintype, subtype)
    msg.set_payload(f.read())
    
  part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filename))    
  msg.attach(part)
  f.close()        
  
  return msg  
  
def login(user, passw, vbox):
  smtp_host = 'smtp.gmail.com'
  smtp_port = 587
  server = smtplib.SMTP()
  server.connect(smtp_host,smtp_port)
  server.ehlo()
  server.starttls()
  server.login(user,passw)
  return server   
    
def main():
  gtk.main()
  
if __name__ == '__main__':
  GUIAPI()
  main()
    
