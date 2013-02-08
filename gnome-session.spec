Summary:	The gnome desktop programs for the GNOME GUI desktop environment
Name:		gnome-session
Version:	3.6.2
Release:	2
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/softwaremap/projects/gnome-session/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/3.6/%{name}-%{version}.tar.xz
Patch0:		gnome-session-llvmpipe.patch
Source1:	gnome-session-startgnome
Source2:	gnome-session-gnomerc
Source3:	gnome-session-startgnomeclassic

BuildRequires:	desktop-file-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool >= 0.40.0
BuildRequires:	xmlto
BuildRequires:	pkgconfig(dbus-glib-1) >= 0.76
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gio-2.0) >= 2.28.0
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glib-2.0) >= 2.28.0
BuildRequires:	pkgconfig(gtk+-3.0) >= 2.90.7
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(json-glib-1.0) >= 0.10
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(upower-glib) >= 0.9.0
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	x11-xtrans-devel
BuildRequires:	tcp_wrappers-devel

Requires:	GConf2 >= 1.2.1
Requires:	desktop-common-data
Requires:	gnome-user-docs
Requires:	gnome-settings-daemon
Requires:	%{name}-bin >= %{version}-%{release}

%description
GNOME (GNU Network Object Model Environment) is a user-friendly
set of applications and desktop tools to be used in conjunction with a
window manager for the X Window System.

The GNOME Session Manager restores a set session (group of applications)
when you log into GNOME.

%package bin
Group: %{group}
Summary: %{summary}
Conflicts: gnome-session < 2.30.2-2mdv

%description bin
This package contains the binaries for the GNOME Session Manager, but 
no startup scripts. It is meant for applications such as GDM that use 
gnome-session internally.

%prep
%setup -q
%apply_patches

%build
%configure2_5x

%make

%install
%makeinstall_std

# wmsession session file
mkdir -p %{buildroot}%{_sysconfdir}/X11/wmsession.d
cat << EOF > %{buildroot}%{_sysconfdir}/X11/wmsession.d/02GNOME
NAME=GNOME
ICON=gnome-logo-icon-transparent.png
DESC=GNOME Environment
EXEC=%{_bindir}/startgnome
SCRIPT:
exec %{_bindir}/startgnome
EOF

cat << EOF > %{buildroot}%{_sysconfdir}/X11/wmsession.d/03GNOMECLASSIC
NAME=Gnome Classic
ICON=gnome-logo-icon-transparent.png
DESC=GNOME 3 with separate panel and window manager
EXEC=%{_bindir}/startgnomeclassic
SCRIPT:
exec %{_bindir}/startgnomeclassic
EOF

desktop-file-install --vendor="" \
	--add-category="X-MandrivaLinux-System-Configuration-GNOME-Advanced" \
	--add-category="GTK" \
	--add-category="GNOME" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

install -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/startgnome
install -m 0755 %{SOURCE3} %{buildroot}%{_bindir}/startgnomeclassic

mkdir -p %{buildroot}%{_sysconfdir}/gnome
install -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/gnome/gnomerc
# gw these produce rpmlint errors:
rm -rf %{buildroot}%{_datadir}/locale/{be@latin}
%find_lang %{name}-3.0

# remove unpackaged files
rm -rf %{buildroot}%{_datadir}/xsessions

%post
if [ "$1" = "2" -a -r /etc/sysconfig/desktop ]; then
  sed -i -e "s|^DESKTOP=Gnome$|DESKTOP=GNOME|g" /etc/sysconfig/desktop
fi
%{make_session}

%postun
%{make_session}

%files bin
%{_bindir}/gnome-session
%{_datadir}/glib-2.0/schemas/org.gnome.SessionManager.gschema.xml
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/gnome-session.*

%files -f %{name}-3.0.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/*
%{_sysconfdir}/gnome/gnomerc
%{_bindir}/startgnome
%{_bindir}/startgnomeclassic
%{_bindir}/gnome-session-properties
%{_bindir}/gnome-session-quit
%{_libdir}/gnome-session-check-accelerated
%{_libdir}/gnome-session-check-accelerated-helper
%{_datadir}/applications/*
%{_datadir}/GConf/gsettings/gnome-session.convert
%{_mandir}/man1/gnome-session-properties.*
%{_mandir}/man1/gnome-session-quit.*



%changelog
* Tue Nov 13 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.2-1
- update to 3.6.2

* Tue Oct 30 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.1-1
- update to 3.6.1

* Fri Oct 12 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.0-2
- add patch to unblacklist llvmpipe

* Thu Oct  4 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.0-1
- update to 3.6.0

* Thu May 24 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.4.2.1-1
+ Revision: 800482
- update to new version 3.4.2.1

* Wed May 16 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.4.2-1
+ Revision: 799223
- update to new version 3.4.2

* Sun Apr 29 2012 Guilherme Moro <guilherme@mandriva.com> 3.4.1-1
+ Revision: 794409
- Updated to version 3.4.1

* Mon Mar 05 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.2.1-1
+ Revision: 782227
- new version 3.2.1
- added S3 from mga
- cleaned up spec

* Sun May 08 2011 Funda Wang <fwang@mandriva.org> 2.32.1-2
+ Revision: 672445
- br sm

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Wed Nov 17 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.32.1-1mdv2011.0
+ Revision: 598366
- update to new version 2.32.1

* Mon Sep 27 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.32.0-1mdv2011.0
+ Revision: 581286
- update to new version 2.32.0

* Wed Aug 04 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.31.6-1mdv2011.0
+ Revision: 565809
- new version
- drop splash screen
- update file list

* Fri Jul 30 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.31.2-1mdv2011.0
+ Revision: 563376
- new version

* Wed Jun 30 2010 Frederic Crozat <fcrozat@mandriva.com> 2.30.2-2mdv2010.1
+ Revision: 549698
- move icons to bin subpackage

* Tue Jun 22 2010 Frederic Crozat <fcrozat@mandriva.com> 2.30.2-1mdv2010.1
+ Revision: 548563
- Release 2.30.2

* Wed Apr 28 2010 Frederic Crozat <fcrozat@mandriva.com> 2.30.0-3mdv2010.1
+ Revision: 540308
- Update splash
- remove obsolete buildrequirements

* Wed Mar 31 2010 Frederic Crozat <fcrozat@mandriva.com> 2.30.0-2mdv2010.1
+ Revision: 530356
- Split package so gdm only requires a subset (Mdv bug #58443)
- remove unneeded dependencies

* Tue Mar 30 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.30.0-1mdv2010.1
+ Revision: 528962
- update to new version 2.30.0
- update build deps

  + Funda Wang <fwang@mandriva.org>
    - update BR's name

* Tue Mar 09 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.29.92-1mdv2010.1
+ Revision: 516898
- update to new version 2.29.92

* Wed Jan 27 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.29.6-1mdv2010.1
+ Revision: 497253
- new version
- drop patch 11

* Wed Dec 30 2009 Pascal Terjan <pterjan@mandriva.org> 2.28.0-5mdv2010.1
+ Revision: 484000
- Update BuildRequires

* Thu Oct 29 2009 Frederic Crozat <fcrozat@mandriva.com> 2.28.0-4mdv2010.0
+ Revision: 460078
- Update splash to 2.28

* Mon Oct 26 2009 Frederic Crozat <fcrozat@mandriva.com> 2.28.0-3mdv2010.0
+ Revision: 459363
- Patch10: fix crash at logout (GNOME bug #590828)
- Patch11: fix crash in xsmp_stop (GNOME bug #598211)

* Mon Sep 21 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.28.0-1mdv2010.0
+ Revision: 446790
- update to new version 2.28.0

* Mon Sep 14 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.27.92-1mdv2010.0
+ Revision: 439657
- update file list
- new version

* Tue Aug 25 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.27.91-1mdv2010.0
+ Revision: 421108
- new version
- update file list

* Wed Jul 29 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.27.5-1mdv2010.0
+ Revision: 402914
- update build deps
- new version
- rediff patch 6
- drop patch 10
- fix build
- update deps

* Wed Jul 15 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.27.4-1mdv2010.0
+ Revision: 396378
- update to new version 2.27.4

* Wed Jul 01 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.26.2-1mdv2010.0
+ Revision: 391232
- new version
- rediff patch 9

* Tue Apr 14 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.26.1-1mdv2009.1
+ Revision: 367219
- update to new version 2.26.1

* Tue Apr 14 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.26.0.90-1mdv2009.1
+ Revision: 367002
- new version
- drop patch 11

* Tue Mar 31 2009 Frederic Crozat <fcrozat@mandriva.com> 2.26.0-2mdv2009.1
+ Revision: 363051
- Patch11 (SVN): bring back session saving (aka vuntz rocks)

* Mon Mar 16 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.26.0-1mdv2009.1
+ Revision: 356296
- update to new version 2.26.0

  + Frederic Crozat <fcrozat@mandriva.com>
    - Update splash

* Tue Mar 03 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.92-1mdv2009.1
+ Revision: 348013
- update to new version 2.25.92
- remove old configure options

* Tue Feb 17 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.91-1mdv2009.1
+ Revision: 341216
- update to new version 2.25.91

* Tue Feb 03 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.90-1mdv2009.1
+ Revision: 336936
- new version
- update file list

* Tue Jan 20 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.5-1mdv2009.1
+ Revision: 331531
- update build deps
- update to new version 2.25.5

* Thu Dec 18 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.3-1mdv2009.1
+ Revision: 315823
- update to new version 2.25.3

* Tue Dec 02 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.2-1mdv2009.1
+ Revision: 309075
- update to new version 2.25.2

* Tue Nov 25 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.24.2-1mdv2009.1
+ Revision: 306723
- update to new version 2.24.2

* Mon Nov 03 2008 Frederic Crozat <fcrozat@mandriva.com> 2.24.1-2mdv2009.1
+ Revision: 299496
- Add x11-xtrans-devel to buildrequires, should fix tcp port being opened by gnome-session

* Wed Oct 22 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.24.1-1mdv2009.1
+ Revision: 296439
- update to new version 2.24.1

* Tue Sep 23 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.24.0-1mdv2009.0
+ Revision: 287291
- new version
- drop patch 11

* Wed Sep 10 2008 Frederic Crozat <fcrozat@mandriva.com> 2.23.92-2mdv2009.0
+ Revision: 283526
- Patch11: fix displaying username in non-UTF8 locales

* Tue Sep 09 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.92-1mdv2009.0
+ Revision: 282914
- new version
- update patch 10
- drop patch 11

* Tue Sep 02 2008 Frederic Crozat <fcrozat@mandriva.com> 2.23.91-2mdv2009.0
+ Revision: 279172
- Patch10, Source4: fix gnome-wm startup
- Patch11: fix default session failsafe (SVN)

* Tue Sep 02 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.91-1mdv2009.0
+ Revision: 278811
- new version
- drop patches 10,11,12

* Fri Aug 29 2008 Frederic Crozat <fcrozat@mandriva.com> 2.23.90-3mdv2009.0
+ Revision: 277263
- Patch12 (Ghee Teo): restore GNOME_DESKTOP_SESSION_ID env variable (GNOME bug #542880)

* Fri Aug 22 2008 Frederic Crozat <fcrozat@mandriva.com> 2.23.90-2mdv2009.0
+ Revision: 275078
- Patch10: make sure non-fatal init errors are not fatal (Mdv bug #43029) (GNOME bug #548980)
- Patch11: don't set a11y gtk moduels if a11y registry could not be started (GNOME bug #548982)

* Wed Aug 20 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.90-1mdv2009.0
+ Revision: 274373
- new version
- drop patch 10

* Tue Aug 19 2008 Frederic Crozat <fcrozat@mandriva.com> 2.23.6-4mdv2009.0
+ Revision: 273922
- Update to new splash for GNOME 2.24
- Update patch6 to enable splash
- Patch10: autohide splash after last client tiemouts (GNOME bug #546410)

* Wed Aug 06 2008 Frederic Crozat <fcrozat@mandriva.com> 2.23.6-3mdv2009.0
+ Revision: 264325
- Remove login/logout sounds, handled by libcanberra now

* Tue Aug 05 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.6-2mdv2009.0
+ Revision: 263873
- fix patch application

  + Frederic Crozat <fcrozat@mandriva.com>
    - Patch review :
     - remove patches 3 (handled with autostart), 4 (no longer needed),
      8 (obsolete), 13 (obsolete), 14 (obsolete), 16 (obsolete)
     - regenerate patch9

* Tue Aug 05 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.6-1mdv2009.0
+ Revision: 263727
- new version
- drop patches 17 and 18

* Thu Jul 24 2008 Frederic Crozat <fcrozat@mandriva.com> 2.23.5-2mdv2009.0
+ Revision: 245398
- Patch18: allow to really disable login sound (GNOME bug #544540)

* Wed Jul 23 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.5-1mdv2009.0
+ Revision: 241901
- new version
- drop patch 18

* Tue Jul 22 2008 Frederic Crozat <fcrozat@mandriva.com> 2.23.4.1-3mdv2009.0
+ Revision: 240215
- Patch18: dither splash background (GNOME bug #544159)

* Mon Jul 21 2008 Frederic Crozat <fcrozat@mandriva.com> 2.23.4.1-2mdv2009.0
+ Revision: 239333
- Patch17: use new dbus activation sesion environment API (GNOME bug #360475)

* Fri Jul 04 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.4.1-1mdv2009.0
+ Revision: 231421
- fix buildrequires
- new version
- update deps
- disable patches 3,4,13,14,16
- update file list

* Mon Jun 30 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.22.3-1mdv2009.0
+ Revision: 230185
- new version
- drop patch 11
- update buildrequires
- update license

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Tue May 27 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.22.2-1mdv2009.0
+ Revision: 211638
- new version

* Thu Apr 10 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.22.1.1-1mdv2009.0
+ Revision: 192554
- new version

* Tue Mar 25 2008 Frederic Crozat <fcrozat@mandriva.com> 2.22.0-2mdv2008.1
+ Revision: 189962
- Do not ship xsession file, we use chksession instead (Mdv bug #39196)

* Mon Mar 10 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.22.0-1mdv2008.1
+ Revision: 183851
- new version

* Thu Mar 06 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.93-1mdv2008.1
+ Revision: 180931
- new version
- drop patch 15

* Thu Feb 28 2008 Frederic Crozat <fcrozat@mandriva.com> 2.21.92-2mdv2008.1
+ Revision: 176404
- Replace dependency on mandrake_desk with desktop-common-data

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - new version
    - bump deps

* Mon Feb 25 2008 Olivier Blin <blino@mandriva.org> 2.21.91-3mdv2008.1
+ Revision: 174936
- require GConf2-sanity-check (which has been split out of GConf2)

* Wed Feb 20 2008 Frederic Crozat <fcrozat@mandriva.com> 2.21.91-2mdv2008.1
+ Revision: 173222
- Update splash for Mandriva 2008.1

* Mon Feb 11 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.91-1mdv2008.1
+ Revision: 165451
- fix installation
- new version
- rediff patch 15
- remove invalid locales

* Mon Jan 28 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.90-1mdv2008.1
+ Revision: 159051
- new version
- update deps

* Tue Jan 15 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.5-1mdv2008.1
+ Revision: 152133
- new version
- drop patch 12
- update file list

* Tue Jan 08 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.20.3-1mdv2008.1
+ Revision: 146379
- new version

* Thu Jan 03 2008 Frederic Crozat <fcrozat@mandriva.com> 2.20.2-2mdv2008.1
+ Revision: 143979
- Patch16 (Fedora): always enable sound server (since we use PulseAudio)
- Update source2 to fix typo in linc-cleanup-socket test, preventing it from running

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Nov 27 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.20.2-1mdv2008.1
+ Revision: 113320
- new version

* Mon Oct 15 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.20.1-1mdv2008.1
+ Revision: 98658
- new version

* Fri Sep 21 2007 Frederic Crozat <fcrozat@mandriva.com> 2.20.0-2mdv2008.0
+ Revision: 91770
- Patch15: fix login/logout sound events (GNOME bug #466458)

* Wed Sep 19 2007 Frederic Crozat <fcrozat@mandriva.com> 2.20.0-1mdv2008.0
+ Revision: 90439
- Patch13 (Ubuntu): don't fade logout on LTSP client
- Patch14 (Ubuntu): prevent splash from staying too long on screen

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - new version

* Thu Sep 13 2007 Frederic Crozat <fcrozat@mandriva.com> 2.19.92-3mdv2008.0
+ Revision: 85271
- Patch12 (Fedora): fix ICE mem leak
- Remove eggcups from default session, use xdg autostart instead

* Fri Sep 07 2007 Frederic Crozat <fcrozat@mandriva.com> 2.19.92-2mdv2008.0
+ Revision: 81786
- Ensure session preferences menu entry is only visible in GNOME preferences menu

* Tue Sep 04 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.92-1mdv2008.0
+ Revision: 79455
- new version

* Tue Aug 28 2007 Frederic Crozat <fcrozat@mandriva.com> 2.19.90-2mdv2008.0
+ Revision: 72584
- New splash for GNOME 2.20 / Mdv 2008.0 (it isn't released yet :)

* Tue Aug 14 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.90-1mdv2008.0
+ Revision: 63244
- new version

* Mon Jul 30 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.6-1mdv2008.0
+ Revision: 56706
- fix buildrequires
- new version

* Sun Jul 08 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.5-1mdv2008.0
+ Revision: 49938
- new version

* Mon Jun 18 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.4-1mdv2008.0
+ Revision: 40693
- new version
- update patch 11
- new version
- drop patches 2,7.10
- fix buildrequires
- new version

  + Anssi Hannula <anssi@mandriva.org>
    - rebuild with correct optflags


* Thu Mar 15 2007 Frederic Crozat <fcrozat@mandriva.com> 2.18.0-3mdv2007.1
+ Revision: 144091
-bunzip scripts in svn
-update gnomerc script to run linc-cleanup-sockets before starting session
- Remove patch5 and update patch4 : Mandriva-Galaxy is now started by autostart

* Wed Mar 14 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.18.0-2mdv2007.1
+ Revision: 143777
- rename splash screen file and update patch 6
- update patch 4 for Mandriva Galaxy

* Mon Mar 12 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.18.0-1mdv2007.1
+ Revision: 142069
- new version

* Tue Mar 06 2007 Frederic Crozat <fcrozat@mandriva.com> 2.17.92-4mdv2007.1
+ Revision: 133636
- Improve splash corners

* Mon Mar 05 2007 Frederic Crozat <fcrozat@mandriva.com> 2.17.92-3mdv2007.1
+ Revision: 133232
- Updated splash

* Thu Mar 01 2007 Frederic Crozat <fcrozat@mandriva.com> 2.17.92-2mdv2007.1
+ Revision: 130604
- Patch11: increase timeout for a11y startup popup

* Mon Feb 26 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.92-1mdv2007.1
+ Revision: 126154
- new version

* Wed Feb 21 2007 Frederic Crozat <fcrozat@mandriva.com> 2.17.91-2mdv2007.1
+ Revision: 123809
- Patch10: handle shaped image for startup (GNOME bug #399262)
- Update splash

* Mon Feb 12 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.91-1mdv2007.1
+ Revision: 120193
- new version

* Fri Feb 09 2007 Frederic Crozat <fcrozat@mandriva.com> 2.17.90.1-2mdv2007.1
+ Revision: 118539
- Patch10: fix at-spi startup timeout (GNOME bug #345428)

* Mon Jan 22 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.90.1-1mdv2007.1
+ Revision: 111992
- new version
- drop patch 10

  + Frederic Crozat <fcrozat@mandriva.com>
    -Patch10 : fix default session filename

* Mon Jan 22 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.90-1mdv2007.1
+ Revision: 111672
- new version
- rediff patches 3 and 6
- add icons

* Tue Jan 09 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.5-1mdv2007.1
+ Revision: 106286
- new version

* Tue Dec 05 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.3-2mdv2007.1
+ Revision: 90736
- bot rebuild
- fix buildrequires
- new version

* Mon Nov 27 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.2-2mdv2007.1
+ Revision: 87646
- fix buildrequires
- new version

* Wed Nov 22 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.16.2-1mdv2007.1
+ Revision: 86239
- new version
- unpack patches

* Fri Oct 13 2006 Olivier Blin <oblin@mandriva.com> 2.16.1-2mdv2007.1
+ Revision: 63792
- adapt compiz patch to new compositing-wm-common package

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - Import gnome-session

* Fri Oct 06 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.16.1-1mdv2007.0
- New version 2.16.1

* Thu Sep 14 2006 Frederic Crozat <fcrozat@mandriva.com> 2.16.0-2mdv2007.0
- Patch9: allow to start compiz

* Tue Sep 05 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.16.0-1mdv2007.0
- New release 2.16.0

* Sat Sep 02 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.92-2mdv2007.0
- Improved splash screen

* Wed Aug 23 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.15.92-1mdv2007.0
- New release 2.15.92

* Sat Aug 19 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.91-3mdv2007.0
- Update source 3, enable patch6, new splash

* Fri Aug 18 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.91-2mdv2007.0
- update source2 to suppor new way of changing menu style
- fix mandriva category in .desktop

* Wed Aug 09 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.15.91-1mdv2007.0
- New release 2.15.91

* Fri Aug 04 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.90-2mdv2007.0
- Rebuild with latest dbus

* Wed Jul 26 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.15.90-1
- New release 2.15.90

* Tue Jul 18 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.4-2mdv2007.0
- Update source2 to correctly set XDG_CONFIG_DIRS

* Wed Jul 12 2006 Götz Waschk <waschk@mandriva.org> 2.15.4-1mdv2007.0-
- xdg menu
- update deps
- drop patch 9
- New release 2.15.4

* Tue Jun 20 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.1-3mdv2007.0
- Patch9 (CVS): fix warning in gnome-session-remove
- use new macros

* Fri Jun 09 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.1-2mdv2007.0
- Update patch5 to use correct name for mandriva-galaxy

* Wed May 31 2006 GÃ¶ttz Waschk <waschk@mandriva.org> 2.14.2-1mdv2007.0
- New release 2.14.2
- Remove patch10 (merged upstream)
- Patch10 (Fedora): don't crash apps on warningp

* Wed May 31 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.2-1mdv2007.0
- New release 2.14.2

* Sat May 20 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.1-4mdk
- Update patch3 to not start g-v-m (done with new autostart feature)

* Fri Apr 14 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.1-3mdk
- Release 2.14.1
- Remove patch9 (merged upstream)
- Disable patch6

* Fri Feb 24 2006 Frederic Crozat <fcrozat@mandriva.com> 2.12.0-3mdk
- Enable patch 6, update source 3, splash screen is back

* Sun Nov 20 2005 GÃ¶tz Waschk <waschk@mandriva.org> 2.12.0-2mdk
- rebuild for new openssl

* Thu Oct 06 2005 Frederic Crozat <fcrozat@mandriva.com> 2.12.0-1mdk
- Release 2.12.0
- Regenerate patch3 (gotz)
- Remove patch11 (merged upstream)

* Sat Sep 03 2005 GÃ¶tz Waschk <waschk@mandriva.org> 2.10.0-9mdk
- rebuild to remove glitz dep

* Fri Aug 19 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.0-8mdk
- Fix icon path

* Wed Aug 17 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.0-7mdk
- Patch11 (CVS): fix text rendering
- Remove patch8, replaced by patch 11

* Wed Aug 03 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.0-6mdk
- Enable patch 6, splash is back

* Fri Jul 29 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.0-5mdk 
- Regenerate patch3: remove gnome-smproxy, it is causing more problems 
  than it solves (Mdk bug #16870)

* Fri May 13 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.0-4mdk 
- Remove yelp dependency, so removing firefox won't remove gnome-session
  or gnome-panel

* Wed Apr 27 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.0-3mdk 
- Fix typo in source2

* Sat Apr 23 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.0-2mdk 
- Update source2 for new location of original menu files

* Wed Apr 20 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.0-1mdk 
- Release 2.10.0 (based on Götz Waschk package)
- disable patch 6

* Tue Mar 22 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.1-9mdk 
- New splash

* Wed Mar 16 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.1-8mdk 
- Enable patch6, new splash

* Tue Mar 08 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.1-7mdk 
- Update source2 to never touch BROWSER variable

* Fri Feb 18 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.1-6mdk 
- Patch10: really hide bad hostname dialog when it is ok (Mdk bug #12426)

* Wed Feb 16 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.1-5mdk 
- Update patch3 to start eggcups

* Fri Feb 11 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.1-4mdk 
- Update source2 to set XDG_CONFIG_DIRS if using original menu (Mdk bug #12971)
- Update patch3 to call gnome-volume-manager instead of magicdev

* Wed Jan 05 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.1-3mdk 
- Rebuild with latest howl

* Wed Nov 17 2004 Götz Waschk <waschk@linux-mandrake.com> 2.8.1-2mdk
- fix buildrequires

* Wed Oct 20 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.1-1mdk
- New release 2.8.1
- Remove patch9 (merged upstream)
- Disable patch 6
- Patch9 (Fedora): add autostart .desktop directory support

* Fri Oct 01 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.2-5mdk
- Patch9 (CVS): don't leak background pixbuf

* Thu Sep 02 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.2-4mdk
- Splash is back, enable patch6

* Thu Aug 05 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.2-3mdk
- Update source 2 to no longer start mdkapplet (handled by xinit now)

* Sat Jul 10 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.2-2mdk
- Update source 2 to use epiphany as default browser (otherwise galeon)

* Wed Jun 16 2004 Götz Waschk <waschk@linux-mandrake.com> 2.6.2-1mdk
- reenable libtoolize
- New release 2.6.2

* Thu Apr 22 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.1-2mdk
- Update patch 3 to fix bug 9462 (need to increment number of clients)

* Wed Apr 21 2004 Goetz Waschk <goetz@mandrakesoft.com> 2.6.1-1mdk
- New release 2.6.1

* Tue Apr 06 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.0-1mdk
- Release 2.6.0 (with Götz Waschk help)
- disable patch 6, use default gnome2.6 splash
- really fix patches 3,4

