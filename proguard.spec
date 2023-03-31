%{?_javapackages_macros:%_javapackages_macros}
Name:           proguard
Version:        5.1
Release:        1.4
Summary:        Java class file shrinker, optimizer, obfuscator and preverifier
Group:		Development/Java

License:        GPLv2+
URL:            http://proguard.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}%{version}.tar.gz
Source1:        %{name}.desktop
Source2:        README.dist

BuildRequires:  jpackage-utils
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  ant
Requires:       jpackage-utils
Requires:       java >= 1:1.6.0

BuildArch:      noarch

%description
ProGuard is a free Java class file shrinker, optimizer, obfuscator and 
preverifier. It detects and removes unused classes, fields, methods, and 
attributes. It optimizes bytecode and removes unused instructions. It 
renames the remaining classes, fields, and methods using short meaningless 
names. Finally, it preverifies the processed code for Java 6 or for Java 
Micro Edition. 

%package manual
Summary:        Manual for %{name}
Requires:       jpackage-utils

%description manual
The manual for %{name}.

%package gui
Summary:        GUI for %{name}
# we convert the favicon.ico to png files of different sizes, so we require
# ImageMagick
BuildRequires:  imagemagick
BuildRequires:  desktop-file-utils
Requires:       jpackage-utils
Requires:       %{name} = %{version}-%{release}

%description gui
A GUI for %{name}.

%prep
%setup -qn %{name}%{version}

# remove all jar and class files, the snippet from Packaging:Java does 
# not work
find -name '*.jar' -exec rm -f '{}' \;
find -name '*.class' -exec rm -f '{}' \;

# remove the Class-Path from MANIFESTs
sed -i '/class-path/I d' src/%{name}/gui/MANIFEST.MF
sed -i '/class-path/I d' src/%{name}/retrace/MANIFEST.MF

# this will create three png files from the favicon that contains multiple size 
# icons: 0: 48x48, 1: 32x32, 2: 16x16
convert docs/favicon.ico %{name}.png
cp -p %{name}-0.png %{name}48.png
cp -p %{name}-1.png %{name}32.png
cp -p %{name}-2.png %{name}16.png

# add README.dist
cp -p %{SOURCE2} .

%build
cd build/
# build ProGuard, ProGuardGUI, retrace and anttask
ant -Dant.jar=%{_javadir}/ant.jar basic anttask

%install
mkdir -p ${RPM_BUILD_ROOT}%{_javadir}/%{name}/
cp -p lib/%{name}.jar ${RPM_BUILD_ROOT}%{_javadir}/%{name}/%{name}.jar
cp -p lib/%{name}gui.jar ${RPM_BUILD_ROOT}%{_javadir}/%{name}/%{name}gui.jar
cp -p lib/retrace.jar ${RPM_BUILD_ROOT}%{_javadir}/%{name}/retrace.jar

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
%jpackage_script proguard.ProGuard "" "" proguard proguard true
%jpackage_script proguard.gui.ProGuardGUI "" "" proguard proguard-gui true
%jpackage_script proguard.retrace.ReTrace "" "" proguard proguard-retrace true

#install the desktop file for proguard-gui
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications %{SOURCE1}

#copy icons
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/48x48/apps
cp -p %{name}48.png ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/32x32/apps
cp -p %{name}32.png ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/16x16/apps
cp -p %{name}16.png ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png

%post
# update icon cache
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%postun
# update icon cache
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%files
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/proguard.jar
%{_javadir}/%{name}/retrace.jar
%{_bindir}/proguard
%{_bindir}/proguard-retrace
%doc README examples/ README.dist

%files manual
%doc docs/*

%files gui
%{_bindir}/%{name}-gui
%{_javadir}/%{name}/proguardgui.jar
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/*/*/apps/*

%changelog
* Wed Nov 05 2014 François Kooman <fkooman@tuxed.net> - 5.1-1
- update to 5.1

* Fri Aug 22 2014 François Kooman <fkooman@tuxed.net> - 5.0-1
- update to 5.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 07 2014 Michael Simacek <msimacek@redhat.com> - 4.11-2
- Adapt to current packaging guidelines (rhbz#1022159)

* Mon Dec 30 2013 François Kooman <fkooman@tuxed.net> - 4.11-1
- update to 4.11

* Tue Aug 13 2013 F. Kooman <fkooman@tuxed.net> - 4.10-2
- forgot to remove old patch completely

* Tue Aug 13 2013 F. Kooman <fkooman@tuxed.net> - 4.10-1
- update to 4.10

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 20 2013 F. Kooman <fkooman@tuxed.net> - 4.9-2
- bump spec

* Wed Mar 20 2013 F. Kooman <fkooman@tuxed.net> - 4.9-1
- update to 4.9

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 24 2013 F. Kooman <fkooman@tuxed.net> - 4.8-2
- bump spec

* Tue Sep 04 2012 F. Kooman <fkooman@tuxed.net> - 4.8-1
- update to 4.8

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 28 2012 F. Kooman <fkooman@tuxed.net> - 4.7-1
- update to 4.7

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 13 2011 F. Kooman <fkooman@tuxed.net> - 4.6-1
- update to 4.6

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 15 2010 François Kooman <fkooman@tuxed.net> - 4.5.1-1
- update to 4.5.1

* Fri Jun 11 2010 François Kooman <fkooman@tuxed.net> - 4.5-3
- rename proguardgui to proguard-gui (and update .desktop file)
- rename retrace to proguard-retrace
- update README.dist to reflect these changes

* Tue Jun 08 2010 François Kooman <fkooman@tuxed.net> - 4.5-2
- permission fix no longer needed

* Mon Jun  7 2010 François Kooman <fkooman@tuxed.net> - 4.5-1
- update to 4.5 (see http://proguard.sourceforge.net/downloads.html)
- remove GCJ bits as GUI doesn't work with GCJ

* Sun Jan 10 2010 François Kooman <fkooman@tuxed.net> - 4.4-5
- own directory /usr/share/java/proguard
- don't include proguardgui.jar in proguard main package

* Thu Sep  3 2009 François Kooman <fkooman@tuxed.net> - 4.4-4
- create a subpackage for the GUI

* Wed Jul 29 2009 François Kooman <fkooman@tuxed.net> - 4.4-3
- put the manual in a sub package
- fix permissions of launch scripts to 0755 instead of +x to fix rpmlint 
  warning

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 François Kooman <fkooman@tuxed.net> - 4.4-1
- update to ProGuard 4.4

* Wed Jun 10 2009 François Kooman <fkooman@tuxed.net> - 4.3-4
- move creation of icon inside spec
- add GenericName key in .desktop file for KDE users
- make the jar files versioned and create unversioned symlinks to them

* Tue Jun 9 2009 François Kooman <fkooman@tuxed.net> - 4.3-3
- more consistent use of name macro, consistent RPM_BUILD_ROOT variable naming
- indicate that proguard is a directory in files section
- remove redundant attr macro for gcj in files section
- require Java >=1.5
- Use favicon as icon for ProGuard
- keep timestamps when copying files

* Mon Jun 8 2009 François Kooman <fkooman@tuxed.net> - 4.3-2
- add .desktop file + requires
- describe why there are launch scripts included 
- add a README.dist describing how to use ProGuard now that it is packaged
- add GCJ AOT stuff

* Sat Jun 6 2009 François Kooman <fkooman@tuxed.net> - 4.3-1
- Initial Fedora package

