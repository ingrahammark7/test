package test.wndows.copier;

import java.util.ArrayList;
import test.wndows.copier.sb.util.SBmain;
import test.wndows.copier.sb.util.web.fileutil;

public class app {

  public static String tempdir = "C:/Games/";
  public static String temp = " " + tempdir + "f.txt";
  public static String storedir = "E:\\ge\\garb\\smalll5345\\crawl";
  public static String newcr = String.valueOf(System.currentTimeMillis());
  public static String tempfile = " >" + temp;
  public static ArrayList<String> devices = new ArrayList<String>();

  public static void main(String[] args) throws Exception {
    fileutil.delete(temp);
    SBmain.doer("adb devices" + tempfile);
    String s = fileutil.read(temp);
    String[] foff = s.split("\n");
    for (int i = 0; i < foff.length; ++i) {
      String t = foff[i];
      if (t.contains("List"))
        continue;
      if (t.equals(""))
        continue;
      if (t.contains("device"))
        devices.add(t.split("\t")[0]);
    }
    for (String sf : devices) {
      pulldevice(sf);
    }
  }

  public static void pulldevice(String s) throws Exception {
    String craw1 = s + newcr;
    String crawp = craw1 + "/file.txt";
    fileutil.makedir(crawp);
    String temper = tempdir + craw1 + ".txt";
    SBmain.doer("adb shell ls sdcard/Documents/ >" + temper);
    String res = fileutil.read(temper);
    for (String ss : res.split("\n")) {
      SBmain.doer("adb pull sdcard/Documents/" + ss + " >" + crawp);
    }
  }

}
