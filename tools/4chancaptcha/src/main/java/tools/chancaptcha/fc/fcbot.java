package tools.chancaptcha.fc;

import java.awt.Robot;
import java.awt.event.KeyEvent;
import java.io.BufferedReader;
import java.io.InputStreamReader;

import tools.chancaptcha.fc.util.fcutil;

public class fcbot {

	public static int locationx = 39;
	public static int locationy = 156;
	public static int playx = 1157;
	public static int playy = 389;

	public static void dofc() throws Exception {
		Robot bot = new Robot();
		checkrunning(bot);
		while (true) {
			checkrunning(bot);
			Thread.sleep(60000L);
			dosave(bot);
		}
	}

	public static void checkrunning(Robot bot) throws Exception {
		String pdinfo = "";
		Runtime rt = Runtime.getRuntime();
		Process p = rt.exec("tasklist");
		BufferedReader input = new BufferedReader(new InputStreamReader(p.getInputStream()));
		String line = "";
		while ((line = input.readLine()) != null) {
			pdinfo += line;
		}
		boolean isrunning = false;
		if (pdinfo.contains("Fleet"))
			isrunning = true;
		if (!isrunning)
			open(bot);
		System.out.println("status " + isrunning);
	}

	public static void dosave(Robot bot) throws Exception {
		int savex = 263;
		int savey = 79;
		fcutil.dopress(bot, KeyEvent.VK_G);
		Thread.sleep(1000L);
		fcutil.cli(bot, savex, savey);
		Thread.sleep(1000L);
		fcutil.enter(bot);
		Thread.sleep(1000L);
		fcutil.enter(bot);
		Thread.sleep(1000L);
	}

	public static void open(Robot bot) throws Exception {
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
		fcutil.dopress(bot, KeyEvent.VK_P);
		Thread.sleep(1000L);
		fcutil.dopress(bot, KeyEvent.VK_T);
		Thread.sleep(1000L);
		fcutil.dopress(bot, KeyEvent.VK_T);
		Thread.sleep(1000L);
		fcutil.dopress(bot, KeyEvent.VK_T);
		Thread.sleep(1000L);
		fcutil.dopress(bot, KeyEvent.VK_P);
		Thread.sleep(1000L);
		dosave(bot);
	}
}
