import os
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__))+ '/enum')
sys.path.append(os.path.dirname(os.path.abspath(__file__))+ '/workflow')

from enum import Enum
from workflow import Workflow


class FileType(Enum):
    xcodeproj = 'xcode-project_Icon.icns'
    xcworkspace = 'workspace_Icon.icns'
    playground = 'playground_Icon.icns'

    def extension(self):
        return self.name

    def icon(self):
        return self.value

def search(query, file_type):
    find_command = "mdfind \"kMDItemFSName == '{0}*.{1}'c\"".format(query, file_type.extension())
    found_paths = subprocess.check_output(find_command, shell=True).decode("utf-8").rstrip().split("\n")
    results = []
    for path in found_paths:
        filename = path.split("/")[-1]
        results.append((filename, path, file_type.icon()))
    return results


def main(wf):
    if len(wf.args) > 0:
        query = wf.args[0]
    else:
        return

    xcode_path = subprocess.check_output("xcode-select -print-path", shell=True).decode("utf-8").rstrip()
    xcode_resouce_path= "/".join(xcode_path.split("/")[:-1]) + "/Resources/"

    for fileType in [FileType.xcworkspace, FileType.playground, FileType.xcodeproj]:
        for (filename, path, icon) in search(query, fileType):
            wf.add_item(filename, path, arg=path, valid=True, icon=xcode_resouce_path + icon)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
