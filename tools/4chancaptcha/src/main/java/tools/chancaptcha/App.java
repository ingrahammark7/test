package tools.chancaptcha; 

import java.awt.MouseInfo;
import java.awt.Point;
import java.awt.Robot;
import java.awt.event.KeyEvent;

public class App {
	public static void main(String[] args) throws Exception {
		for (int i = 0; i < 300; ++i) {
			log();
		}

	}

	public static void log() throws Exception {
		tools.dourl();
		Robot bot = new Robot();
		tools.dopress(bot, KeyEvent.VK_HOME);
		tools.cli(bot, 941, 275, 100); // open reply
		Thread.sleep(1000);
		tools.cli(bot, 895, 431, 100); // chooise file
		Thread.sleep(1000);
		tools.dopress(bot, KeyEvent.VK_ENTER); // pointless enter needed
		tools.cli(bot, 257, 170, 100); // image seelcted first
		tools.dopress(bot, KeyEvent.VK_DELETE);
		Thread.sleep(500);
		tools.cli(bot, 257, 170, 100); // select image again
		Thread.sleep(500);
		tools.dopress(bot, KeyEvent.VK_ENTER); // submit image
		Thread.sleep(500);
		tools.cli(bot, 1121, 298, 100);
		Thread.sleep(90000);
	}

	public static void getpos() throws Exception {
		Robot bot = new Robot();
		Point l = MouseInfo.getPointerInfo().getLocation();
		System.out.println("ine " + l.x + " " + l.y);
		Thread.sleep(1000);
	}
}