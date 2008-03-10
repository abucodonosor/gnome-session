%define  req_libgnomeui_version	2.1.0

Summary:        The gnome desktop programs for the GNOME GUI desktop environment
Name:           gnome-session
Version: 2.22.0
Release:        %mkrel 1
License:        GPL/LGPL
Group:          Graphical desktop/GNOME
Source0:        ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Source1:        gnome-session-startgnome
Source2:	gnome-session-gnomerc
Source3:        gnome-splash.png
# (fc) 2.0.7-2mdk add pam-panel-icon and eggcups to default session
Patch3:		gnome-session-2.17.90-defaultsession.patch
# (fc) 2.2.0.2-2mdk add some icons to splashscreen
Patch4:		gnome-session-2.18.0-splashicons.patch
# (fc) 2.4.2-3mdk use our own splash
Patch6:		gnome-session-2.17.90-splash.patch
# (fc) 2.15.1-1mdv disable crash on warning
Patch8:		gnome-session-2.13.4-no-crashes.patch
# (blino) 2.16.1-2mdv allow to pass sm client id to compositing wm
Patch9:		gnome-session-2.16.1-compositing-wm.patch
# (fc) 2.17.92-2mdv increase timeout for at-spi launch
Patch11:	gnome-session-2.19.4-popup.patch
# (fc) 2.20.0-1mdv don't fade logout on LTSP client (Ubuntu)
Patch13:	gnome-session-2.20-dont-fade-ltsp.patch
# (fc) 2.20.0-1mdv prevent splash from staying too long on screen (Ubuntu)
Patch14:	gnome-session-2.20-splash-hide.patch
# (fc) 2.20.2-2mdv always enable sound server (since we use PulseAudio)
Patch16:	gnome-session-enable-sound-by-default.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-root
URL:            http://www.gnome.org/softwaremap/projects/gnome-session/
Requires:	GConf2 >= 1.2.1
Requires:	GConf2-sanity-check
Requires:	desktop-common-data
Requires:	usermode >= 1.63
Requires:	gnome-user-docs
Requires:	gnome-settings-daemon
BuildRequires:	gnome-keyring-devel >= 2.21.92
BuildRequires:	usermode-consoleonly
BuildRequires:  tcp_wrappers-devel
BuildRequires:	libGConf2-devel >= 1.2.1
BuildRequires:  libgnomeui2-devel >= %{req_libgnomeui_version}
BuildRequires:  gnome-settings-daemon-devel
BuildRequires:  avahi-glib-devel avahi-client-devel
BuildRequires:  libgcrypt-devel
BuildRequires: perl-XML-Parser
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
%patch3 -p1 -b .defaultsession
%patch4 -p1 -b .splashicons
%patch6 -p1 -b .splash
%patch8 -p1 -b .disablewarningcrash
%patch9 -p1 -b .compositing-wm
%patch11 -p1 -b .popup
%patch13 -p1 -b .prevent-fade-ltsp
%patch14 -p1 -b .splash-hide
%patch16 -p1 -b .enable-sound

%build

%configure2_5x --with-reboot-command=%{_bindir}/reboot --with-halt-command=%{_bindir}/poweroff
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

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_bindir}/gnome-smproxy


%define schemas gnome-session

%post
if [ "$1" = "2" -a -r /etc/sysconfig/desktop ]; then
  sed -i -e "s|^DESKTOP=Gnome$|DESKTOP=GNOME|g" /etc/sysconfig/desktop
fi
%post_install_gconf_schemas %{schemas}
%{make_session}
%{update_menus}
%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas %{schemas}

%postun
%{make_session}
%{clean_menus}
%clean_icon_cache hicolor

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT


%files -f %{name}-2.0.lang
%defattr (-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/*
%{_sysconfdir}/gnome/gnomerc
%{_sysconfdir}/gconf/schemas/*
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/gnome/*
%{_datadir}/pixmaps/*
%_datadir/icons/hicolor/*/apps/*
%{_datadir}/xsessions/gnome.desktop
%{_mandir}/*/*


