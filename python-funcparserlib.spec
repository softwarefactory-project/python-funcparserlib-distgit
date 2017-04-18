%global srcname funcparserlib

%if 0%{?fedora} > 0
%global has_py3	1
%else
%global has_py3	0
%endif

Name:           python-%{srcname}
Version:        0.3.6
Release:        11%{?dist}
Summary:        Recursive descent parsing library based on functional combinators

License:        MIT
URL:            https://github.com/vlasovskikh/funcparserlib
Source0:        https://pypi.python.org/packages/source/f/%{srcname}/%{srcname}-%{version}.tar.gz
Source1:        description-%{srcname}.txt


BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools  python-nose

%if %{has_py3}
BuildRequires:  python3-devel python3-setuptools python3-nose
%endif

%description
%(cat %{SOURCE1})


%if %{has_py3}
%package -n python3-%{srcname}
Summary:        %{summary}


%description -n python3-%{srcname}
%(cat %{SOURCE1})

This package installs the %{srcname} module for Python 3.
%endif


%prep
%setup -q -n %{srcname}-%{version}

%if %{has_py3}
rm -rf %{py3dir}
cp -a . %{py3dir}

find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'
%endif


%build
%{__python2} setup.py build

%if %{has_py3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%if %{has_py3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif


%check
nosetests build/

%if %{has_py3}
pushd %{py3dir}
nosetests-%{python3_version} build/
popd
%endif


%files
%doc PKG-INFO LICENSE README CHANGES
%{python2_sitelib}/%{srcname}*
%exclude %{python2_sitelib}/%{srcname}/tests


%if %{has_py3}
%files -n python3-%{srcname}
%{_pkgdocdir}
%{python3_sitelib}/%{srcname}*
%exclude %{python3_sitelib}/%{srcname}/tests
%endif


%changelog
* Sat Feb 11 2017 Dridi Boukelmoune <dridi.boukelmoune@gmail.com> - 0.3.6-11
- Python 3 detection for epel7

* Fri Feb 10 2017 Dridi Boukelmoune <dridi.boukelmoune@gmail.com> - 0.3.6-10
- Update URL

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.3.6-9
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sat Dec 21 2013 Dridi Boukelmoune <dridi.boukelmoune@gmail.com> - 0.3.6-2
- Using %%{python3_version} instead of hardcoded 3.3

* Mon Dec 09 2013 Dridi Boukelmoune <dridi.boukelmoune@gmail.com> - 0.3.6-1
- Initial spec
