package test.wndows.copier;

import test.wndows.copier.sb.util.SBmain;
import test.wndows.copier.sb.util.web.fileutil;

public class app {

  public static String temp = " C:/Games/f.txt";
  public static String tempfile = " >" + temp;

  public static void main(String[] args) throws Exception {
    fileutil.delete(temp);
    SBmain.doer("dir" + tempfile);

  }



}
