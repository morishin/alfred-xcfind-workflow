#!/usr/bin/env python

import subprocess
import sys

from workflow import Workflow


def main(wf):
    if len(wf.args) > 0:
        query = wf.args[0]
    else:
        return

    xcode_path = subprocess.check_output("xcode-select -print-path", shell=True).decode("utf-8").rstrip()
    xcode_resouce_path= "/".join(xcode_path.split("/")[:-1]) + "/Resources/"

    find_xcworkspace = "mdfind \"kMDItemFSName == '{0}*.xcworkspace'c\"".format(query)
    xcworkspace_files = subprocess.check_output(find_xcworkspace, shell=True).decode("utf-8").rstrip().split("\n")
    xcworkspace_icon_path = xcode_resouce_path + 'workspace_Icon.icns'
    for path in xcworkspace_files:
        filename = path.split("/")[-1]
        wf.add_item(filename, path, arg=path, valid=True, icon=xcworkspace_icon_path)

    find_xcodeproj = "mdfind \"kMDItemFSName == '{0}*.xcodeproj'c\"".format(query)
    xcodeproj_files = subprocess.check_output(find_xcodeproj, shell=True).decode("utf-8").rstrip().split("\n")
    xcodeproj_icon_path = xcode_resouce_path + 'xcode-project_Icon.icns'
    for path in xcodeproj_files:
        filename = path.split("/")[-1]
        wf.add_item(filename, path, arg=path, valid=True, icon=xcodeproj_icon_path)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))

