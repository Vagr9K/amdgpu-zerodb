# Maintainer: Ruben Harutyunyan <vagr9k@gmail.com>

pkgname=amdgpu-zerodb
pkgver=0.4
pkgrel=1
pkgdesc="A 0dB service for AMDGPU based GPUs."
arch=('i686' 'x86_64')
url="https://github.com/vagr9k/amdgpu-zerodb"
license=('GPL3')
depends=('python3')
provides=('amdgpu-zerodb')
source=("${pkgname}-${pkgver}.tar.gz::https://github.com/vagr9k/amdgpu-zerodb/archive/v${pkgver}.tar.gz")
md5sums=('fd1a6370465c73184ad78f062cd7fbaf')

package() {
  cd "$srcdir/${pkgname}-${pkgver}"
  mkdir -p "$pkgdir/usr/bin/"
  cp amdgpu-zerodb.py "$pkgdir/usr/bin/amdgpu-zerodb"
  mkdir "$pkgdir/etc/"
  cp amdgpu-zerodb.conf "$pkgdir/etc/amdgpu-zerodb.conf"
  mkdir -p "$pkgdir/usr/lib/systemd/system/"
  cp amdgpu-zerodb.service "$pkgdir/usr/lib/systemd/system/amdgpu-zerodb.service"
}
