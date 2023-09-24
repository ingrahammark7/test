package test;

import java.awt.MouseInfo;
import java.awt.Point;

public class util {

  public static int wx = 150;
  public static int wy = 52;
  public static int flattenwx = 6;// top left corner of height window
  public static int flattenwy = 715;
  public static int flx = flattenwx + 21;
  public static int fly = flattenwy + 89;
  public static int frx = flx + 65;
  public static int fry = fly;
  public static int heightx = flx + 143;
  public static int heighty = fly - 2;
  public static int ewx = 3;
  public static int ewy = 48;
  public static int rscrollx = ewx + 1711;
  public static int rscrolly = ewy - 11;
  public static int lscrollx = ewx + 1694;
  public static int lscrolly = ewy + 977;

  public static void getpos() throws Exception {
    while (true) {
      Thread.sleep(1000);
      Point p = MouseInfo.getPointerInfo().getLocation();
      int x = p.x;
      int y = p.y;
      System.out.println("x " + x + " y " + y);
    }
  }
  // window corner x 150 y 52
  // flatten left 142 452
  // flatten right 207 452
  // height entry 285 450
  //



}
