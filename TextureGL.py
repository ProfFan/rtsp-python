import ctypes
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk, GLib, Gtk
from gi.repository import GObject, Gst, GstVideo
import six
from OpenGL.GL import *
from OpenGL.GLUT import *

class Receiver(object):

    def __init__(self, video_tex_id, pipeline_string):
        self.tex_updated = True
        self.texdata = (ctypes.c_ubyte * 1024 * 576 * 3)()
        self.video_tex_id = video_tex_id

        # Create GStreamer pipeline
        self.pipeline = Gst.parse_launch(pipeline_string)

        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::error', self.on_error)

        self.fakesink = self.pipeline.get_by_name('fakesink0')
        self.fakesink.props.signal_handoffs = True
        self.fakesink.connect("handoff", self.on_gst_buffer)

        self.pipeline.set_state(Gst.State.PLAYING)
        print("TextureGL: INIT_SUCCESS")

    def on_gst_buffer(self, fakesink, buff, pad, data=None):
        #print("TextureGL: GST_BUFFER")
        self.tex_updated = False
        (result, mapinfo) = buff.map(Gst.MapFlags.READ)
        assert result

        try:
            ctypes.memmove(self.texdata, mapinfo.data, mapinfo.size)
            #print(mapinfo.size)
            pass
        finally:
            buff.unmap(mapinfo)
        return Gst.FlowReturn.OK


    def updateTexture(self):
        if not self.tex_updated and not self.texdata == None:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.video_tex_id)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 1024, 576, 0, GL_RGB, GL_UNSIGNED_BYTE, self.texdata)
            self.tex_updated = True


    def on_eos(self, bus, msg):
        print('on_eos(): seeking to start of video')
        self.pipeline.seek_simple(
            gst.FORMAT_TIME,
            gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_KEY_UNIT,
            six.long(0)
        )


    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())
