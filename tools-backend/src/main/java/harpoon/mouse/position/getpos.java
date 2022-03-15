package harpoon.mouse.position;

import java.awt.AWTException;
import java.awt.MouseInfo;
import java.awt.Point;
import java.awt.Robot;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;

public class getpos {

	public static void getPos() {
		Point spot = MouseInfo.getPointerInfo().getLocation();
		System.out.println(String.valueOf(spot.getX()) + "," + String.valueOf(spot.getY()));
	}

	public static void click(int x, int y) throws AWTException, InterruptedException {
		Robot bot = new Robot();
		bot.keyPress(KeyEvent.VK_E);
		bot.keyPress(KeyEvent.VK_U);
		bot.keyPress(KeyEvent.VK_A);
		bot.mouseMove(x, y);
		doclick(bot);
		bot.keyPress(KeyEvent.VK_DOWN);
		bot.keyPress(KeyEvent.VK_ENTER);
		cli(bot, 653, 222);
	}

	public static void cli(Robot bot, int x, int y) throws InterruptedException {
		bot.mouseMove(x, y);
		doclick(bot);
	}

	public static void doclick(Robot bot) throws InterruptedException {
		bot.mousePress(InputEvent.BUTTON1_DOWN_MASK);
		Thread.sleep(500);
		bot.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
	}

}
