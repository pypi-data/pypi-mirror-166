import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.5.0.post167"
version_tuple = (0, 5, 0, 167)
try:
    from packaging.version import Version as V
    pversion = V("0.5.0.post167")
except ImportError:
    pass

# Data version info
data_version_str = "0.5.0.post25"
data_version_tuple = (0, 5, 0, 25)
try:
    from packaging.version import Version as V
    pdata_version = V("0.5.0.post25")
except ImportError:
    pass
data_git_hash = "9acceb8d1dbe799fb3890bb7aa6bea1a453c0ba1"
data_git_describe = "0.5.0-25-g9acceb8d"
data_git_msg = """\
commit 9acceb8d1dbe799fb3890bb7aa6bea1a453c0ba1
Merge: d21637e4 8b32238a
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Thu Sep 8 11:16:34 2022 +0200

    Merge pull request #664 from silabs-oivind/clic_ptr_fetch_mret_wb_fix
    
    Fix issue related to CLIC pointer fetch while MRET in WB

"""

# Tool version info
tool_version_str = "0.0.post142"
tool_version_tuple = (0, 0, 142)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post142")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn
