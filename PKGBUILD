# Maintainer: Ruben Harutyunyan <vagr9k@gmail.com>

pkgname=amdgpu-zerodb
pkgver=0.3
pkgrel=1
pkgdesc="A 0dB service for AMDGPU based GPUs."
arch=('i686' 'x86_64')
url="https://github.com/vagr9k/amdgpu-zerodb"
license=('GPL3')
depends=('python3')
provides=('amdgpu-zerodb')
source=("${pkgname}-${pkgver}.tar.gz::https://github.com/vagr9k/amdgpu-zerodb/archive/v${pkgver}.tar.gz")
md5sums=('7cca22d940cde0199018379225433bd3')

package() {
  cd "$srcdir/${pkgname}-${pkgver}"
  mkdir -p "$pkgdir/usr/bin/"
  cp amdgpu-zerodb.py "$pkgdir/usr/bin/amdgpu-zerodb"
  mkdir "$pkgdir/etc/"
  cp amdgpu-zerodb.conf "$pkgdir/etc/amdgpu-zerodb.conf"
  mkdir -p "$pkgdir/usr/lib/systemd/system/"
  cp amdgpu-zerodb.service "$pkgdir/usr/lib/systemd/system/amdgpu-zerodb.service"
}
