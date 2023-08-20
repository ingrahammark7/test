package test;

import java.awt.AWTException;
import java.awt.Robot;
import java.awt.event.KeyEvent;

public class app {



  public static void main(String[] args) throws Exception {
    try {
      Robot robot = new Robot();

      while (true) {
        Thread.sleep(5000);
        robot.keyPress(KeyEvent.VK_END);
      }
    } catch (AWTException e) {
      e.printStackTrace();
    }
  }

}
