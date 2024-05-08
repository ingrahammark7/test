package test.wndows.copier.sb.util.code.z2app;

import java.util.ArrayList;
import test.wndows.copier.sb.util.web.fileutil;

// gallery-dl -i C:\Users\a\Documents\GitHub\test\foo.txt --http-timeout 1000

public class zogapp {

  public static void doer() throws Exception {
    String s = fileutil.read("dun.txt");
    String[] lines = s.split("\n");
    ArrayList<String> foff = new ArrayList<String>();
    for (String f : lines) {
      String f1 = f.replace("//", "/");
      String f2 = f1.split("/")[1];
      foff.add("https://" + f2);
    }
    String comm = "mkdir ";
    String com1 = " && cd ";
    String com2 = " && nohup httrack ";
    String comm2 =
        " +*.jpg -*.wiki* --near --advanced-maxlinks=10000000000000 -s0 > s.txt &; cd ..";
    for (String f : foff) {
      Thread.sleep(2);
      String ss = String.valueOf(System.currentTimeMillis());
      String sf = comm + ss + com1 + ss + com2 + f + comm2;
      sf = sf.replace("\r", "");
      sf = sf.replace("  ", "");
      System.out.println(sf);
    }
  }

}
