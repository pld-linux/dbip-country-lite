%define		edition	country
%define		geoname	Country
%define		mver	2026-08
Summary:	DB-IP IP to Country Lite - free IP geolocation database
Summary(pl.UTF-8):	DB-IP IP to Country Lite - darmowa baza danych krajów dla geolokalizacji IP
Name:		dbip-%{edition}-lite
Version:	20260801
Release:	1
License:	CC-BY-4.0
Group:		Applications/Databases
Source0:	https://download.db-ip.com/free/%{name}-%{mver}.mmdb.gz
# Source0-md5:	69f41a8cb14015a78da74031bb38f5a4
URL:		https://db-ip.com/db/lite.php
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DB-IP Lite databases are free IP geolocation databases from DB-IP.com,
a freely redistributable alternative to MaxMind GeoLite2 in the same
MMDB format.

This package provides the IP to Country Lite database, which maps IP
addresses to a country.

This product includes IP geolocation data created by DB-IP.com,
available under a Creative Commons Attribution 4.0 International
License.

%description -l pl.UTF-8
Bazy danych DB-IP Lite to darmowe bazy geolokalizacji adresów IP od
DB-IP.com, swobodnie redystrybuowalna alternatywa dla MaxMind GeoLite2
w tym samym formacie MMDB.

Ten pakiet dostarcza bazę IP to Country Lite, przypisującą adresom IP
kraj.

Produkt zawiera dane geolokalizacyjne stworzone przez DB-IP.com,
dostępne na licencji Creative Commons Attribution 4.0 International.

%package -n dbip-%{edition}-lite-GeoLite2-compat
Summary:	GeoLite2-named symlink for the DB-IP Country Lite database
Summary(pl.UTF-8):	Dowiązanie o nazwie GeoLite2 do bazy DB-IP Country Lite
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}
Provides:	GeoLite2-db-%{geoname} = %{version}-%{release}
Conflicts:	GeoLite2-db-%{geoname}

%description -n dbip-%{edition}-lite-GeoLite2-compat
This compatibility package installs the DB-IP Country Lite database
under the MaxMind file name %{_datadir}/GeoIP/GeoLite2-%{geoname}.mmdb
(a symlink), for software that expects the GeoLite2 file name.

%description -n dbip-%{edition}-lite-GeoLite2-compat -l pl.UTF-8
Pakiet zgodności udostępniający bazę DB-IP Country Lite pod nazwą
pliku MaxMind %{_datadir}/GeoIP/GeoLite2-%{geoname}.mmdb (dowiązanie
symboliczne), dla oprogramowania oczekującego nazwy zgodnej z
GeoLite2.

%prep
%setup -qcT
cp -p %{SOURCE0} dbip-%{edition}-lite.mmdb.gz

# -N: take the build date from the gzip header, not the download mtime
gunzip -N dbip-%{edition}-lite.mmdb.gz

# the database build month must match %{mver}
ver=$(TZ=GMT stat -c '%y' dbip-%{edition}-lite.mmdb | cut -c1-7)
if [ "$ver" != "%{mver}" ]; then
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/GeoIP
cp -p dbip-%{edition}-lite.mmdb $RPM_BUILD_ROOT%{_datadir}/GeoIP
ln -s dbip-%{edition}-lite.mmdb $RPM_BUILD_ROOT%{_datadir}/GeoIP/GeoLite2-%{geoname}.mmdb

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_datadir}/GeoIP/dbip-%{edition}-lite.mmdb

%files -n dbip-%{edition}-lite-GeoLite2-compat
%defattr(644,root,root,755)
%{_datadir}/GeoIP/GeoLite2-%{geoname}.mmdb
