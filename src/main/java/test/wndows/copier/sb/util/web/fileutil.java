package test.wndows.copier.sb.util.web;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;

public class fileutil {

  public static void write(String s) throws Exception {
    String str = s;
    BufferedWriter writer = new BufferedWriter(new FileWriter("foo.txt", true));
    writer.write(str);
    writer.close();
  }

  public static String read(String s) throws Exception {
    BufferedReader readre = new BufferedReader(new FileReader(s));
    StringBuilder content = new StringBuilder();
    int nextChar;
    while ((nextChar = readre.read()) != -1) {
      content.append((char) nextChar);
    }
    readre.close();
    return String.valueOf(content);
  }

}
