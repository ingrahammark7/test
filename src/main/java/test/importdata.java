package test;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import javax.imageio.ImageIO;
import javax.imageio.stream.MemoryCacheImageInputStream;

public class importdata {

  // basrah is 30 n 47 e

  public static void importing() throws Exception {
    File f = new File("img.jpg");
    load(f);
  }

  static void load(File f) throws Exception {
    FileInputStream fileInputStream = new FileInputStream(f);
    MemoryCacheImageInputStream memoryCache = new MemoryCacheImageInputStream(fileInputStream);
    BufferedImage bufferedImage = ImageIO.read(memoryCache);
    int res = bufferedImage.getRGB(0, 0);
    System.out.println("one " + res);
    res = bufferedImage.getRGB(100, 100);
    System.out.println(res);
  }

}
