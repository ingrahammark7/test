package tools.chancaptcha.fc.util;

import java.awt.AWTException;
import java.awt.MouseInfo;
import java.awt.Point;
import java.awt.Robot;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;

public class fcutil {

	public static long wait = 1000L;

	public static void getPos() {
		Point spot = MouseInfo.getPointerInfo().getLocation();
		System.out.println(String.valueOf(spot.getX()) + "," + String.valueOf(spot.getY()));
	}

	public static void dolocationclick(Robot bot, int x, int y) throws InterruptedException {
		Thread.sleep(wait);
		cli(bot, x, y);
		Thread.sleep(wait);
		cli(bot, x, y + 1); // double click on specific unit
		Thread.sleep(wait);
	}

	public static void enter(Robot bot) throws Exception {
		fcutil.dopress(bot, KeyEvent.VK_ENTER);
	}

	public static void click(int x, int y) throws AWTException, InterruptedException {
		Robot bot = new Robot();
		dopress(bot, KeyEvent.VK_E);
		dopress(bot, KeyEvent.VK_U);
		dopress(bot, KeyEvent.VK_A);
		bot.mouseMove(x, y);
		doclick(bot); // place unit
		dopress(bot, KeyEvent.VK_DOWN); // select type of unit
		doOK(bot);
		dolocationclick(bot, 100, 100);
		doOK(bot);
	}

	public static void dopress(Robot bot, int event) throws InterruptedException {
		bot.keyPress(event);
		bot.keyRelease(event);
		Thread.sleep(wait);
	}

	public static void dopressDelay(Robot bot, int event, int delay) throws InterruptedException {
		bot.keyPress(event);
		Long l = Integer.toUnsignedLong(delay);
		Thread.sleep(l);
		bot.keyRelease(event);
		Thread.sleep(wait);
	}

	public static void doPresstimes(Robot bot, int event, int times) throws Exception {
		for (int i = 0; i < times; ++i) {
			bot.keyPress(event);
			Thread.sleep(10L);
			bot.keyRelease(event);
			Thread.sleep(10L);
		}
	}

	public static void doclick(Robot bot) throws InterruptedException {
		bot.mousePress(InputEvent.BUTTON1_DOWN_MASK);
		bot.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
	}

	public static void doOK(Robot bot) throws InterruptedException {
		Thread.sleep(wait);
		doCombo(bot, KeyEvent.VK_ALT, KeyEvent.VK_O);
	}

	public static void doCombo(Robot bot, int one, int two) throws InterruptedException {
		bot.keyPress(one);
		bot.keyPress(two);
		bot.keyRelease(one);
		bot.keyRelease(two);
	}

	public static void cli(Robot bot, int x, int y) throws InterruptedException {
		bot.mouseMove(x, y);
		doclick(bot);
	}

}
