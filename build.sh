#!/bin/bash

list_dependencies=(rpm-build rpmdevtools)

for i in ${list_dependencies[*]}
do
    if ! rpm -qa | grep -qw $i; then
        echo "__________Dont installed '$i'__________"
        #yum -y install $i
    fi
done

rm -rf ~/rpmbuild/
mkdir -p ~/rpmbuild/{RPMS,SRPMS,BUILD,SOURCES,SPECS}
cd SOURCES
cp jaeger-all-in-one.service ~/rpmbuild/SOURCES
cp jaeger-all-in-one.yaml ~/rpmbuild/SOURCES
cd ..
spectool -g -R jaeger-all-in-one-rpm.spec
rpmbuild -bb jaeger-all-in-one-rpm.spec
