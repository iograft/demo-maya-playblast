# Copyright 2022 Fabrica Software, LLC

import os

import iograft
import iobasictypes

from iogmaya_threading import maya_main_thread


class ImportFBXAnimation(iograft.Node):
    """
    Import an animation file into the scene and merge into
    the loaded scene.
    """
    # Path to an FBX animation file to apply.
    anim_file = iograft.InputDefinition("anim_file", iobasictypes.String())

    # The name of the FBX animation.
    namespace = iograft.OutputDefinition("namespace", iobasictypes.String())

    # The start & end frames of the imported animation.
    start_frame = iograft.OutputDefinition("start_frame", iobasictypes.Int())
    end_frame = iograft.OutputDefinition("end_frame", iobasictypes.Int())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("import_fbx_anim")
        node.AddInput(cls.anim_file)
        node.AddOutput(cls.namespace)
        node.AddOutput(cls.start_frame)
        node.AddOutput(cls.end_frame)
        return node

    @staticmethod
    def Create():
        return ImportFBXAnimation()

    @maya_main_thread
    def Process(self, data):
        import maya.cmds
        anim_file = iograft.GetInput(self.anim_file, data)

        namespace = os.path.splitext(os.path.basename(anim_file))[0]

        # Build the args to the import command.
        file_args = {
            "i": True,
            "rnn": True,
            "type": "FBX",
            "ignoreVersion": True,
            "ra": True,
            "mergeNamespacesOnClash": False,
            "namespace": namespace,
            "options": "fbx",
            "preserveReferences": True,
            "importTimeRange": "override"
        }

        # Run the command.
        new_nodes = maya.cmds.file(anim_file, **file_args)

        # Get the imported frame range.
        start_time = maya.cmds.playbackOptions(animationStartTime=1, q=1)
        end_time = maya.cmds.playbackOptions(animationEndTime=1, q=1)

        iograft.SetOutput(self.namespace, data, namespace)
        iograft.SetOutput(self.start_frame, data, int(start_time))
        iograft.SetOutput(self.end_frame, data, int(end_time))


def LoadPlugin(plugin):
    node = ImportFBXAnimation.GetDefinition()
    plugin.RegisterNode(node, ImportFBXAnimation.Create)
