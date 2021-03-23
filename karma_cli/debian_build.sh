#!/bin/bash
VERSION=1.1.0
REVISION=1

BUILD_DIR=$(mktemp -d)
PACKAGE_DIR=karma-cli_$VERSION-$REVISION
CURRENT_DIR=$(pwd)
cd $BUILD_DIR
git clone https://github.com/bit-bots/karma
mkdir -p $PACKAGE_DIR/usr/bin
cp karma/karma_cli/src/karma_cli.py $PACKAGE_DIR/usr/bin/karma
mkdir $PACKAGE_DIR/DEBIAN
cat > $PACKAGE_DIR/DEBIAN/control << EOF
Package: karma-cli
Version: $VERSION-$REVISION
Section: misc
Priority: optional
Architecture: all
Depends: python3, python3-yaml, python3-requests, python3-numexpr
Maintainer: Timon Engelke <debian@timonengelke.de>
Homepage: https://karma.bit-bots.de
Vcs-Browser: https://github.com/bit-bots/karma
Vcs-Git: https://github.com/bit-bots/karma.git
Description: The command line interface for Bit-Bots karma
EOF
dpkg-deb --build $PACKAGE_DIR
mv $PACKAGE_DIR.deb $CURRENT_DIR
