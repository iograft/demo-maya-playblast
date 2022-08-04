# Copyright 2022 Fabrica Software, LLC

import iograft
import iobasictypes

from iogmaya_threading import maya_main_thread


class FitToView(iograft.Node):
    """
    Fit the requested camera to frame all items in the scene.
    """
    camera = iograft.InputDefinition("camera", iobasictypes.String(),
                                     default_value="persp")

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("fit_to_view")
        node.SetMenuPath("Maya")
        node.AddInput(cls.camera)
        return node

    @staticmethod
    def Create():
        return FitToView()

    @maya_main_thread
    def Process(self, data):
        import maya.cmds
        camera = iograft.GetInput(self.camera, data)
        maya.cmds.viewFit(camera)


def LoadPlugin(plugin):
    node = FitToView.GetDefinition()
    plugin.RegisterNode(node, FitToView.Create)
