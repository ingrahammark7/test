package test.wndows.copier;

import java.util.ArrayList;
import test.wndows.copier.sb.util.SBmain;
import test.wndows.copier.sb.util.web.fileutil;

public class app {

  public static String tempdir = "C:\\Users\\a\\Documents\\GitHub\\test\\tools\\";
  public static String temp = " " + tempdir + "f.txt";
  public static String newcr = String.valueOf(System.currentTimeMillis());
  public static String tempfile = " >" + temp;
  public static ArrayList<String> devices = new ArrayList<String>();
  public static String foffer = tempdir + "foof.bat";
  public static String lsoffer = tempdir + "lso.bat";
  public static String pulff = tempdir + "pullf.bat";
  public static String savedrive = "E:";
  public static String storedir = savedrive + ":/ge/garb/smalll5345/crawls/";

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
    String device = s;
    String crawp = storedir + craw1 + "/";
    fileutil.makedir(crawp);
    String direr = "sdcard/Documents/";
    direr(craw1, crawp, direr, device);
    direr = "sdcard/Downloads/";
    direr(craw1, crawp, direr, device);
    direr = "sdcard/DCIM/";
    direr(craw1, crawp, direr, device);
  }

  public static void direr(String craw1, String crawp, String direr, String device)
      throws Exception {
    System.gc();
    String temper = tempdir + craw1 + ".txt";
    SBmain.doer("start " + foffer + " " + device + " " + direr + " " + temper + " " + tempdir);
    String res = fileutil.read(temper);
    fileutil.delete(temper);
    SBmain.doer("start " + lsoffer + " " + device + " " + direr + " " + temper + " " + tempdir);
    String r1 = fileutil.read(temper);
    fileutil.delete(temper);
    String[] files = res.split("\n");
    files = removelsof(files, r1);
    String savedir = storedir + direr + device + System.currentTimeMillis();
    fileutil.makedir(savedir);
    for (String ss : files) {
      if (checkiflib(ss)) {
        dolib(ss, direr, tempdir, craw1, crawp, device, savedir);
      }
      dofile(direr, ss, crawp, craw1, device, savedir, savedrive);
    }
    fileutil.delete(temper);
  }

  public static String[] removelsof(String[] files, String r1) {
    ArrayList<String> ff = new ArrayList<String>();
    for (String s : files) {
      if (r1.contains(s))
        continue;
      ff.add(s);
    }
    return fileutil.list2array(ff);
  }

  public static void dofile(String direr, String ss, String crawp, String craw1, String device,
      String savedir, String savedrive) throws Exception {
    String com = "start " + pulff + " " + device + " " + direr + " " + "foo" + " " + tempdir + " "
        + storedir + savedrive;
    SBmain.doer(com);
  }

  public static void dolib(String ss, String direr, String tempdir, String craw1, String crawp,
      String device, String savedir) throws Exception {
    String outfile = tempdir + craw1 + ".tx1";
    SBmain.doer("adb shell ls " + direr + "/" + ss + "/" + " >" + outfile);
    String r = fileutil.read(outfile);
    fileutil.delete(outfile);
    String[] ff = r.split("\n");
    if (ff.length > 999) {
      dofile(direr, ss, crawp, craw1, device, savedir, savedrive);
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
