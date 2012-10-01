Summary:	Libraries for digital cameras
Name:		libgphoto2
Version:	2.4.14
Release:	3
License:	LGPL
Group:		Applications
Source0:	http://downloads.sourceforge.net/gphoto/%{name}-%{version}.tar.gz
# Source0-md5:	492bec63dd610906c3a28030be77e650
Patch0:		%{name}-canonS90.patch
URL:		http://www.gphoto.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libexif-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	libusbx-devel
BuildRequires:	pkg-config
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libraries for digital cameras.

%package runtime
Summary:	Runtime part of libgphoto2 library
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description runtime
This is the runtime package containing camera drivers, ports
and utilities.

%description
Libraries for digital cameras.

%package devel
Summary:	Header files for libgphoto2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libgphoto2.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I auto-m4 -I m4m
%{__automake}
%{__autoconf}

cd libgphoto2_port
%{__libtoolize}
%{__aclocal} -I auto-m4 -I m4
%{__automake}
%{__autoconf}
cd ..

%configure \
	--disable-static	\
	--disable-baudboy	\
	--disable-resmgr	\
	--disable-ttylock	\
	--without-libusb
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/lib/udev/rules.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir} \
	udevscriptdir=%{_libdir}/libgphoto2

:> $RPM_BUILD_ROOT/usr/lib/udev/rules.d/40-libgphoto2.rules

%find_lang %{name} --all-name

# prepare docs
install -d docs
cp --parents \
	camlibs/adc65/{Changelog,README.*,TODO}		\
	camlibs/agfa-cl20/{RANDOM,README.*,STATUS}	\
	camlibs/aox/README.*				\
	camlibs/canon/README.*				\
	camlibs/casio/PROTOCOL.txt			\
	camlibs/digigr8/README.*			\
	camlibs/dimera/{CREDITS,Protocol.txt}		\
	camlibs/enigma13/{README.*,STATUS,protocol.txt} \
	camlibs/fuji/PROTOCOL				\
	camlibs/gsmart300/README.*			\
	camlibs/iclick/README.*				\
	camlibs/jamcam/README.*				\
	camlibs/jd11/jd11.html 				\
	camlibs/kodak/CAMERAS 				\
	camlibs/kodak/ez200/Protocol.txt 		\
	camlibs/konica/{EXPERTS,README.*} 		\
	camlibs/largan/lmini/README.* 			\
	camlibs/lg_gsm/README.* 			\
	camlibs/mars/{README.*,protocol.txt} 		\
	camlibs/minolta/NEWER_MINOLTAS 			\
	camlibs/minolta/dimagev/README.* 		\
	camlibs/mustek/{AUTHOR,README.*} 		\
	camlibs/panasonic/README.* 			\
	camlibs/panasonic/coolshot/README.* 		\
	camlibs/panasonic/l859/README.* 		\
	camlibs/pccam300/README.* 			\
	camlibs/pccam600/README.* 			\
	camlibs/polaroid/*.html 			\
	camlibs/ptp2/{README.*,TODO} 			\
	camlibs/ricoh/g3.txt 				\
	camlibs/sierra/PROTOCOL 			\
	camlibs/sipix/{*.txt,web2.html} 		\
	camlibs/smal/README.* 				\
	camlibs/sonix/README.* 				\
	camlibs/soundvision/README.* 			\
	camlibs/spca50x/README.* 			\
	camlibs/stv0674/{Changelog,Protocol} 		\
	camlibs/stv0680/{680_comm*,CREDITS,README.pdf}	\
	camlibs/toshiba/pdrm11/README.*			\
	libgphoto2_port/AUTHORS				\
	docs

rm -f $RPM_BUILD_ROOT%{_libdir}/libgphoto2/*/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libgphoto2_port/*/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libgphoto2_port/*/serial.*

# kill unpackaged files
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libgphoto{2,2_port}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%post runtime
umask 022
%{_libdir}/libgphoto2/print-camera-list udev-rules version 175 group usb mode 0660 > \
	$RPM_BUILD_ROOT/usr/lib/udev/rules.d/40-libgphoto2.rules

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TESTERS docs/*
%attr(755,root,root) %ghost %{_libdir}/libgphoto2.so.?
%attr(755,root,root) %ghost %{_libdir}/libgphoto2_port.so.?
%attr(755,root,root) %{_libdir}/libgphoto2.so.*.*.*
%attr(755,root,root) %{_libdir}/libgphoto2_port.so.*.*.*

%files runtime -f %{name}.lang
%defattr(644,root,root,755)
# camera plugins
%dir %{_libdir}/libgphoto2
%dir %{_libdir}/libgphoto2/%{version}
%attr(755,root,root) %{_libdir}/libgphoto2/%{version}/*.so
%{_libdir}/libgphoto2/%{version}/*.la

# port plugins
%dir %{_libdir}/libgphoto2_port
%dir %{_libdir}/libgphoto2_port/*
%attr(755,root,root) %{_libdir}/libgphoto2_port/*/disk.so
%attr(755,root,root) %{_libdir}/libgphoto2_port/*/ptpip.so
%attr(755,root,root) %{_libdir}/libgphoto2_port/*/usb1.so
%attr(755,root,root) %{_libdir}/libgphoto2_port/*/usbdiskdirect.so
%attr(755,root,root) %{_libdir}/libgphoto2_port/*/usbscsi.so
%{_libdir}/libgphoto2_port/*/disk.la
%{_libdir}/libgphoto2_port/*/ptpip.la
%{_libdir}/libgphoto2_port/*/usb1.la
%{_libdir}/libgphoto2_port/*/usbdiskdirect.la
%{_libdir}/libgphoto2_port/*/usbscsi.la

# utilities
%attr(755,root,root) %{_libdir}/libgphoto2/check-ptp-camera
%attr(755,root,root) %{_libdir}/libgphoto2/print-camera-list

# udev rules file for libgphoto2 devices
%ghost /usr/lib/udev/rules.d/40-libgphoto2.rules

%dir %{_datadir}/libgphoto2
%dir %{_datadir}/libgphoto2/%{version}
%dir %{_datadir}/libgphoto2/%{version}/konica
%{_datadir}/libgphoto2/%{version}/konica/english
%lang(fr) %{_datadir}/libgphoto2/%{version}/konica/french
%lang(de) %{_datadir}/libgphoto2/%{version}/konica/german
%lang(ja) %{_datadir}/libgphoto2/%{version}/konica/japanese
%lang(ko) %{_datadir}/libgphoto2/%{version}/konica/korean
%lang(es) %{_datadir}/libgphoto2/%{version}/konica/spanish

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gphoto2*-config
%attr(755,root,root) %{_libdir}/libgphoto2.so
%attr(755,root,root) %{_libdir}/libgphoto2_port.so
%{_libdir}/libgphoto2.la
%{_libdir}/libgphoto2_port.la
%{_includedir}/gphoto2
%{_pkgconfigdir}/*.pc
%{_mandir}/man3/*

