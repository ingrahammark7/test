package test.copier;

import java.awt.event.KeyEvent;
import java.util.ArrayList;
import test.sb.util.util;

public class Copier {

  public static String p1 = "D:\\2023\\foo\\";
  public static String p2 = "C:\\Users\\a\\Downloads\\";
  public static String p3 = "https://vk.com/wall-200782618?offset=";
  public static ArrayList<String> allfiles = new ArrayList<String>();
  public static int increment = 20;
  public static int pages = 430;
  public static int offset = increment * pages;
  public static String p4 = p3 + offset;
  public static int addressx = 461;
  public static int addressy = 60;
  public static int emptyx = 269;
  public static int emptyy = 284;
  public static ArrayList<String> urllist = new ArrayList<String>();
  public static String base = "https://vk.com/";
  public static int pdfx = 944;
  public static int pdfy = 642;

  public static void dof() throws Exception {
    try {
      for (int i = (pages * increment) - increment; i > 0; i = i - increment) {
        runs(p3 + i);
      }
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  public static void runs(String board) throws Exception {
    util.click(addressx, addressy);
    util.combo(KeyEvent.VK_CONTROL, KeyEvent.VK_A);
    util.pressKey(KeyEvent.VK_DELETE);
    util.setBoard(board);
    util.combo(KeyEvent.VK_CONTROL, KeyEvent.VK_V);
    util.pressKey(KeyEvent.VK_ENTER);
    Thread.sleep(5000);
    util.combo(KeyEvent.VK_CONTROL, KeyEvent.VK_U);
    Thread.sleep(5000);
    util.click(emptyx, emptyy);
    util.combo(KeyEvent.VK_CONTROL, KeyEvent.VK_A);
    Thread.sleep(100);
    util.combo(KeyEvent.VK_CONTROL, KeyEvent.VK_C);
    String result = util.getBoard();
    geturls(result);
  }

  public static void geturls(String res) throws Exception {
    try {
      res.replaceAll("dist/web/docs", "");
      String[] reps = res.split("/doc");
      for (int i = 1; i < reps.length; ++i) {
        String rr = reps[i].split("\"")[0];
        rr = base + "doc" + rr;
        util.enterurl(addressx, addressy, rr);
        util.click(pdfx, pdfy);
        Thread.sleep(5000);
      }
      urllist.clear();
    } catch (Exception e) {
      e.printStackTrace();
    }
    util.combo(KeyEvent.VK_CONTROL, KeyEvent.VK_F4);
  }

}
