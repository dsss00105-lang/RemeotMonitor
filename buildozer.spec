[app]
title = RemoteMonitor
version = 0.1
package.name = remotemonitor
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
requirements = python3,kivy==2.3.0,requests==2.31.0,android,cython==0.29.37
android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE,ACCESS_WIFI_STATE,ACCESS_NETWORK_STATE
android.sdk = 24
android.ndk = 21
android.api = 24
android.skip_update = True
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1