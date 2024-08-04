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
      "https://web.archive.org/web/20080213085614/http://www.aero-web.org/locator/manufact/lockheed/t-33.htm\r\n"
          + "http://www.faculty.ucr.edu/~legneref/bronze/climate.htm\r\n"
          + "https://web.archive.org/web/20110302105923/http://abakus.narod.ru/bg/biggun.htm\r\n"
          + "https://www.cl.cam.ac.uk/~jgd1000/melanin.html\r\n"
          + "https://web.archive.org/web/20180118011123/http://www.ofbindia.gov.in/products/data/military/3.htm\r\n"
          + "https://web.archive.org/web/20070119000524/http://www.kilometr.pl/MR_GAZ66.html\r\n"
          + "https://web.archive.org/web/20060823215124/http://gaz.toimii.net/\r\n"
          + "https://web.archive.org/web/20110720134602/http://gaz66.livejournal.com/\r\n"
          + "https://web.archive.org/web/20120220085222/http://gaz66.co.uk/\r\n"
          + "https://web.archive.org/web/20170725102740/http://defence.ashokleyland.com/products.html\r\n"
          + "https://web.archive.org/web/20110711080249/http://gaz51.com/\r\n" + "\r\n" + "";

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
      if (m.startsWith("s") && !f2[i].contains(m)) {
        m = m.substring(1);
      }
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
