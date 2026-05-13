[app]
title = Sade Kafa
package.name = sadekafa
package.domain = org.yucemurat
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.accept_sdk_license = True
android.api = 33
android.minapi = 21
android.ndk = 25b
android.gradle_dependencies = sqlite3
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
