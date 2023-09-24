package test;

import java.awt.Rectangle;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;
import javax.imageio.ImageIO;
import javax.imageio.stream.MemoryCacheImageInputStream;

public class importdata {

  // basrah is 30 n 47 e

  public static double maxx = 0;
  public static double maxy = 0;

  public static void importing() throws Exception {
    File f = new File("img.jpg");
    HashMap<Integer, Integer> map = load(f);
    readMap(map);
  }

  static void readMap(HashMap<Integer, Integer> map) {

    Set<Integer> key1 = map.keySet();
    Iterator<Integer> key1it = key1.iterator();
    HashMap<Integer, Integer> working = new HashMap<Integer, Integer>();
    int temp = 0;
    int x = 0;
    while (key1it.hasNext()) {
      temp = key1it.next();
      x = temp;
      System.out.println("x is " + temp);
      Set<Integer> set2 = working.keySet();
      System.out.println("size " + set2.size());
      while (working.keySet().iterator().hasNext()) {
        temp = working.keySet().iterator().next();
        System.out.println("working " + x + " " + temp);
      }
    }
  }

  static HashMap<Integer, Integer> load(File f) throws Exception {
    FileInputStream fileInputStream = new FileInputStream(f);
    MemoryCacheImageInputStream memoryCache = new MemoryCacheImageInputStream(fileInputStream);
    BufferedImage bufferedImage = ImageIO.read(memoryCache);
    Rectangle r = bufferedImage.getRaster().getBounds();
    maxx = r.getMaxX();
    maxy = r.getMaxY();
    HashMap<Integer, Integer> ff = new HashMap<Integer, Integer>();
    int res = 0;
    int keyx = 0;
    int maxintx = (int) maxx;
    int maxinty = (int) maxy;
    int[] xkeys = new int[maxintx * maxinty];
    for (int i = 0; i < maxintx; ++i) {
      for (int k = 0; k < maxinty; ++k) {
        int foo = i * maxintx;
        xkeys[i] = foo;
      }
    }
    for (int i = 0; i < maxx; ++i) {
      if (i % 100 == 0)
        System.out.println("progress: " + i / maxx);
      for (int k = 0; k < maxy; ++k) {
        keyx = xkeys[i] + k;
        res = bufferedImage.getRGB(i, k);
        ff.put(keyx, res);
      }
    }
    return ff;
  }

}
