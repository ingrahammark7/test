package test.sb.util;

import java.awt.MouseInfo;
import java.awt.Point;
import java.awt.Robot;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;

public class util {

  public static int flattenwx = 1711;// top left corner of height window
  public static int flattenwy = 742;
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
  public static Robot r = roconstruct();
  public static int startx = 9;
  public static int starty = 49;

  private static Robot roconstruct() {
    try {
      return new Robot();
    } catch (Exception e) {
    }
    return null;
  }

  public static void getpos() throws Exception {
    while (true) {
      if (IsKeyPressed.iswpressed())
        System.exit(0);
      Thread.sleep(1000);
      Point p = MouseInfo.getPointerInfo().getLocation();
      int x = p.x;
      int y = p.y;
      System.out.println("x " + x + " y " + y);
    }
  }

  public static void setel(int el) throws Exception {
    click(heightx, heighty);
    click(heightx, heighty);
    for (int i = 0; i < 20; ++i) {
      pressKey(KeyEvent.VK_BACK_SPACE);
      pressKey(KeyEvent.VK_DELETE);
    }
    typenumber(el);
    click(heightx - 20, heighty);
  }

  public static void click(int x, int y) throws Exception {
    r.mouseMove(x, y);
    Thread.sleep(1);
    r.mousePress(InputEvent.getMaskForButton(KeyEvent.BUTTON1_DOWN_MASK));
    Thread.sleep(1);
    r.mouseRelease(InputEvent.getMaskForButton(KeyEvent.BUTTON1_DOWN_MASK));
    Thread.sleep(1);
  }

  public static void typenumber(int n) throws Exception {
    String temp = Integer.toString(n);
    int[] ng = new int[temp.length()];
    for (int i = 0; i < temp.length(); ++i) {
      ng[i] = temp.charAt(i) - '0';
      int f = ng[i];
      if (f == 0)
        pressKey(KeyEvent.VK_0);
      if (f == 1)
        pressKey(KeyEvent.VK_1);
      if (f == 2)
        pressKey(KeyEvent.VK_2);
      if (f == 3)
        pressKey(KeyEvent.VK_3);
      if (f == 4)
        pressKey(KeyEvent.VK_4);
      if (f == 5)
        pressKey(KeyEvent.VK_5);
      if (f == 6)
        pressKey(KeyEvent.VK_6);
      if (f == 7)
        pressKey(KeyEvent.VK_7);
      if (f == 8)
        pressKey(KeyEvent.VK_8);
      if (f == 9)
        pressKey(KeyEvent.VK_9);
    }
  }

  public static void pressKey(int p) throws Exception {
    Thread.sleep(1);
    r.keyPress(p);
    Thread.sleep(1);
    r.keyRelease(p);
    Thread.sleep(1);
  }

  static int rk = 0;
  static int ri = 0;

  public static void iterate() throws Exception {
    for (int i = 0; i < importdata.maxx / 1000; ++i) {
      if (IsKeyPressed.iswpressed())
        System.exit(0);
      for (int k = 0; k < importdata.maxy / 1000; ++k) {
        rk = k + startx;
        ri = i + starty;
        int col = importdata.getcolor(i, k);
        setel(col);
        click(rk, ri);
      }
    }
  }

}


