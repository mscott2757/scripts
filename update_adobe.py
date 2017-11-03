import os
import subprocess

channel_ids_map = {
    "Acrobat DC": "Pro--11.0.0--osx10--AdobeAcrobatXIPro-11.0",
    "Photoshop CC 2015": "CC (2014)--15.0--osx10--AdobePhotoshopCC2014-15.0",
    "Photoshop CC 2014": "CC (2015)--16.0--osx10--AdobePhotoshopCC2015-16.0",
    "InDesign CC 2014": "CC (2014)--10.0--osx10--AdobeInDesignCC2014-10.0",
    "InDesign CC 2015": "CC (2015)--11.0--osx10--AdobeInDesignCC2015-11.0",
    "Illustrator CC 2014": "CC (2014)--18.0--osx10-64--AdobeIllustrator18-mul",
    "Illustrator CC 2015": "CC (2015)--19.0--osx10-64--AdobeIllustrator19-mul",
}

adobe_apps = []
channel_ids = []

for filename in os.listdir("/Applications"):
    if filename.startswith("Adobe"):

        # strip off adobe prefix
        filename = filename[6:]

        if filename in channel_ids_map:
            adobe_apps.append(filename)
            channel_id = channel_ids_map[filename]
            channel_ids.append(channel_id)

if channel_ids:
    channel_ids_arg = "--channelIds=\"" + ",".join(channel_ids) + "\""
    command = ["RemoteUpdateManager", channel_ids_arg]

    print("Attempting to update")
    print(", ".join(adobe_apps) + "\n")
    print("Running command")
    print(" ".join(command) + "\n")

    try:
        subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print("Process returned with error (code {}): {}".format(e.returncode, e.output))
else:
    print("No Adobe Apps found")

