[app]
title = City Drive Mobile
package.name = citydrive
package.domain = org.citydrive
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1.0
requirements = python3,kivy
orientation = landscape
fullscreen = 1
android.api = 35
android.minapi = 23
android.archs = arm64-v8a,armeabi-v7a
android.allow_backup = False
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
