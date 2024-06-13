package test.wndows.copier.sb.util.code.z2app;

import java.awt.event.KeyEvent;
import java.util.ArrayList;
import test.wndows.copier.sb.util.util;
import test.wndows.copier.sb.util.web.fileutil;

// gallery-dl -i C:\Users\a\Documents\GitHub\test\foo.txt --http-timeout 1000

public class zogapp {

  public static int urlx = 1682;
  public static int urly = 394;
  public static int topx = 327;
  public static int topy = 61;
  public static ArrayList<String> urls = new ArrayList<String>();

  public static void d2() throws Exception {
    String dun = "dun.txt";
    fileutil.delete(dun);
    fileutil.writenew("", dun);
    for (int i = 0; i < 30; ++i) {
      util.click(urlx, urly);
      Thread.sleep(100);
      util.click(topx, topy);
      util.combo(KeyEvent.VK_CONTROL, KeyEvent.VK_C);
      String b = util.getBoard();
      urls.add(b);
      util.rightclick(urlx, urly);
      Thread.sleep(100);
      util.pressKey(KeyEvent.VK_UP);
      Thread.sleep(100);
      util.pressKey(KeyEvent.VK_ENTER);
      Thread.sleep(100);
      System.out.println(b);
      fileutil.append("\n" + b, dun);
    }
  }

  public static void doer() throws Exception {
    String s = fileutil.read("dun.txt");
    String[] lines = s.split("\n");
    ArrayList<String> foff = new ArrayList<String>();
    for (String f : lines) {
      String f1 = f.replace("//", "/");
      String f2 = f1.split("/")[1];
      foff.add("https://" + f2);
    }
    // String comm = "mkdir "; String com1 = " && cd "; String com2 = " && nohup httrack ";
    // String comm2 = " +*.jpg -*.wiki* --near --advanced-maxlinks=10000000000000 -s0 > s.txt &";
    String foo = "";
    for (String f : foff) {
      String sf = f;
      sf = sf.replace("\r", "");
      sf = sf.replace("  ", "");
      foo = foo + " " + sf;
    }
    String f = "nohup httrack " + foo
        + " +*.jpg -*.wiki* --near --advanced-maxlinks=10000000000000 -s0 > s.txt &";
    f = f.replace("  ", " ");
    System.out.println(f);
  }

}
