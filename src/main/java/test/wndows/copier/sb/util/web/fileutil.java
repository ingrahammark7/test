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
      "https://web.archive.org/web/20230305010255/https://stat.kg/en/statistics/naselenie/\r\n"
          + "https://web.archive.org/web/20220706072339/http://avcom.co.za/airport2/aircraftlist.php?cmd=search&t=aircraft&psearch=&psearchtype=\r\n"
          + "https://web.archive.org/web/20170515152653/http://motca.gov.af/fa\r\n"
          + "https://web.archive.org/web/20190122103236/https://www.gov.je/travel/maritimeaviation/civilaviation/pages/jarapplicationforms.aspx\r\n"
          + "https://web.archive.org/web/20210123133518/http://www.carc.jo/en/content/344-jordanian-registered-aircraft\r\n"
          + "https://web.archive.org/web/20190111091940/https://www.caa.ro/supervizare/registru-operatori-aerieni-romani\r\n"
          + "https://web.archive.org/web/20150907180623/https://www.scaa.sc/index.php?option=com_content&view=article&id=65&Itemid=39\r\n"
          + "https://web.archive.org/web/20140209154818/https://www.aacm.gov.mo/english/aircraft.html\r\n";

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
      f3 = f3.split("?")[0];
      sb.append(f3 + " ");
    }
    return sb.toString();
  }

}
