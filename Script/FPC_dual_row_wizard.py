#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

from __future__ import division
import pcbnew

import FootprintWizardBase

class FPC_Dual_Row_FootprintWizard(FootprintWizardBase.FootprintWizard):

    def GetName(self):
        return "Dual Row FPC (SMT connector)"

    def GetDescription(self):
        return "Dual Row FPC (SMT connector) Footprint Wizard"

    def GetValue(self):
        pins = self.parameters["Pads"]["n"]
        return "FPC_DR_%d" % pins

    def GenerateParameterList(self):
        self.AddParam( "Pads", "n", self.uInteger, 45 )
        self.AddParam( "Pads", "pitch", self.uMM, 0.3 )
        self.AddParam( "Pads", "width", self.uMM, 0.3 )
        self.AddParam( "Pads", "upper_height", self.uMM, 0.7 )
        self.AddParam( "Pads", "lower_height", self.uMM, 1.25 )
        self.AddParam( "Pads", "separation", self.uMM, 3.45)
        self.AddParam( "Outline", "width", self.uMM, 16)
        self.AddParam( "Outline", "height", self.uMM, 4.15)

    # build a rectangular pad
    def smdRectPad(self,module,size,pos,name):
        pad = pcbnew.D_PAD(module)
        pad.SetSize(size)
        pad.SetShape(pcbnew.PAD_SHAPE_RECT)
        pad.SetAttribute(pcbnew.PAD_ATTRIB_SMD)
        pad.SetLayerSet( pad.SMDMask() )
        pad.SetPos0(pos)
        pad.SetPosition(pos)
        pad.SetName(name)
        return pad

    def CheckParameters(self):
        #TODO implement custom parameter checking
        pass

    def BuildThisFootprint(self):
        p = self.parameters
        pad_count        = int(p["Pads"]["n"])
        pad_width        = p["Pads"]["width"]
        pad_upper_height = p["Pads"]["upper_height"]
        pad_lower_height = p["Pads"]["lower_height"]
        pad_separation   = p["Pads"]["separation"]
        pad_pitch        = p["Pads"]["pitch"]
        outline_width    = p["Outline"]["width"]
        outline_height   = p["Outline"]["height"]

        size_upper_pad   = pcbnew.wxSize( pad_width, pad_upper_height )
        size_lower_pad   = pcbnew.wxSize( pad_width, pad_lower_height )
        size_text = self.GetTextSize()  # IPC nominal

        pad_upper_count  = int(pad_count / 2)
        pad_lower_count  = pad_upper_count + 1

        offsetX = (pad_lower_count - 1) * pad_pitch * 2 / 2

        # Gives a position and size to ref and value texts:
        textposy = pad_separation / 2 + pad_lower_height + pcbnew.FromMM(1) + self.GetTextThickness()
        angle_degree = 0.0
        self.draw.Reference( 0, textposy, size_text, angle_degree )

        textposy = textposy + size_text + self.GetTextThickness()
        self.draw.Value( 0, textposy, size_text )

        # create upper and lower pad array and add it to the module
        ypos = 0 - (pad_lower_height / 2 + pad_separation / 2)
        for n in range ( 0, pad_upper_count ):
            xpos = pad_pitch*n*2 + pad_pitch - offsetX
            pad = self.smdRectPad(self.module,size_upper_pad, pcbnew.wxPoint(xpos,ypos),str(n*2+2))
            self.module.Add(pad)

        ypos = pad_upper_height / 2 + pad_separation / 2
        for n in range ( 0, pad_lower_count ):
            xpos = pad_pitch*n*2 - offsetX
            pad = self.smdRectPad(self.module,size_lower_pad, pcbnew.wxPoint(xpos,ypos),str(n*2+1))
            self.module.Add(pad)

        # set SMD attribute
        self.module.SetAttributes(pcbnew.MOD_CMS)

        # add footprint outline
        linewidth = self.draw.GetLineThickness()
        margin = linewidth

        # left side - left line
        posx = 0 - outline_width / 2
        ystart = 0 - outline_height / 2
        yend = outline_height / 2
        self.draw.Line( posx, ystart, posx, yend )

        # left side - upper line
        posy = 0 - outline_height / 2
        xstart = 0 - outline_width / 2
        xend = 0 - offsetX - pad_pitch
        self.draw.Line( xstart, posy, xend, posy )

        # left side - lower line
        posy = outline_height / 2
        xend = 0 - offsetX - 2 * pad_pitch
        self.draw.Line( xstart, posy, xend, posy )

        # right side - right line
        posx = outline_width / 2
        ystart = 0 - outline_height / 2
        yend = outline_height / 2
        self.draw.Line( posx, ystart, posx, yend )

        # right side - upper line
        posy = 0 - outline_height / 2
        xstart = offsetX + pad_pitch
        xend = outline_width / 2
        self.draw.Line( xstart, posy, xend, posy )

        # right side - lower line
        posy = outline_height / 2
        xstart = offsetX + 2 * pad_pitch
        self.draw.Line( xstart, posy, xend, posy )

FPC_Dual_Row_FootprintWizard().register()
