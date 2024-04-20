package test.wndows.copier.sb.util.apputil;

import java.util.ArrayList;
import test.wndows.copier.sb.util.SBmain;
import test.wndows.copier.sb.util.web.fileutil;

public class dophone {


  public static void direr(String craw1, String crawp, String direr, String device)
      throws Exception {
    System.gc();
    String temper = sbutils.tempdir + craw1 + ".txt";
    String args = "start " + sbutils.foffer + " " + device + " " + direr + " " + temper + " "
        + sbutils.tempdir;
    SBmain.doer(args);
    String res = fileutil.read(temper);
    fileutil.delete(temper);
    SBmain.doer("start " + sbutils.lsoffer + " " + device + " " + direr + " " + temper + " "
        + sbutils.tempdir);
    String r1 = fileutil.read(temper);
    fileutil.delete(temper);
    String[] files = res.split("\n");
    files = removelsof(files, r1);
    String savedir = sbutils.storedir + direr + device + System.currentTimeMillis();
    fileutil.makedir(savedir);
    String temp = savedir;
    for (String ss : files) {
      if (checkiflib(ss)) {
        dolib(ss, direr, sbutils.tempdir, craw1, crawp, device, savedir);
      }
      dofile(direr, ss, crawp, craw1, device, savedir, sbutils.savedrive);
    }
    deleteempty(temp);
    fileutil.delete(temper);
  }

  public static void deleteempty(String savedir) throws Exception {
    if (fileutil.isempty(savedir))
      fileutil.delete(savedir);
    String s = fileutil.removelastpath(savedir);
    String[] dirs = fileutil.subdirs(s);
    for (String ss : dirs) {
      ss = s + ss;
      if (fileutil.isempty(ss))
        fileutil.delete(ss);
    }
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
    String com = "start " + sbutils.pulff + " " + device + " " + direr + " " + "foo" + " "
        + sbutils.tempdir + " " + sbutils.storedir + " " + savedrive + " " + savedir;
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
      dofile(direr, ss, crawp, craw1, device, savedir, sbutils.savedrive);
    }
  }

  public static boolean checkiflib(String ss) {
    char[] ff = ss.toCharArray();
    for (int i = 0; i < ff.length; ++i) {
      char s = ff[i];
      if (Character.isDigit(s))
        continue;
      if (i > 5)
        return true;
      return false;
    }
    return true;
  }

}
