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
    System.out.println("size is " + map.size());
    Set<Integer> key1 = map.keySet();
    Iterator<Integer> key1it = key1.iterator();
    Integer temp = 0;
    while (key1it.hasNext()) {
      temp = key1it.next();
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
    int counter = 0;
    for (int i = 0; i < maxx / 10; ++i) {
      for (int k = 0; k < maxy; ++k) {
        res = bufferedImage.getRGB(i, k);
        ff.put(counter, res);
        ++counter;
      }
    }
    return ff;
  }

}
