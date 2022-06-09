CONVERT_DIR = "my/dir"

import os

def file_iter(path, ext):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            ext = os.path.splitext(filename)[1]
            if ext.lower().endswith(ext):
                yield os.path.join(dirpath, filename)

import bpy


def reset_blend():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def convert_recursive(base_path):
    files = glob.glob('C:\\Users\\roncl\\Documents\\FaitMaison\\AutoReconstruction\\Images\\*\\project\\*_LOD0.obj')
    for filepath_src in files:
        filepath_dst = os.path.splitext(filepath_src)[0] + ".glb"

        print("Converting %r -> %r" % (filepath_src, filepath_dst))

        reset_blend()

        bpy.ops.import_scene.obj(filepath=filepath_src)
        
        # create a copy of the context
        ctx = bpy.context.copy()
        
        # because the active_object attribute isn't created until the user interacts
        # with the scene we create one here but we don't need to set it to anything
        ctx['active_object'] = None

        # pass our context copy with active object attribute to the operator
        bpy.ops.export_scene.gltf(ctx, export_format="GLB",filepath=filepath_dst)


if __name__ == "__main__":
    convert_recursive(CONVERT_DIR)