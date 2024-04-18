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
    s = s.replace(" ", "");
    String str = s;
    BufferedWriter writer = new BufferedWriter(new FileWriter("foo.txt", true));
    writer.write(str);
    writer.close();
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

}
