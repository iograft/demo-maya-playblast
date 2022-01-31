# Copyright 2022 Fabrica Software, LLC

import iograft
import iobasictypes

from iogmaya_threading import maya_main_thread


class LoadMayaPlugin(iograft.Node):
    """
    Load the plugin with the given name/path into Maya. Helpful to ensure
    that a plugin is loaded prior to using its features.
    """
    plugin_name = iograft.InputDefinition("plugin", iobasictypes.String())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("load_plugin_maya")
        node.AddInput(cls.plugin_name)
        return node

    @staticmethod
    def Create():
        return LoadMayaPlugin()

    @maya_main_thread
    def Process(self, data):
        import maya.cmds
        plugin_name = iograft.GetInput(self.plugin_name, data)
        maya.cmds.loadPlugin(plugin_name)


def LoadPlugin(plugin):
    node = LoadMayaPlugin.GetDefinition()
    plugin.RegisterNode(node, LoadMayaPlugin.Create)
