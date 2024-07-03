package test.wndows.copier.sb.util.web;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.FilenameFilter;
import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;

public class fileutil {

  public static void write(String s) throws Exception {
    writenew(s, "foo.txt");
  }

  public static void replacefile(String filename, String newtext) throws Exception {
    delete(filename);
    writenew(newtext, filename);
  }

  public static void writenew(String s, String name) throws Exception {
    s = s.replace(" ", "");
    String str = s;
    BufferedWriter writer = new BufferedWriter(new FileWriter(name, true));
    writer.write(str);
    writer.close();
  }

  public static void removelast(String s) throws Exception {
    String ss = read(s);
    String[] f = ss.split("\n");
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < f.length - 1; ++i) {
      sb.append(f[i]);
      if (i < f.length - 2)
        sb.append("\n");
    }
    delete(s);
    writenew(sb.toString(), s);
  }

  public static void append(String s, String name) throws Exception {
    String f = read(name) + s;
    delete(name);
    writenew(f, name);
  }

  public static String read(String s) throws Exception {
    s = s.replace(" ", "");
    BufferedReader readre = new BufferedReader(new FileReader(s));
    StringBuilder content = new StringBuilder();
    int nextChar;
    while ((nextChar = readre.read()) != -1) {
      content.append((char) nextChar);
    }
    readre.close();
    return String.valueOf(content);
  }

  public static void makedir(String s) throws Exception {
    s = s.replace(" ", "");
    File f = new File(s);
    f.mkdirs();
    f.createNewFile();
  }

  public static void delete(String s) {
    s = s.replace(" ", "");
    File f = new File(s);
    f.delete();
  }

  public static String[] list2array(ArrayList<String> array) {
    String[] newf = new String[array.size()];
    for (int i = 0; i < newf.length; ++i) {
      newf[i] = array.get(i);
    }
    return newf;
  }

  public static String removelastpath(String s) {
    s = s.replace("\\", "/");
    String[] f = s.split("/");
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < f.length; ++i) {
      if (i == f.length - 1)
        continue;
      sb.append(f[i] + "/");
    }
    return sb.toString();
  }

  public static Boolean isempty(String savedir) throws IOException {
    DirectoryStream<Path> directory = Files.newDirectoryStream(Path.of(savedir));
    if (directory.iterator().hasNext()) {
      directory.close();
      return false;
    }
    directory.close();
    return true;
  }

  public static String[] subdirs(String s) {
    File f = new File(s);
    String[] dirs = f.list(new FilenameFilter() {
      @Override
      public boolean accept(File current, String name) {
        return new File(current, name).isDirectory();
      }
    });
    return dirs;
  }

  public static boolean containsarray(String s, String[] arr) {
    for (String ss : arr) {
      if (ss.equals(s))
        return true;
    }
    return false;
  }

  public static String ff =
      "https://web.archive.org/web/20101230082430/http://mailer.fsu.edu/~akirk/tanks/UnitedStates/unarmored-halftracks/unarmored-half-tracks.html\r\n"
          + "https://web.archive.org/web/20080302112911/http://www.transchool.eustis.army.mil/museum/museum.html\r\n"
          + "https://web.archive.org/web/20111005150532/http://stampedout.net/odds-011-snl.html\r\n"
          + "https://web.archive.org/web/20180110201527/http://golem.fjfi.cvut.cz/wiki/\r\n"
          + "https://web.archive.org/web/20160310105056/http://www.ipr.res.in/sst1/documents/sst-1_cryogenics.html\r\n"
          + "https://web.archive.org/web/20050225172107/http://www.kiae.ru/eng/str/inf/o11nsi.htm\r\n"
          + "https://web.archive.org/web/20220110062218/https://ktm.nnc.kz/\r\n"
          + "https://web.archive.org/web/20130409180149/http://h1nf.anu.edu.au/\r\n"
          + "https://web.archive.org/web/20161006104622/http://kehilalinks.jewishgen.org/drohobycz/maps/Map_oilfields.asp\r\n"
          + "https://web.archive.org/web/20070125075744/https://www.bankofguyana.org.gy/bansystab.htm\r\n"
          + "https://web.archive.org/web/20100125205946/http://www.brh.net/\r\n"
          + "https://web.archive.org/web/20070121082858/http://www.centralbank.an/\r\n"
          + "https://web.archive.org/web/20070203135858/http://www.avianosec.com/\r\n"
          + "https://web.archive.org/web/20220324054051/https://www.ou.edu/englhale/meinkampf.html\r\n"
          + "https://web.archive.org/web/20240613155309/https://kostromka.ru/\r\n"
          + "https://web.archive.org/web/20120121035304/https://www.oakingtonplane.co.uk/\r\n"
          + "https://web.archive.org/web/20140309200838/http://www.viagginellastoria.it/caproni/illibro.htm\r\n"
          + "https://web.archive.org/web/20220118171536/http://www.flyingmachines.org/\r\n"
          + "https://web.archive.org/web/20170611200243/https://ivchenko-progress.com/?portfolio=d18t&lang=en\r\n"
          + "https://web.archive.org/web/20200315004149/https://members.ziggo.nl/henrikaper/koolhoven/worlds-first-airliner/\r\n"
          + "https://web.archive.org/web/20040629132156/http://bora1.ssec.wisc.edu/~experiments/atost2003/viewer/\r\n"
          + "https://web.archive.org/web/20050407093921/http://web.wt.net/~kikuko/Do17depot/Do17index.htm\r\n"
          + "https://web.archive.org/web/20120112030302/http://ktsorens.tihlde.org/flyvrak/buvikvoll.html\r\n"
          + "\r\n" + "https://web.archive.org/web/20170506140621/https://www.ju88.net/\r\n" + "";

  public static void d3() {
    String arch = "https://web.archive.org/web/";
    String[] f2 = ff.split("\r\n");
    StringBuilder sb = new StringBuilder();
    StringBuilder s2 = new StringBuilder();
    for (int i = 0; i < f2.length; ++i) {
      String m = f2[i];
      m = m.replace(arch, "");
      System.out.println(m);
      try {
        m = m.split("http")[1];
      } catch (Exception e) {
      }
      m = m.replace("://", "");
      m = m.split("/")[0];
      m = "+*" + m + "* ";
      sb.append(m);
    }
    for (String sf : f2) {
      s2.append(sf + " ");
    }
    String s3 = s2.toString().replace("www.", "");
    s3 = removeq(s3);
    String m = "nohup httrack " + s3 + " -* " + sb.toString()
        + "+*.jpg -*.wiki* --near --advanced-maxlinks=10000000000000 -s0 > s.txt &";
    System.out.println(m);

  }

  public static String removeq(String s) {
    String[] ff = s.split(" ");
    StringBuilder sb = new StringBuilder();
    for (String f3 : ff) {
      f3 = f3.replace("?", " ");
      f3 = f3.split(" ")[0];
      sb.append(f3 + " ");
    }
    String s3 = sb.toString();
    return s3;
  }

}
