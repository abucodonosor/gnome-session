%define  req_libgnomeui_version	2.1.0

Summary:        The gnome desktop programs for the GNOME GUI desktop environment
Name:           gnome-session
Version: 2.26.0
Release:        %mkrel 1
License:        GPLv2+
Group:          Graphical desktop/GNOME
Source0:        ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Source1:        gnome-session-startgnome
Source2:	gnome-session-gnomerc
Source3:        gnome-splash.png
Source4:	gnome-wm.desktop
# (fc) 2.4.2-3mdk use our own splash
Patch6:		gnome-session-2.17.90-splash.patch
# (blino) 2.16.1-2mdv allow to pass sm client id to compositing wm
Patch9:		gnome-session-2.23.6-compositing-wm.patch
# (fc) 2.23.91-2mdv set gnome-wm as default window manager
Patch10:	gnome-session-2.23.92-gnome-wm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-root
URL:            http://www.gnome.org/softwaremap/projects/gnome-session/
Requires:	GConf2 >= 1.2.1
Requires:	GConf2-sanity-check
Requires:	desktop-common-data
Requires:	usermode >= 1.63
Requires:	gnome-user-docs
Requires:	gnome-settings-daemon
BuildRequires:  x11-xtrans-devel
BuildRequires:  libxtst-devel
BuildRequires:	gnome-keyring-devel >= 2.21.92
BuildRequires:	usermode-consoleonly
BuildRequires:  tcp_wrappers-devel
BuildRequires:	libGConf2-devel >= 1.2.1
BuildRequires:  libgnomeui2-devel >= %{req_libgnomeui_version}
BuildRequires:  libglade2.0-devel
BuildRequires:  startup-notification-devel
BuildRequires:  gnome-settings-daemon-devel
BuildRequires:  policykit-gnome-devel
BuildRequires:  avahi-glib-devel avahi-client-devel
BuildRequires:  libgcrypt-devel
BuildRequires: intltool >= 0.40.0
BuildRequires: desktop-file-utils
BuildRequires: automake1.9

%description
GNOME (GNU Network Object Model Environment) is a user-friendly
set of applications and desktop tools to be used in conjunction with a
window manager for the X Window System.

The GNOME Session Manager restores a set session (group of applications)
when you log into GNOME.

%prep
%setup -q
%patch6 -p1 -b .splash
%patch9 -p1 -b .compositing-wm
%patch10 -p1 -b .gnome-wm

%build

%configure2_5x
%make


%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

cp %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/pixmaps/splash/mdv-gnome-splash.png

# wmsession session file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/wmsession.d
cat << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/X11/wmsession.d/02GNOME
NAME=GNOME
ICON=gnome-logo-icon-transparent.png
DESC=GNOME Environment
EXEC=%{_bindir}/startgnome
SCRIPT:
exec %{_bindir}/startgnome
EOF

desktop-file-install --vendor="" \
  --add-category="X-MandrivaLinux-System-Configuration-GNOME-Advanced" \
  --add-category="GTK" \
  --add-category="GNOME" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/startgnome

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gnome
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/gnome/gnomerc
# gw these produce rpmlint errors:
rm -rf %buildroot%_datadir/locale/{be@latin}
%find_lang %{name}-2.0


# restore gnome-wm.desktop file
install -m644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/applications/gnome-wm.desktop

# remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_datadir}/xsessions


%define schemas gnome-session

%post
if [ "$1" = "2" -a -r /etc/sysconfig/desktop ]; then
  sed -i -e "s|^DESKTOP=Gnome$|DESKTOP=GNOME|g" /etc/sysconfig/desktop
fi
%if %mdkversion < 200900
%post_install_gconf_schemas %{schemas}
%endif
%{make_session}
%if %mdkversion < 200900
%{update_menus}
%update_icon_cache hicolor
%endif

%preun
%preun_uninstall_gconf_schemas %{schemas}

%postun
%{make_session}
%if %mdkversion < 200900
%{clean_menus}
%clean_icon_cache hicolor
%endif

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT


%files -f %{name}-2.0.lang
%defattr (-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/*
%{_sysconfdir}/gnome/gnomerc
%{_sysconfdir}/gconf/schemas/*
%{_sysconfdir}/xdg/autostart/at-spi-registryd-wrapper.desktop
%{_sysconfdir}/xdg/autostart/gnome-settings-daemon-helper.desktop
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/gnome/autostart/gnome-session-splash.desktop
%{_datadir}/%name
%_datadir/icons/hicolor/*/apps/*
%{_mandir}/*/*
%dir %_libdir/gnome-session
%dir %_libdir/gnome-session/helpers
%_libdir/gnome-session/helpers/*

