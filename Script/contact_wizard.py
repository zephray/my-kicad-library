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

import sys
import math

import pcbnew
import FootprintWizardBase
import PadArray as PA


class contact_wizard(FootprintWizardBase.FootprintWizard):

    def GetName(self):
        return "Button Contact"

    def GetDescription(self):
        return "Contact for buttons"

    def GenerateParameterList(self):

        self.AddParam("Pads", "style", self.uInteger, 1, min_value = 1, max_value = 2)
        self.AddParam("Pads", "trace width", self.uMM, 0.2)
        self.AddParam("Pads", "trace clearance", self.uMM, 0.2)
        self.AddParam("Pads", "diameter", self.uMM, 5)

    def CheckParameters(self):
        pass

    def GetValue(self):
        return "contact"

    def square_contact(self):

        prm = self.parameters['Pads']
        p_trace_width = prm['trace width']
        p_trace_clearance = prm['trace clearance']
        p_diameter = prm['diameter'];


        spacing = p_trace_width + p_trace_clearance
        pad_length = p_diameter - spacing 
        radius = p_diameter/2
        posY = -radius + p_trace_width / 2
        alt = 0
        
        # draw horizontal bars
        while posY <= radius:
            posX = spacing * (2*alt-1) / 2

            pad = PA.PadMaker(self.module).SMDPad(p_trace_width, pad_length, shape=pcbnew.PAD_SHAPE_RECT, rot_degree=0.0)
            pos = self.draw.TransformPoint(posX, posY)
            pad.SetPadName(1+alt)
            pad.SetPos0(pos)
            pad.SetPosition(pos)
            pad.SetShape(pcbnew.PAD_SHAPE_OVAL)
            pad.SetLayerSet(pad.ConnSMDMask())

            pad.GetParent().Add(pad)
              
            posY = posY + spacing
            alt = 1-alt

        # vertical sides
        
        pad = PA.PadMaker(self.module).SMDPad(p_diameter, p_trace_width, shape=pcbnew.PAD_SHAPE_RECT, rot_degree=0.0)
        pos = self.draw.TransformPoint(-p_diameter/2 + p_trace_width/2, 0)
        pad.SetPadName(1)
        pad.SetPos0(pos)
        pad.SetPosition(pos)
        pad.SetLayerSet(pad.ConnSMDMask())
        pad.GetParent().Add(pad)
      
        pad = PA.PadMaker(self.module).SMDPad(p_diameter, p_trace_width, shape=pcbnew.PAD_SHAPE_RECT, rot_degree=0.0)
        pos = self.draw.TransformPoint(p_diameter/2 - p_trace_width/2, 0)
        pad.SetPadName(2)
        pad.SetPos0(pos)
        pad.SetPosition(pos)
        pad.SetLayerSet(pad.ConnSMDMask())
        pad.GetParent().Add(pad)

        # 
        body_radius = (p_diameter + self.draw.GetLineThickness())
        self.draw.Box(0,0,body_radius, body_radius)

    def round_contact(self):

        prm = self.parameters['Pads']
        p_trace_width = prm['trace width']
        p_trace_clearance = prm['trace clearance']
        p_diameter = prm['diameter'];

        radius = p_diameter/2
        circumference = (p_diameter + p_trace_width) * math.pi
        step_angle = p_trace_width / circumference * 360

                    
        # draw cross bars  
        spacing = p_trace_width + p_trace_clearance
        posY = -radius + spacing
        alt = 0
        min_y = posY
 
        while posY <= radius - spacing:
            pad_length = math.sqrt (radius * radius - posY * posY) * 2
            pad_length = pad_length - spacing 
            posX = spacing * (2*alt-1) / 2
            
            pad = PA.PadMaker(self.module).SMDPad(p_trace_width, pad_length, shape=pcbnew.PAD_SHAPE_OVAL, rot_degree=0)
            pos = self.draw.TransformPoint(posX, posY)
            pad.SetPadName(1+alt)
            pad.SetPos0(pos)
            pad.SetPosition(pos)
            pad.SetLayerSet(pad.ConnSMDMask())
            pad.GetParent().Add(pad)
            
            max_y = posY
            posY = posY + spacing
            alt = 1-alt

        angle1 = math.degrees(math.asin (min_y/radius))
        angle2 = math.degrees(math.asin (max_y/radius))
        
        print "%d %d" %(angle1,angle2)
        sys.stderr.write("%d %d\n" %(angle1,angle2))
        
        # draw the outer parts as an arc composed of small pads
        alt = 0
        for j in [0,1]:
            if j==0:        
                start_angle = 180 - angle2
                last_angle =  180 - angle1
            else:
                start_angle = angle1
                last_angle = angle2
            
            angle = start_angle
            while angle <= last_angle:
                posX = math.cos (math.radians(angle)) * radius
                posY = math.sin (math.radians(angle)) * radius
                pad = PA.PadMaker(self.module).SMDPad(p_trace_width, p_trace_width, shape=pcbnew.PAD_SHAPE_RECT, rot_degree=-angle)
                pos = self.draw.TransformPoint(posX, posY)
                pad.SetPadName(1+j)
                pad.SetPos0(pos)
                pad.SetPosition(pos)
                pad.SetLayerSet(pad.ConnSMDMask())
                pad.GetParent().Add(pad)
              
                angle = angle + step_angle
        
        # circle on silkscreen
        body_radius = (p_diameter/2 + self.draw.GetLineThickness())
        self.draw.Circle(0, 0, body_radius)
    
    def BuildThisFootprint(self):

        prm = self.parameters['Pads']
        p_diameter = prm['diameter'];
        p_style = prm['style']
         
        if p_style == 1:
            self.square_contact()
        else:
            self.round_contact() 

        text_size = self.GetTextSize()  # IPC nominal
        thickness = self.GetTextThickness()
        body_radius = (p_diameter/2 + self.draw.GetLineThickness())
        textposy = body_radius + self.draw.GetLineThickness()/2 + self.GetTextSize()/2 + thickness
        self.draw.Value( 0, textposy, text_size )
        self.draw.Reference( 0, -textposy, text_size )



contact_wizard().register()
