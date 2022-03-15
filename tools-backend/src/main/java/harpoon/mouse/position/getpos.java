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
		doPress(bot, KeyEvent.VK_E);
		doPress(bot, KeyEvent.VK_U);
		doPress(bot, KeyEvent.VK_A);
		bot.mouseMove(x, y);
		doclick(bot);
		doPress(bot, KeyEvent.VK_DOWN);
		Thread.sleep(500);
		cli(bot, 462, 362); // ok add ship
		cli(bot, 420, 559); // select ship
		cli(bot, 418, 969); // ok selected shipeua
	}

	public static void cli(Robot bot, int x, int y) throws InterruptedException {
		bot.mouseMove(x, y);
		doclick(bot);
	}

	public static void doPress(Robot bot, int event) {
		bot.keyPress(event);
		bot.keyRelease(event);
	}

	public static void doclick(Robot bot) throws InterruptedException {
		bot.mousePress(InputEvent.BUTTON1_DOWN_MASK);
		Thread.sleep(10);
		bot.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
	}

}
