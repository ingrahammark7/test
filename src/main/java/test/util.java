package test;

import java.awt.MouseInfo;
import java.awt.Point;
import java.awt.Robot;

public class util {

  public static int wx = 150;
  public static int wy = 52;
  public static int flattenwx = 5;// top left corner of height window
  public static int flattenwy = 35;
  public static int flx = flattenwx + 21;
  public static int fly = flattenwy + 89;
  public static int frx = flx + 65;
  public static int fry = fly;
  public static int heightx = flx + 143;
  public static int heighty = fly - 2;
  public static int ewx = 0;
  public static int ewy = 0;
  public static int rscrollx = ewx + 1714;
  public static int rscrolly = ewy + 39;
  public static int lscrollx = ewx + 1697;
  public static int lscrolly = ewy + 1026;

  public static void getpos() throws Exception {
    while (true) {
      Thread.sleep(1000);
      Point p = MouseInfo.getPointerInfo().getLocation();
      int x = p.x;
      int y = p.y;
      System.out.println("x " + x + " y " + y);
    }
  }

  public static void setel(int el) throws Exception {
    Robot r = new Robot();

  }

  public static void click(Robot r) {

  }
}


