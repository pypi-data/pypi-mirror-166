#! /usr/bin/env python

import os
import sys
import shutil
import platform
import tempfile
from optparse import OptionParser
import subprocess

try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

usage = """
This command creates a graphical installer for the
Panda3D plugin and runtime environment.

  %prog [opts]"""

parser = OptionParser(usage = usage)
parser.add_option('-n', '--short', dest = 'short_name',
                  help = 'The product short name',
                  default = 'Panda3D')
parser.add_option('-N', '--long', dest = 'long_name',
                  help = 'The product long name',
                  default = 'Panda3D Game Engine')
parser.add_option('-v', '--version', dest = 'version',
                  help = 'The product version',
                  default = None)
parser.add_option('-p', '--publisher', dest = 'publisher',
                  help = 'The name of the publisher',
                  default = 'Carnegie Mellon Entertainment Technology Center')
parser.add_option('', '--install', dest = 'install_dir',
                  help = "The install directory on the user's machine (Windows only)",
                  default = '$PROGRAMFILES\\Panda3D')
parser.add_option('-l', '--license', dest = 'license',
                  help = 'A file containing the license or EULA text',
                  default = None)
parser.add_option('-w', '--website', dest = 'website',
                  help = 'The product website',
                  default = 'https://www.panda3d.org')
parser.add_option('', '--start', dest = 'start',
                  help = 'Specify this option to add a start menu',
                  action = 'store_true', default = False)
parser.add_option('', '--welcome_image', dest = 'welcome_image',
                  help = 'The image to display on the installer, 170x312 BMP',
                  default = None)
parser.add_option('', '--install_icon', dest = 'install_icon',
                  help = 'The icon to give to the installer',
                  default = None)
parser.add_option('', '--nsis', dest = 'nsis',
                  help = 'The path to the makensis executable',
                  default = None)
parser.add_option('', '--cab', dest = 'cab',
                  help = 'Generate an ActiveX CAB file (Windows only).  If --spc and --pvk are not also specified, the CAB file will be unsigned.',
                  action = 'store_true', default = False)
parser.add_option('', '--spc', dest = 'spc',
                  help = 'Sign the CAB file generated by --cab with the indicated spc file (Windows only).  You must also specify --pvk.',
                  default = None)
parser.add_option('', '--pvk', dest = 'pvk',
                  help = 'Specifies the private key to be used in conjuction with --spc to sign a CAB file (Windows only).',
                  default = None)
parser.add_option('', '--mssdk', dest = 'mssdk',
                  help = 'The path to the MS Platform SDK directory (Windows only).  mssdk/bin should contain cabarc.exe and signcode.exe.',
                  default = None)
parser.add_option('', '--regview', dest = 'regview',
                  help = 'Which registry view to use, 64 or 32.',
                  default = None)

(options, args) = parser.parse_args()

this_dir = os.path.split(sys.argv[0])[0]

assert options.version, "A version number must be supplied!"

##############################################################################
#
# This Info.plist file is used only for the OSX 10.4 version of packagemaker.
#
##############################################################################

Info_plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleIdentifier</key>
  <string>%(package_id)s</string>
  <key>CFBundleShortVersionString</key>
  <string>%(version)s</string>
  <key>IFPkgFlagRelocatable</key>
  <false/>
  <key>IFPkgFlagAuthorizationAction</key>
  <string>RootAuthorization</string>
</dict>
</plist>
"""

##############################################################################
#
# This Description.plist file is used only for the OSX 10.4 version of packagemaker.
#
##############################################################################

Description_plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>IFPkgDescriptionDescription</key>
  <string></string>
  <key>IFPkgDescriptionTitle</key>
  <string>%(long_name)s</string>
</dict>
</plist>
"""


##############################################################################
#
# Locate the relevant files.
#
##############################################################################

def findExecutable(filename):
    """ Searches for the named .exe or .dll file along the system PATH
    and returns its full path if found, or None if not found. """

    if sys.platform == "win32":
        for p in os.defpath.split(";") + os.environ["PATH"].split(";"):
            if os.path.isfile(os.path.join(p, filename)):
                return os.path.join(p, filename)
    else:
        for p in os.defpath.split(":") + os.environ["PATH"].split(":"):
            if os.path.isfile(os.path.join(p, filename)):
                return os.path.join(p, filename)
    return None


if not options.nsis:
    makensis = findExecutable('makensis.exe')
    if sys.platform == "win32":
        if not makensis:
            try:
                import pandac
                makensis = os.path.dirname(os.path.dirname(pandac.__file__))
                makensis = os.path.join(makensis, "nsis", "makensis.exe")
                if not os.path.isfile(makensis):
                    makensis = None
            except ImportError: pass
        if not makensis:
            thirdparty = os.environ.get("MAKEPANDA_THIRDPARTY", "thirdparty")
            makensis = os.path.join(thirdparty, "win-nsis", "makensis.exe")
            if not os.path.isfile(makensis):
                makensis = None
        options.nsis = makensis

if not options.license:
    try:
        import pandac
        options.license = os.path.join(os.path.dirname(os.path.dirname(pandac.__file__)), "LICENSE")
        if not os.path.isfile(options.license):
            options.license = None
    except: pass
    if not options.license:
        options.license = os.path.join("doc", "LICENSE")
        if not os.path.isfile(options.license):
            options.license = None
    if options.license:
        options.license = os.path.abspath(options.license)

if sys.platform == "win32" and not options.welcome_image:
    filename = os.path.join('models', 'plugin_images', 'installer.bmp')
    if not os.path.exists(filename):
        sys.exit("Couldn't find installer.bmp for welcome_image.")
    options.welcome_image = os.path.abspath(filename)

def parseDependenciesWindows(tempFile):
    """ Reads the indicated temporary file, the output from
    dumpbin /dependents, to determine the list of dll's this
    executable file depends on. """

    lines = open(tempFile, 'rU').readlines()
    li = 0
    while li < len(lines):
        line = lines[li]
        li += 1
        if line.find(' has the following dependencies') != -1:
            break

    if li < len(lines):
        line = lines[li]
        if line.strip() == '':
            # Skip a blank line.
            li += 1

    # Now we're finding filenames, until the next blank line.
    filenames = []
    while li < len(lines):
        line = lines[li]
        li += 1
        line = line.strip()
        if line == '':
            # We're done.
            return filenames
        filenames.append(line)

    # Hmm, we ran out of data.  Oh well.
    if not filenames:
        # Some parse error.
        return None

    # At least we got some data.
    return filenames

def parseDependenciesUnix(tempFile):
    """ Reads the indicated temporary file, the output from
    otool -XL or ldd, to determine the list of dll's this
    executable file depends on. """

    lines = open(tempFile, 'rU').readlines()
    filenames = []
    for l in lines:
        filenames.append(l.strip().split(' ', 1)[0])
    return filenames

def addDependencies(path, pathname, file, pluginDependencies, dependentFiles, required=True):
    """ Checks the named file for DLL dependencies, and adds any
    appropriate dependencies found into pluginDependencies and
    dependentFiles. """

    tempFile = tempfile.mktemp('.txt', 'p3d_')
    if sys.platform == "darwin":
        command = 'otool -XL "%s" >"%s"'
    elif sys.platform == "win32":
        command = 'dumpbin /dependents "%s" >"%s"'
    else:
        command = 'ldd "%s" >"%s"'
    command = command % (pathname, tempFile)
    try:
        os.system(command)
    except:
        pass
    filenames = None

    if os.path.isfile(tempFile):
        if sys.platform == "win32":
            filenames = parseDependenciesWindows(tempFile)
        else:
            filenames = parseDependenciesUnix(tempFile)
        os.unlink(tempFile)
    if filenames is None:
        sys.exit("Unable to determine dependencies from %s" % (pathname))

    # Look for MSVC[RP]*.dll, and MFC*.dll.  These dependent files
    # have to be included too.  Also, any Panda-based libraries, or
    # the Python DLL, should be included, in case panda3d.exe wasn't
    # built static.  The Panda-based libraries begin with "lib" and
    # are all lowercase, or start with libpanda/libp3d.
    for dfile in filenames:
        dfilelower = dfile.lower()
        if dfilelower not in dependentFiles:
            if dfilelower.startswith('msvc') or \
               dfilelower.startswith('mfc') or \
               dfilelower.startswith('zlib1') or \
               (dfile.startswith('lib') and dfile == dfilelower) or \
               dfilelower.startswith('libpanda') or \
               dfilelower.startswith('libp3d') or \
               dfilelower.startswith('python'):
                pathname = None
                for pitem in path:
                    pathname = os.path.join(pitem, dfile)
                    if os.path.exists(pathname):
                        break
                    pathname = None
                if not pathname:
                    if required:
                        sys.exit("Couldn't find %s." % (dfile))
                    sys.stderr.write("Warning: couldn't find %s." % (dfile))
                    continue
                pathname = os.path.abspath(pathname)
                dependentFiles[dfilelower] = pathname

                # Also recurse.
                addDependencies(path, pathname, file, pluginDependencies, dependentFiles)

        if dfilelower in dependentFiles and dfilelower not in pluginDependencies[file]:
            pluginDependencies[file].append(dfilelower)

def getDllVersion(filename):
    """ Returns the DLL version number in the indicated DLL, as a
    string of comma-separated integers.  Windows only. """

    # This relies on the VBScript program in the same directory as
    # this script.
    thisdir = os.path.split(sys.argv[0])[0]
    versionInfo = os.path.join(thisdir, 'VersionInfo.vbs')
    tempfile = 'tversion.txt'
    tempdata = open(tempfile, 'w+')
    cmd = 'cscript //nologo "%s" "%s"' % (versionInfo, filename)
    print(cmd)
    result = subprocess.call(cmd, stdout = tempdata)
    if result:
        sys.exit(result)

    tempdata.seek(0)
    data = tempdata.read()
    tempdata.close()
    os.unlink(tempfile)
    return ','.join(data.strip().split('.'))


def makeCabFile(ocx, pluginDependencies):
    """ Creates an ActiveX CAB file.  Windows only. """

    ocxFullpath = findExecutable(ocx)
    cabFilename = os.path.splitext(ocx)[0] + '.cab'

    cabarc = 'cabarc'
    signcode = 'signcode'
    if options.mssdk:
        cabarc = options.mssdk + '/bin/cabarc'
        signcode = options.mssdk + '/bin/signcode'

    # First, we must generate an INF file.
    infFile = 'temp.inf'
    inf = open(infFile, 'w')

    info.write('[Add.Code]\n%s=%s\n%s=%s\n' % (infFile, infFile, ocx, ocx))
    dependencies = pluginDependencies[ocx]
    for filename in dependencies:
        inf.write('%s=%s\n' % (filename, filename))
    inf.write('\n[%s]\nfile=thiscab\n' % (infFile))
    inf.write('\n[%s]\nfile=thiscab\nclsid={924B4927-D3BA-41EA-9F7E-8A89194AB3AC}\nRegisterServer=yes\nFileVersion=%s\n' % (ocx, getDllVersion(ocxFullpath)))

    fullpaths = []
    for filename in dependencies:
        fullpath = findExecutable(filename)
        fullpaths.append(fullpath)
        inf.write('\n[%s]\nfile=thiscab\nDestDir=11\nRegisterServer=yes\nFileVersion=%s\n' % (filename, getDllVersion(fullpath)))
    inf.close()

    # Now process the inf file with cabarc.
    try:
        os.unlink(cabFilename)
    except OSError:
        pass

    cmd = '"%s" -s 6144 n "%s"' % (cabarc, cabFilename)
    for fullpath in fullpaths:
        cmd += ' "%s"' % (fullpath)
    cmd += ' "%s" %s' % (ocxFullpath, infFile)
    print(cmd)
    result = subprocess.call(cmd)
    if result:
        sys.exit(result)
    if not os.path.exists(cabFilename):
        print("Couldn't generate %s" % (cabFilename))
        sys.exit(1)

    print("Successfully generated %s" % (cabFilename))

    if options.spc and options.pvk:
        # Now we have to sign the cab file.
        cmd = '"%s" -spc "%s" -k "%s" "%s"' % (signcode, options.spc, options.pvk, cabFilename)
        print(cmd)
        result = subprocess.call(cmd)
        if result:
            sys.exit(result)

def makeInstaller():
    # Locate the plugin(s).
    pluginFiles = {}
    pluginDependencies = {}
    dependentFiles = {}

    # These are the primary files that make
    # up the plugin/runtime.
    if sys.platform == "darwin":
        npapi = 'nppanda3d.plugin'
        panda3d = 'panda3d'
        panda3dapp = 'Panda3D.app'
        baseFiles = [npapi, panda3d, panda3dapp]
    elif sys.platform == 'win32':
        ocx = 'p3dactivex.ocx'
        npapi = 'nppanda3d.dll'
        panda3d = 'panda3d.exe'
        panda3dw = 'panda3dw.exe'
        baseFiles = [ocx, npapi, panda3d, panda3dw]
    else:
        baseFiles = []

    path = []
    pathsep = ':'
    if sys.platform == "win32":
        pathsep = ';'
    if 'PATH' in os.environ:
        path += os.environ['PATH'].split(pathsep)
    if sys.platform != "win32" and 'LD_LIBRARY_PATH' in os.environ:
        path += os.environ['LD_LIBRARY_PATH'].split(pathsep)
    if sys.platform == "darwin" and 'DYLD_LIBRARY_PATH' in os.environ:
        path += os.environ['DYLD_LIBRARY_PATH'].split(pathsep)
    path += os.defpath.split(pathsep)
    for file in baseFiles:
        pathname = None
        for pitem in path:
            pathname = os.path.join(pitem, file)
            if os.path.exists(pathname):
                break
            pathname = None
        if not pathname:
            sys.exit("Couldn't find %s." % (file))

        pathname = os.path.abspath(pathname)
        pluginFiles[file] = pathname
        pluginDependencies[file] = []

        if sys.platform == "win32":
            # Also look for the dll's that these plugins reference.
            addDependencies(path, pathname, file, pluginDependencies, dependentFiles)

    if sys.platform == "darwin":
        tmproot = "/var/tmp/Panda3D Runtime/"

        # Apparently, we have to rename this package with each
        # version, or Snow Leopard won't think the versions are
        # increasing.  I don't really understand why this is so.  It
        # might be related to the use of the Tiger PackageMaker's
        # output being run on Snow Leopard.  Whatever.  Numbering the
        # package files works around the problem and doesn't seem to
        # cause additional problems, so we'll do that.
        pkgname = 'p3d-setup-%s.pkg' % (options.version)

        if os.path.exists(tmproot):
            shutil.rmtree(tmproot)
        if os.path.isfile(pkgname):
            os.remove(pkgname)
        elif os.path.isdir(pkgname):
            shutil.rmtree(pkgname)
        if not os.path.exists(tmproot):
            os.makedirs(tmproot)
        dst_npapi = os.path.join(tmproot, "Library", "Internet Plug-Ins", npapi)
        dst_panda3d = os.path.join(tmproot, "usr", "local", "bin", panda3d)
        dst_panda3dapp = os.path.join(tmproot, "Applications", panda3dapp)
        if not os.path.exists(dst_npapi): os.makedirs(os.path.dirname(dst_npapi))
        if not os.path.exists(dst_panda3d): os.makedirs(os.path.dirname(dst_panda3d))
        if not os.path.exists(dst_panda3dapp): os.makedirs(os.path.dirname(dst_panda3dapp))
        shutil.copytree(pluginFiles[npapi], dst_npapi)
        shutil.copyfile(pluginFiles[panda3d], dst_panda3d)
        os.chmod(dst_panda3d, 493) # 0o755
        shutil.copytree(pluginFiles[panda3dapp], dst_panda3dapp)

        tmpresdir = tempfile.mktemp('', 'p3d-resources')
        if os.path.exists(tmpresdir):
            shutil.rmtree(tmpresdir)
        os.makedirs(tmpresdir)
        if options.license:
            shutil.copyfile(options.license, os.path.join(tmpresdir, "License.txt"))

        package_id = 'org.panda3d.pkg.runtime' #TODO: maybe more customizable?

        infoFilename = None
        descriptionFilename = None
        packagemaker = "/Applications/Xcode.app/Contents/Applications/PackageMaker.app/Contents/MacOS/PackageMaker"
        if not os.path.exists(packagemaker):
            packagemaker = "/Developer/usr/bin/packagemaker"

        if os.path.exists(packagemaker):
            # PackageMaker 3.0 or better, e.g. OSX 10.5.
            CMD = packagemaker
            CMD += ' --id "%s"' % package_id
            CMD += ' --version "%s"' % options.version
            CMD += ' --title "%s"' % options.long_name
            CMD += ' --out "%s"' % (pkgname)
            CMD += ' --target 10.5' # The earliest version of OSX supported by Panda
            CMD += ' --domain system'
            CMD += ' --root "%s"' % tmproot
            CMD += ' --resources "%s"' % tmpresdir
            CMD += ' --no-relocate'
        else:
            # PackageMaker 2.0, e.g. OSX 10.4.
            packagemaker = "/Developer/Tools/packagemaker"
            infoFilename = '/tmp/Info_plist'
            info = open(infoFilename, 'w')
            info.write(Info_plist % {
                'package_id' : package_id,
                'version' : options.version,
                })
            info.close()
            descriptionFilename = '/tmp/Description_plist'
            description = open(descriptionFilename, 'w')
            description.write(Description_plist % {
                'long_name' : options.long_name,
                'short_name' : options.short_name,
                })
            description.close()
            CMD = packagemaker
            CMD += ' -build'
            CMD += ' -f "%s"' % (tmproot)
            CMD += ' -r "%s"' % (tmpresdir)
            CMD += ' -p "%s"' % (pkgname)
            CMD += ' -i "%s"' % (infoFilename)
            CMD += ' -d "%s"' % (descriptionFilename)

        print("")
        print(CMD)

        # Don't check the exit status of packagemaker; it's not always
        # reliable.
        subprocess.call(CMD, shell = True)
        shutil.rmtree(tmproot)

        if infoFilename:
            os.unlink(infoFilename)
        if descriptionFilename:
            os.unlink(descriptionFilename)
        if os.path.exists(tmpresdir):
            shutil.rmtree(tmpresdir)

        if not os.path.exists(pkgname):
            print("Unable to create %s." % (pkgname))
            sys.exit(1)

        # Pack the .pkg into a .dmg
        if not os.path.exists(tmproot): os.makedirs(tmproot)
        if os.path.isdir(pkgname):
            shutil.copytree(pkgname, os.path.join(tmproot, pkgname))
        else:
            shutil.copyfile(pkgname, os.path.join(tmproot, pkgname))

        tmpdmg = tempfile.mktemp('', 'p3d-setup') + ".dmg"
        CMD = 'hdiutil create "%s" -srcfolder "%s"' % (tmpdmg, tmproot)
        print("")
        print(CMD)
        result = subprocess.call(CMD, shell = True)
        if result:
            sys.exit(result)
        shutil.rmtree(tmproot)

        # Compress the .dmg (and make it read-only)
        if os.path.exists("p3d-setup.dmg"):
            os.remove("p3d-setup.dmg")
        CMD = 'hdiutil convert "%s" -format UDBZ -o "p3d-setup.dmg"' % tmpdmg
        print("")
        print(CMD)
        result = subprocess.call(CMD, shell = True)
        if result:
            sys.exit(result)

    elif sys.platform == 'win32':
        # Now build the NSIS command.
        CMD = "\"" + options.nsis + "\" /V3 "
        CMD += '/DPRODUCT_NAME="' + options.long_name + '" '
        CMD += '/DPRODUCT_NAME_SHORT="' + options.short_name + '" '
        CMD += '/DPRODUCT_PUBLISHER="' + options.publisher + '" '
        CMD += '/DPRODUCT_WEB_SITE="' + options.website + '" '
        CMD += '/DPRODUCT_VERSION="' + options.version + '" '
        CMD += '/DINSTALL_DIR="' + options.install_dir + '" '
        CMD += '/DLICENSE_FILE="' + options.license + '" '
        CMD += '/DOCX="' + ocx + '" '
        CMD += '/DOCX_PATH="' + pluginFiles[ocx] + '" '
        CMD += '/DNPAPI="' + npapi + '" '
        CMD += '/DNPAPI_PATH="' + pluginFiles[npapi] + '" '
        CMD += '/DPANDA3D="' + panda3d + '" '
        CMD += '/DPANDA3D_PATH="' + pluginFiles[panda3d] + '" '
        CMD += '/DPANDA3DW="' + panda3dw + '" '
        CMD += '/DPANDA3DW_PATH="' + pluginFiles[panda3dw] + '" '

        if options.regview:
            CMD += '/DREGVIEW=%s ' % (options.regview)

        for i, dep in enumerate(dependentFiles.items()):
            CMD += '/DDEP%s="%s" ' % (i, dep[0])
            CMD += '/DDEP%sP="%s" ' % (i, dep[1])

        for i, dep in enumerate(pluginDependencies[npapi]):
            CMD += '/DNPAPI_DEP%s="%s" ' % (i, dep)

        if options.start:
            CMD += '/DADD_START_MENU '

        if options.welcome_image:
            CMD += '/DMUI_WELCOMEFINISHPAGE_BITMAP="' + options.welcome_image + '" '
            CMD += '/DMUI_UNWELCOMEFINISHPAGE_BITMAP="' + options.welcome_image + '" '
        if options.install_icon:
            CMD += '/DINSTALL_ICON="' + options.install_icon + '" '

        CMD += '"' + this_dir + '\\p3d_installer.nsi"'

        print("")
        print(CMD)
        print("packing...")
        result = subprocess.call(CMD)
        if result:
            sys.exit(result)

        if options.cab:
            # Generate a CAB file and optionally sign it.
            makeCabFile(ocx, pluginDependencies)

makeInstaller()
