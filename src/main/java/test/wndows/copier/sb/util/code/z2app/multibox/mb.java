package test.wndows.copier.sb.util.code.z2app.multibox;

import test.wndows.copier.sb.util.web.fileutil;

public class mb {

  public static String mandir =
      "C:\\Users\\a\\AndroidStudioProjects\\MyApplication\\app\\src\\main\\";
  public static String manif = "AndroidManifest.xml";
  public static String manc = mandir + manif;
  public static String mm =
      "C:\\Users\\a\\AndroidStudioProjects\\MyApplication\\app\\src\\main\\java\\com\\example\\";
  public static String anme = "myapplication";
  public static String an2 = mm + anme;
  public static String l1 = "MYapp";
  public static String ltext = "label=\"";

  public static void doman(int number) throws Exception {
    String f = fileutil.read(manc);
    String[] ff = f.split(anme);
    f = ff[0] + anme + number + "." + ff[1];
    String[] f3 = f.split(ltext);
    String f4 = f3[1].split("\"")[0];
    f = f.replace(f4, l1 + number);
    fileutil.replacefile(manc, f);
    renamefolder(number);
  }

  public static void renamefolder(int number) throws Exception {

  }

}
