Summary:        The gnome desktop programs for the GNOME GUI desktop environment
Name:           gnome-session
Version: 2.32.1
Release:        %mkrel 2
License:        GPLv2+
Group:          Graphical desktop/GNOME
Source0:        ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Source1:        gnome-session-startgnome
Source2:	gnome-session-gnomerc
Source4:	gnome-wm.desktop
# (blino) 2.16.1-2mdv allow to pass sm client id to compositing wm
Patch9:		gnome-session-2.26.2-compositing-wm.patch
# (fc) 2.28.0-2mdv fix crash at logout (GNOME bug #590828)
Patch10:	gnome-session-2.28.0-fixcrash.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-root
URL:            http://www.gnome.org/softwaremap/projects/gnome-session/
Requires:	GConf2 >= 1.2.1
Requires:	desktop-common-data
Requires:	gnome-user-docs
Requires:	gnome-settings-daemon
Requires:	%{name}-bin >= %{version}-%{release}
BuildRequires:  x11-xtrans-devel
BuildRequires:	libsm-devel
BuildRequires:  libxtst-devel
BuildRequires:	usermode-consoleonly
BuildRequires:  tcp_wrappers-devel
BuildRequires:	libGConf2-devel >= 1.2.1
BuildRequires:	GConf2
BuildRequires:  gtk+2-devel
BuildRequires:  startup-notification-devel
BuildRequires:  gnome-settings-daemon-devel
BuildRequires:	UPower-devel
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

%package bin
Group:          %{group}
Summary:        %{summary}
Conflicts: gnome-session < 2.30.2-2mdv
Requires:	GConf2-sanity-check

%description bin
This package contains the binaries for the GNOME Session Manager, but 
no startup scripts. It is meant for applications such as GDM that use 
gnome-session internally.

%prep
%setup -q
%apply_patches

%build

%configure2_5x --with-default-wm=gnome-wm --enable-splash
%make


%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

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

%if %mdkversion < 200900
%post bin
%post_install_gconf_schemas %{schemas}
%endif

%post
if [ "$1" = "2" -a -r /etc/sysconfig/desktop ]; then
  sed -i -e "s|^DESKTOP=Gnome$|DESKTOP=GNOME|g" /etc/sysconfig/desktop
fi
%{make_session}
%if %mdkversion < 200900
%{update_menus}
%endif

%if %mdkversion < 200900
%post bin
%update_icon_cache hicolor
%endif

%preun bin
%preun_uninstall_gconf_schemas %{schemas}

%postun
%{make_session}
%if %mdkversion < 200900
%{clean_menus}
%endif

%if %mdkversion < 200900
%postun bin
%clean_icon_cache hicolor
%endif

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files bin
%defattr (-, root, root)
%{_sysconfdir}/gconf/schemas/*
%{_bindir}/gnome-session
%{_mandir}/*/gnome-session.*
%{_datadir}/%name
%_datadir/icons/hicolor/*/apps/*

%files -f %{name}-2.0.lang
%defattr (-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/*
%{_sysconfdir}/gnome/gnomerc
%{_bindir}/startgnome
%{_bindir}/gnome-session-properties
%{_bindir}/gnome-wm
%{_bindir}/gnome-session-save
%{_datadir}/applications/*
%{_mandir}/*/gnome-wm.*
%{_mandir}/*/gnome-session-properties.*
%{_mandir}/*/gnome-session-save.*

