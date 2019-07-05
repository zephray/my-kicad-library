from pcbnew import *
import operator
import wx

def help():
    print "This python script shows the length of group which name starts with ddr"

def run():
    board = GetBoard()
    tracks = board.GetTracks()
    lengths = {}
    for track in tracks:
        netname = track.GetNetname()
        if (netname.startswith("/ddr")):
            lengths[netname] = lengths.get(netname, 0) + track.GetLength()
    msg = ''
    sorted_lengths = sorted(lengths, key=lengths.get)
    for key in sorted_lengths:
        msg = msg + "Net {0:}, length {1:.3f} mm\n".format(key, lengths[key] / 1000000)
    wx.MessageDialog(None, message = msg,style = wx.OK).ShowModal()

class menu(ActionPlugin):
    def defaults( self ):
        self.name = "DDR Length chart"
        self.category = "Layout"
        self.description = "Show the length of ddr traces."
    def Run(self):
        run()

try:
    menu().register()
except:
    pass