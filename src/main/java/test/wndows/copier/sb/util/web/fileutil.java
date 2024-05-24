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

  public static void writenew(String s, String name) throws Exception {
    s = s.replace(" ", "");
    String str = s;
    BufferedWriter writer = new BufferedWriter(new FileWriter(name, true));
    writer.write(str);
    writer.close();
  }

  public static void append(String s, String name) throws Exception {
    String f = read(name) + "/n" + s;
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
      "https://web.archive.org/web/20030805181154/https://www.csd.uwo.ca/~pettypi/elevon/baugher_other/tsr2.html\r\n"
          + "https://web.archive.org/web/20070207233430/http://www.unrealaircraft.com/classics/arrow.php\r\n"
          + "https://web.archive.org/web/20050306175349/http://prototypes.free.fr/tsr2/tsr2-1.htm\r\n"
          + "https://web.archive.org/web/20070223095454/http://www.chinfo.navy.mil/\r\n"
          + "https://web.archive.org/web/20060527202256/http://aeroflt.users.netlink.co.uk/types/usa/boeing/x-32/X-32.htm\r\n"
          + "https://web.archive.org/web/20050507025857/http://www.danshistory.com/m2000.html\r\n"
          + "https://web.archive.org/web/20020203173146/http://aeroflt.users.netlink.co.uk//profile/d335top.htm\r\n"
          + "https://web.archive.org/web/20010331180545/http://www.sci.fi/~fta/MiG-29.htm\r\n"
          + "https://web.archive.org/web/20050212104820/http://www.canit.se/~griffon/aviation/text/29tunnan.htm\r\n"
          + "https://web.archive.org/web/20050308030536/http://www.utvaaviation.co.yu/index2a.html\r\n"
          + "https://web.archive.org/web/20040217102812/http://aeroweb.lucia.it/~agretch/RAFAQ/Yak-141Freestyle.html\r\n"
          + "";

  public static void d3() {
    String arch = "https://web.archive.org/web/";
    String[] f2 = ff.split("\r\n");
    StringBuilder sb = new StringBuilder();
    StringBuilder s2 = new StringBuilder();
    for (int i = 0; i < f2.length; ++i) {
      String m = f2[i];
      m = m.replace(arch, "");
      System.out.println(m);
      m = m.split("http")[1];
      m = m.replace("://", "");
      m = m.split("/")[0];
      m = "+*" + m + "* ";
      sb.append(m);
    }
    for (String sf : f2) {
      s2.append(sf + " ");
    }

    String m = "nohup httrack " + s2.toString() + " -* " + sb.toString()
        + "+*.jpg -*.wiki* --near --advanced-maxlinks=10000000000000 -s0 > s.txt &";
    System.out.println(m);

  }

}
