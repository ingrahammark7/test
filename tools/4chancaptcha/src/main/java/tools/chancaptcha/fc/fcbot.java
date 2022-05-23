package tools.chancaptcha.fc;

import java.awt.Robot;
import java.awt.event.KeyEvent;

import tools.chancaptcha.fc.util.fcutil;

public class fcbot {

	public static int locationx = 39;
	public static int locationy = 156;
	public static int playx = 1157;
	public static int playy = 389;

	public static void dofc() throws Exception {

		Robot bot = new Robot();
		fcutil.dolocationclick(bot, locationx, locationy);
		fcutil.enter(bot);
		fcutil.dolocationclick(bot, playx, playy);
		fcutil.enter(bot);
		Thread.sleep(10000L);
		fcutil.enter(bot);
		Thread.sleep(1000L);
		fcutil.enter(bot);
		Thread.sleep(1000L);
		fcutil.enter(bot);
		Thread.sleep(1000L);
		fcutil.dolocationclick(bot, 220, 240);
		Thread.sleep(1000L);
		fcutil.doPresstimes(bot, KeyEvent.VK_DOWN, 100);
		fcutil.enter(bot);
		fcutil.enter(bot);
		Thread.sleep(10000L);
	}

	public static void open() throws Exception {
		while (true) {
			fcutil.getPos();
			Thread.sleep(1000L);
		}
	}
}
