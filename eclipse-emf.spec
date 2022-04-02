%global _eclipsedir %{_prefix}/lib/eclipse
%global emf_tag 666f438f84c97358ce33fd4c1f615212cdd419f9
%global xsd_tag a5f53126aa28435e3f44bde6700372c8559127de
%bcond_without bootstrap
Name:                eclipse-emf
Version:             2.16.0
Release:             2
Summary:             EMF and XSD Eclipse plug-ins
License:             EPL-2.0
URL:                 http://www.eclipse.org/modeling/emf/
Source0:             http://git.eclipse.org/c/emf/org.eclipse.emf.git/snapshot/org.eclipse.emf-%{emf_tag}.tar.gz
Source1:             http://git.eclipse.org/c/xsd/org.eclipse.xsd.git/snapshot/org.eclipse.xsd-%{xsd_tag}.tar.gz
Patch0:              remove-nebula-dep.patch
Patch1:              remove-network-tests.patch
Patch2:              remove-timezone-test.patch
Patch3:              remove-unnecessary-imports.patch
BuildRequires:       tycho tycho-extras
%if %{without bootstrap}
BuildRequires:       eclipse-pde
%endif
BuildArch:           noarch
%description
The Eclipse Modeling Framework (EMF) and XML Schema Definition (XSD) plug-ins.

%package   core
Epoch:               1
Summary:             Eclipse EMF Core Bundles
%description core
Core EMF bundles required by the Eclipse platform.
%if %{without bootstrap}

%package   runtime
Summary:             Eclipse Modeling Framework (EMF) Eclipse plug-in
%description runtime
The Eclipse Modeling Framework (EMF) allows developers to build tools and
other applications based on a structured data model. From a model
specification described in XMI, EMF provides tools and run-time support to
produce a set of Java classes for the model, along with a set of adapter
classes that enable viewing and command-based editing of the model, and a
basic editor.

%package   xsd
Summary:             XML Schema Definition (XSD) Eclipse plug-in
Obsoletes:           eclipse-xsd < %{version}-%{release}
Provides:            eclipse-xsd = %{version}-%{release}
%description xsd
The XML Schema Definition (XSD) plug-in is a library that provides an API for
manipulating the components of an XML Schema as described by the W3C XML
Schema specifications, as well as an API for manipulating the DOM-accessible
representation of XML Schema as a series of XML documents.

%package   sdk
Summary:             Eclipse EMF and XSD SDK
Obsoletes:           %{name}-tests < %{version}-%{release}
Obsoletes:           %{name}-examples < %{version}-%{release}
Obsoletes:           eclipse-xsd-examples < %{version}-%{release}
Obsoletes:           eclipse-xsd-sdk < %{version}-%{release}
Provides:            eclipse-xsd-sdk = %{version}-%{release}
%description sdk
Documentation and developer resources for the Eclipse Modeling Framework
(EMF) plug-in and XML Schema Definition (XSD) plug-in.
%endif

%prep
%setup -c -T -q -a 0 -a 1
mv org.eclipse.emf-%{emf_tag}/ org.eclipse.emf/
mv org.eclipse.xsd-%{xsd_tag}/ org.eclipse.xsd/
%patch0
%patch1
%patch2
%patch3
pushd org.eclipse.emf
sed -i -e '/org.eclipse.emf.gwt/d' releng/org.eclipse.emf.parent/{plugins,features}/pom.xml
sed -i -e '/org.eclipse.emf.oda/d' releng/org.eclipse.emf.parent/{plugins,features}/pom.xml
sed -i -e '/org.eclipse.emf.rap/d' releng/org.eclipse.emf.parent/{plugins,features}/pom.xml
sed -i -e '/codegen.ecore.xtext/d' releng/org.eclipse.emf.parent/{plugins,features}/pom.xml
sed -i -e '/ecore.xcore/d' releng/org.eclipse.emf.parent/{plugins,features}/pom.xml
sed -i -e '/test.edit.ui.rap/d' releng/org.eclipse.emf.parent/{plugins,features}/pom.xml
%pom_xpath_remove "plugin[@id='org.eclipse.emf.test.edit.ui.rap']" tests/org.eclipse.emf.tests-feature/feature.xml
%pom_disable_module "../../../examples/org.eclipse.emf.examples-feature" releng/org.eclipse.emf.parent/features
%pom_disable_module "../../../../org.eclipse.xsd/features/org.eclipse.xsd.example-feature" releng/org.eclipse.emf.parent/features
sed -i -e '/<module>.*examples/d' releng/org.eclipse.emf.parent/plugins/pom.xml
%pom_xpath_remove "plugin[@id='org.eclipse.emf.test.examples']" tests/org.eclipse.emf.tests-feature/feature.xml
%pom_disable_module "tp" releng/org.eclipse.emf.parent
%pom_disable_module "../org.eclipse.emf.site" releng/org.eclipse.emf.parent
%pom_disable_module '../../../features/org.eclipse.emf.all-feature' releng/org.eclipse.emf.parent/features
%pom_remove_plugin :target-platform-configuration releng/org.eclipse.emf.parent
%pom_remove_dep :tycho-sourceref-jgit releng/org.eclipse.emf.parent
%pom_remove_dep :tycho-buildtimestamp-jgit releng/org.eclipse.emf.parent
%pom_xpath_remove 'pom:configuration/pom:timestampProvider' releng/org.eclipse.emf.parent
%pom_xpath_remove 'pom:configuration/pom:jgit.ignore' releng/org.eclipse.emf.parent
%pom_xpath_remove 'pom:configuration/pom:jgit.dirtyWorkingTree' releng/org.eclipse.emf.parent
%pom_xpath_remove 'pom:configuration/pom:sourceReferences' releng/org.eclipse.emf.parent
%if %{with bootstrap}
%pom_xpath_replace "pom:modules" "<modules>
<module>../../../features/org.eclipse.emf.base-feature</module>
<module>../../../features/org.eclipse.emf.license-feature</module>
<module>../../../features/org.eclipse.emf.common-feature</module>
<module>../../../features/org.eclipse.emf.ecore-feature</module>
</modules>" releng/org.eclipse.emf.parent/features
%pom_xpath_replace "pom:modules" "<modules>
<module>../../../plugins/org.eclipse.emf.common</module>
<module>../../../plugins/org.eclipse.emf.ecore.change</module>
<module>../../../plugins/org.eclipse.emf.ecore.xmi</module>
<module>../../../plugins/org.eclipse.emf.ecore</module>
</modules>" releng/org.eclipse.emf.parent/plugins
%endif
popd
%mvn_package "::pom::" __noinstall
%mvn_package ":org.eclipse.{emf,xsd}.license" __noinstall
%mvn_package ":org.eclipse.emf.tests" __noinstall
%mvn_package ":org.eclipse.emf.test.*" __noinstall
%if %{with bootstrap}
%mvn_package ":::{sources,sources-feature}:" __noinstall
%else
%mvn_package ":::{sources,sources-feature}:" sdk
%endif
%mvn_package ":org.eclipse.emf.{sdk,doc,cheatsheets,example.installer}" sdk
%mvn_package ":org.eclipse.xsd.{sdk,doc,cheatsheets,example.installer}" sdk
%mvn_package "org.eclipse.emf.features:org.eclipse.emf.{base,common,ecore}"
%mvn_package "org.eclipse.emf:org.eclipse.emf.{common,ecore,ecore.change,ecore.xmi}"
%mvn_package ":org.eclipse.xsd*" xsd
%mvn_package ":org.eclipse.emf.mapping.xsd**" xsd
%mvn_package ":" runtime

%build
QUALIFIER=$(date -u -d"$(stat --format=%y %{SOURCE0})" +v%Y%m%d-%H%M)
%mvn_build -j -- -f org.eclipse.emf/pom.xml -DforceContextQualifier=$QUALIFIER -Dmaven.test.failure.ignore=true

%install
%mvn_install
install -d -m 755 %{buildroot}%{_eclipsedir}
mv %{buildroot}%{_datadir}/eclipse/droplets/emf/{plugins,features} %{buildroot}%{_eclipsedir}
rm -r %{buildroot}%{_datadir}/eclipse/droplets/emf
sed -i -e 's|%{_datadir}/eclipse/droplets/emf|%{_eclipsedir}|' %{buildroot}%{_datadir}/maven-metadata/eclipse-emf.xml
sed -i -e 's|%{_datadir}/eclipse/droplets/emf/features/|%{_eclipsedir}/features/|' \
       -e 's|%{_datadir}/eclipse/droplets/emf/plugins/|%{_eclipsedir}/plugins/|' .mfiles
sed -i -e '/droplets/d' .mfiles
for del in $( (cd %{buildroot}%{_eclipsedir}/plugins && ls | grep -v -e '^org\.eclipse\.emf' ) ) ; do
rm %{buildroot}%{_eclipsedir}/plugins/$del
sed -i -e "/$del/d" .mfiles
done

%files core -f .mfiles
%license org.eclipse.emf/features/org.eclipse.emf.license-feature/*.html
%if %{without bootstrap}

%files runtime -f .mfiles-runtime

%files xsd -f .mfiles-xsd

%files sdk -f .mfiles-sdk
%endif

%changelog
* Thu Apr 7 2022 xiaoqian lv <xiaoqian@nj.iscas.ac.cn> - 2.16.0-2
- bootstrap build

* Thu Aug 27 2020 yanan li <liyanan032@huawei.com> - 2.16.0-1
- Package init
