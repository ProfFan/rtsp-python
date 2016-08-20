#!/usr/bin/env python

import sys, os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GdkX11, GstVideo

class GTK_Main(object):

    def __init__(self):
        window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("Video-Player")
        window.set_default_size(500, 400)
        window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        window.add(vbox)
        hbox = Gtk.HBox()
        vbox.pack_start(hbox, False, False, 0)
        self.entry = Gtk.Entry()
        hbox.add(self.entry)
        self.button = Gtk.Button("Start")
        hbox.pack_start(self.button, False, False, 0)
        self.button.connect("clicked", self.start_stop)
        self.movie_window = Gtk.DrawingArea()
        vbox.add(self.movie_window)
        window.show_all()

        self.pipeline = Gst.Pipeline()
        self.preview = Gst.ElementFactory.make("autovideosink", "preview")
        self.player = Gst.ElementFactory.make("rtspsrc", "player")
        self.decoder = Gst.ElementFactory.make("rtpjpegdepay", "decoder")
        self.queue = Gst.ElementFactory.make("queue","queue")
        converter = Gst.ElementFactory.make("jpegdec","converter")
        colorspace = Gst.ElementFactory.make("videoconvert","colorspace")

        self.pipeline.add(self.player)
        self.pipeline.add(self.decoder)
        self.pipeline.add(self.preview)
        self.pipeline.add(self.queue)
        self.pipeline.add(converter)
        self.pipeline.add(colorspace)
        
        self.player.link(self.decoder)
        self.decoder.link(converter)
        converter.link(colorspace)
        colorspace.link(self.queue)
        self.queue.link(self.preview)
        #self.decoder.link(self.preview)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

    def start_stop(self, w):
        if self.button.get_label() == "Start":
            filepath = self.entry.get_text().strip()
            self.button.set_label("Stop")
            self.player.set_property("location", filepath)
            self.pipeline.set_state(Gst.State.PLAYING)
        
    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            self.button.set_label("Start")

    def on_sync_message(self, bus, message):
        if message.get_structure().get_name() == 'prepare-window-handle':
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_window_handle(self.movie_window.get_property('window').get_xid())


GObject.threads_init()
Gst.init(None)
GTK_Main()
Gtk.main()
