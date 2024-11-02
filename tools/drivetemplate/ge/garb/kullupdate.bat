adb shell
pm list packages | grep soagent
pm list packages | grep wssyncmldm
pm disable-user --user 0 com.sec.android.soagent
pm disable-user --user 0 com.wssyncmldm
appops set com.motorola.ccc.ota RUN_IN_BACKGROUND deny
pm disable-user com.motorola.ccc.devicemanagement
pm disable-user com.motorola.ccc.mainplm
pm disable-user com.motorola.ccc.notification
pm disable-user com.motorola.motocare
pm clear com.motorola.ccc.devicemanagement
pm clear com.motorola.ccc.mainplm
pm clear com.motorola.ccc.notification
pm clear com.motorola.motocare
adb shell pm disable-user --user 0 com.motorola.ccc.ota
appops set com.motorola.ccc.ota BOOT_COMPLETED deny
cmd appops set com.motorola.ccc.ota RUN_IN_BACKGROUND ignore
pm uninstall --user 0 com.motorola.ccc.ota
pm uninstall -k --user 0 com.motorola.ccc.ota
pm hide com.motorola.ccc.ota
cmd appops set com.motorola.ccc.ota RUN_IN_BACKGROUND deny
cmd appops set com.motorola.ccc.ota RUN_ANY_IN_BACKGROUND deny
cmd appops set com.motorola.android.fota RUN_IN_BACKGROUND deny
cmd appops set com.motorola.android.fota RUN_ANY_IN_BACKGROUND deny
