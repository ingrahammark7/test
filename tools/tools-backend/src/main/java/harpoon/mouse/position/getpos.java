package harpoon.mouse.position;

import java.awt.AWTException;
import java.awt.MouseInfo;
import java.awt.Point;
import java.awt.Robot;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;

public class getpos {

	public static int wait = 500;
	public static int shortwait = 100;
	public static int left = 572;
	public static int top = 116;
	public static int bottom = 1333 / 2;
	public static int right = 766;

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
		doclick(bot); // place unit
		doPress(bot, KeyEvent.VK_DOWN); // select type of unit
		Thread.sleep(wait);
		doOK(bot);
		Thread.sleep(wait);
		cli(bot, 762, 881);
		Thread.sleep(wait);
		cli(bot, 762, 880); // double click on specific unit
		Thread.sleep(wait);
		doOK(bot);
	}

	public static void cli(Robot bot, int x, int y) throws InterruptedException {
		bot.mouseMove(x, y);
		doclick(bot);
	}

	public static void doPress(Robot bot, int event) throws InterruptedException {
		bot.keyPress(event);
		bot.keyRelease(event);
		Thread.sleep(wait);
	}

	public static void doclick(Robot bot) throws InterruptedException {
		bot.mousePress(InputEvent.BUTTON1_DOWN_MASK);
		Thread.sleep(wait);
		bot.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
	}

	public static void doOK(Robot bot) throws InterruptedException {
		doCombo(bot, KeyEvent.VK_ALT, KeyEvent.VK_O);
	}

	public static void doCombo(Robot bot, int one, int two) throws InterruptedException {
		bot.keyPress(one);
		bot.keyPress(two);
		Thread.sleep(shortwait);
		bot.keyRelease(one);
		bot.keyRelease(two);
	}

}
