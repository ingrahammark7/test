adb shell
pm list packages | grep soagent
pm list packages | grep wssyncmldm
pm disable-user --user 0 com.sec.android.soagent
pm disable-user --user 0 com.wssyncmldm