package test.wndows.copier.sb.util.web;

import java.io.BufferedWriter;
import java.io.FileWriter;

public class fileutil {

  public static void write(String s) throws Exception {
    String str = s;
    BufferedWriter writer = new BufferedWriter(new FileWriter("foo.txt"));
    writer.write(str);
    writer.close();
  }

}
