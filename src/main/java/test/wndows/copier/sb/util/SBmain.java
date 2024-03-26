package test.wndows.copier.sb.util;

import java.util.ArrayList;
import test.wndows.copier.sb.util.web.fileutil;
import test.wndows.copier.sb.util.web.webutil;

public class SBmain {


  public static void dof() throws Exception {
    try {
      ArrayList<String> foof = new ArrayList<String>();
      String ssf = fileutil.read("in.txt");
      String[] ff = ssf.split("\n");
      for (int i = 0; i < ff.length; ++i) {
        foof.add(ff[i]);
      }
      for (int i = 0; i < foof.size(); ++i) {
        String s = webutil.doreq(foof.get(i));
        String[] ss = s.split("\"authorId\":\"");
        s = ss[1];
        s = s.split("\"")[0];
        s = "https://www.pixiv.net/en/users/" + s + "\n";
        fileutil.write(s);
      }
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  public static void sb() throws Exception {
    // util.getpos();
    dof();
  }

}
