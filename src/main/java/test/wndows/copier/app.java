package test.wndows.copier;

import java.util.ArrayList;
import test.wndows.copier.sb.util.SBmain;
import test.wndows.copier.sb.util.web.fileutil;

public class app {

  public static String tempdir = "C:/Games/";
  public static String temp = " " + tempdir + "f.txt";
  public static String storedir = "E:/ge/garb/smalll5345/crawls/";
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
    String crawp = storedir + craw1 + "/";
    fileutil.makedir(crawp);
    String direr = "sdcard/Documents/";
    direr(craw1, crawp, direr);
    direr = "sdcard/Downloads/";
    direr(craw1, crawp, direr);
    direr = "sdcard/DCIM/";
    direr(craw1, crawp, direr);
  }

  public static void direr(String craw1, String crawp, String direr) throws Exception {
    System.gc();
    String temper = tempdir + craw1 + ".txt";
    SBmain.doer("adb shell ls " + direr + " >" + temper);
    String res = fileutil.read(temper);
    System.out.println("res is " + res);
    for (String ss : res.split("\n")) {
      if (checkiflib(ss)) {
        dolib(ss, direr, tempdir, craw1, crawp);
      }
      dofile(direr, ss, crawp, craw1);
    }
    fileutil.delete(temper);
  }

  public static void dofile(String direr, String ss, String crawp, String craw1) throws Exception {
    SBmain.doer("cd " + crawp + " && adb pull " + direr + ss + " && adb shell rm -r " + direr + ss);
  }

  public static void dolib(String ss, String direr, String tempdir, String craw1, String crawp)
      throws Exception {
    String outfile = tempdir + craw1 + ".tx1";
    SBmain.doer("adb shell ls " + direr + "/" + ss + "/" + " >" + outfile);
    String r = fileutil.read(outfile);
    fileutil.delete(outfile);
    String[] ff = r.split("\n");
    if (ff.length > 999) {
      dofile(direr, ss, crawp, craw1);
    }
  }

  public static boolean checkiflib(String ss) {
    ss = ss.split(".")[0];
    if (ss.length() > 7)
      return false;
    if (ss.length() < 6)
      return false;
    for (char s : ss.toCharArray()) {
      if (Character.isDigit(s))
        continue;
      return false;
    }
    return true;
  }

}
