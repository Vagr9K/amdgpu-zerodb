# Maintainer: Ruben Harutyunyan <vagr9k@gmail.com>
# Maintainer: Ruben Harutyunyan <vagr9k@gmail.com>

pkgname=amdgpu-zerodb
pkgver=0.1
pkgrel=1
pkgdesc="0dB service for AMDGPU based GPUs."
arch=('i686' 'x86_64')
url="https://github.com/vagr9k/amdgpu-zerodb"
license=('GPL3')
depends=('python3')
provides=('amdgpu-zerodb')
source=('${pgname}-${pkgver}.tar.gz::https://github.com/vagr9k/amdgpu-zerodb/archive/v${pkgver}.tar.gz')

package() {
  cd "$srcdir/${pkgname}-${pkgver}"
  cp amdgpu-zerodb.py "$pkgdir/usr/bin/amdgpu-zerodb"
  cp amdgpu-zerodb.conf "$pkgdir/etc/amdgpu-zerodb.conf"
  cp amdgpu-zerodb.service "$pkgdir/usr/lib/systemd/system/amdgpu-zerodb.service"
}
