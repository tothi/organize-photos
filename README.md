# organize-photos

organize photos taken using different devices: batch rename media files
in given directory according to creation date and device model exif
metadata:

> orig.JPG -> 20190820_2015_Nexus5X.jpg

device translation and optional datetime difference infos are stored in
the appropriate `.conf` file.

## typical use-case

photos (+videos) taken during holiday using various devices.
you want to organize them in a folder with suitable ordering
(by timeline, regardless the shooter device) while keeping also the
shooter device name in the filename.

this way the most comprehensive slideshow is available by
timeline inlcuding all of the devices.

## usage

1.) edit exifrename.conf

2.) python exifrename.py [folder_name]

