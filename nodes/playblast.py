# Copyright 2022 Fabrica Software, LLC

import os

import iograft
import iobasictypes

from iogmaya_threading import maya_main_thread


class Playblast(iograft.Node):
    """
    Export a playblast movie.
    """
    filename = iograft.InputDefinition("output_file", iobasictypes.Path())
    start_frame = iograft.InputDefinition("start_frame", iobasictypes.Int(),
                                          default_value=0)
    end_frame = iograft.InputDefinition("end_frame", iobasictypes.Int(),
                                        default_value=10)

    output = iograft.OutputDefinition("output_file", iobasictypes.Path())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("playblast_maya")
        node.AddInput(cls.filename)
        node.AddInput(cls.start_frame)
        node.AddInput(cls.end_frame)
        node.AddOutput(cls.output)
        return node

    @staticmethod
    def Create():
        return Playblast()

    @maya_main_thread
    def Process(self, data):
        import maya.cmds
        output_file = iograft.GetInput(self.filename, data)
        start_time = iograft.GetInput(self.start_frame, data)
        end_time = iograft.GetInput(self.end_frame, data)

        playblast_args = {
            "startTime": start_time,
            "endTime": end_time,
            "filename": output_file,
            "percent": 50,
            "clearCache": True,
            "format": "movie",
            "width": 1280,
            "height": 720,
            "offScreen": True,
            "viewer": False,
            "forceOverwrite": True
        }
        output = maya.cmds.playblast(**playblast_args)

        iograft.SetOutput(self.output, data, output)


def LoadPlugin(plugin):
    node = Playblast.GetDefinition()
    plugin.RegisterNode(node, Playblast.Create)
