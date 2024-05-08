package test.wndows.copier.sb.util.code.zogapp;

import java.awt.Rectangle;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.util.HashMap;
import javax.imageio.ImageIO;
import javax.imageio.stream.MemoryCacheImageInputStream;

public class importdata {

  // basrah is 30 n 47 e

  int maxcolor = 765;
  public static double maxx = 0;
  public static double maxy = 0;
  public static HashMap<Integer, Integer> ff = new HashMap<Integer, Integer>();

  public static void importing() throws Exception {
    File f = new File("img.jpg");
    load(f);
  }

  public static int getcolor(int x, int y) {
    x = getnice(x, y);
    return sumcolor(x);
  }

  public static int sumcolor(int in) {
    String s = Integer.toBinaryString(in);
    s = s.substring(8); // alpha removed
    String red = s.substring(0, 8);
    String green = s.substring(8, 16);
    String blue = s.substring(16, 24);
    int redi = Integer.parseInt(red, 2);
    int greeni = Integer.parseInt(green, 2);
    int bluei = Integer.parseInt(blue, 2);
    redi = redi + greeni + bluei;
    return redi;
  }

  public static int getnice(int x, int y) {
    int realx = x * (int) maxx;
    x = realx + y;
    return ff.get(x);
  }

  static HashMap<Integer, Integer> load(File f) throws Exception {
    FileInputStream fileInputStream = new FileInputStream(f);
    MemoryCacheImageInputStream memoryCache = new MemoryCacheImageInputStream(fileInputStream);
    BufferedImage bufferedImage = ImageIO.read(memoryCache);
    Rectangle r = bufferedImage.getRaster().getBounds();
    maxx = r.getMaxX();
    maxy = r.getMaxY();
    int res = 0;
    int counter = 0;
    for (int i = 0; i < maxx; ++i) {
      for (int k = 0; k < maxy; ++k) {
        res = bufferedImage.getRGB(i, k);
        ff.put(counter, res);
        ++counter;
      }
    }
    return ff;
  }

}
