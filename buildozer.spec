[app]

# (str) Title of your application
title = Sadece Kafa

# (str) Package name
package.name = sadekafa

# (str) Package domain (needed for android packaging)
package.domain = org.mutluteknik

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# USTA NOTU: Buraya 'openssl' ve 'sqlite3' gibi kritik parçaları ekledim ki az önceki hata tekrarlamasın.
requirements = python3,kivy,openssl,requests,urllib3

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
# USTA NOTU: 33 en stabil olanıdır.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
# USTA NOTU: Az önce takıldığımız yer burasıydı, 25b sürümüne sabitledim.
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded)
android.ndk_path = 

# (str) Android SDK directory (if empty, it will be automatically downloaded)
android.sdk_path = 

# (list) Android architectures to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# USTA NOTU: Modern telefonlar için en iyisi budur.
android.archs = arm64-v8a

# (bool) enables Android auto backup feature. Default to False
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk or aar).
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
