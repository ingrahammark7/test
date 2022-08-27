package tools.chancaptcha;

import java.awt.AWTException;
import java.awt.Robot;
import java.awt.Toolkit;
import java.awt.datatransfer.Clipboard;
import java.awt.datatransfer.DataFlavor;
import java.awt.datatransfer.StringSelection;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;

public class tools {

	public static int wait = 500;
	public static int shortwait = 100;
	public static String cookie = "";
	public static Long lastlog = 0L;
	public static Long loginwait = 1000000L;

	public static Boolean checktime() {
		Long now = System.currentTimeMillis();
		if (lastlog == 0L) {
			lastlog = now;
			return true;
		}
		Long diff = now - lastlog;
		if (diff > loginwait) {
			lastlog = now;
			return true;
		}
		return false;
	}

	public static void dologin() throws Exception {
		Robot bot = new Robot();
		String loginurl = "https://www.theeroticreview.com/memberlaunch/login.asp?dest=/myter/index.asp?";
		StringSelection ss = new StringSelection(loginurl);
		Clipboard clip = Toolkit.getDefaultToolkit().getSystemClipboard();
		clip.setContents(ss, null);
		cli(bot, 596, 47, wait);
		doCombo(bot, KeyEvent.VK_CONTROL, KeyEvent.VK_A);
		doCombo(bot, KeyEvent.VK_CONTROL, KeyEvent.VK_V);
		dopress(bot, KeyEvent.VK_ENTER);
		Thread.sleep(3000);
		cli(bot, 994, 492, wait);
		cli(bot, 994, 492, wait);
		Thread.sleep(1000);
		docaptcha(bot);
		docaptcha(bot);
		docaptcha(bot);

	}

	public static void docookie(Robot bot) throws Exception {
		Clipboard clip = Toolkit.getDefaultToolkit().getSystemClipboard();
		dopress(bot, KeyEvent.VK_F12);
		doCombo(bot, KeyEvent.VK_CONTROL, KeyEvent.VK_R);
		cli(bot, 1909, 324, wait);
		cli(bot, 1909, 324, wait);
		cli(bot, 1198, 324, wait);
		cli(bot, 1198, 324, wait);
		cli(bot, 1500, 524, wait);
		cli(bot, 1500, 524, wait);
		doCombo(bot, KeyEvent.VK_CONTROL, KeyEvent.VK_A);
		doCombo(bot, KeyEvent.VK_CONTROL, KeyEvent.VK_C);
		dopress(bot, KeyEvent.VK_F12);
		String foo = "";
		foo = (String) clip.getData(DataFlavor.stringFlavor);
		foo = foo.split("cookie:")[1];
		foo = foo.split("dnt:")[0];
		cookie = foo;
		cookie = cookie.replace("\n", "");
		if (cookie.substring(0, 1).equals(" ")) {
			cookie = cookie.substring(1);
		}
	}

	public static void docaptcha(Robot bot) throws Exception {
		int solving = 0;
		while (solving == 0) {
			doCombo(bot, KeyEvent.VK_CONTROL, KeyEvent.VK_A);
			doCombo(bot, KeyEvent.VK_CONTROL, KeyEvent.VK_C);
			Clipboard clip = Toolkit.getDefaultToolkit().getSystemClipboard();
			String foo = (String) clip.getData(DataFlavor.stringFlavor);
			if (foo.contains("Solving")) {
				Thread.sleep(1000);
			}
			solving = 1;
		}
		cli(bot, 938, 550, wait);
		cli(bot, 938, 550, wait);
		Thread.sleep(1000);
	}

	public static String copyscreen(Robot bot) throws Exception {
		cli(bot, 14, 561, wait);
		doCombo(bot, KeyEvent.VK_CONTROL, KeyEvent.VK_A);
		doCombo(bot, KeyEvent.VK_CONTROL, KeyEvent.VK_C);
		Clipboard clip = Toolkit.getDefaultToolkit().getSystemClipboard();
		String foo = (String) clip.getData(DataFlavor.stringFlavor);
		if (foo.contains("Oklahoma")) {
			System.exit(0);
		}
		if (foo.contains("Verification")) {
			dologin();
		}
		return foo;
	}

	public static String dourl() throws AWTException, Exception {
		String path = "";
		Robot bot = new Robot();
		String base = "https://boards.4chan.org/pol/thread/392812780";
		if (!path.contains("http"))
			path = base + path;
		StringSelection ss = new StringSelection(path);
		Clipboard clip = Toolkit.getDefaultToolkit().getSystemClipboard();
		clip.setContents(ss, null);
		cli(bot, 368, 55, wait); // url bar location
		doCombo(bot, KeyEvent.VK_CONTROL, KeyEvent.VK_A);
		doCombo(bot, KeyEvent.VK_CONTROL, KeyEvent.VK_V);
		dopress(bot, KeyEvent.VK_ENTER);
		System.out.println("doing paste" + path);
		Thread.sleep(3000);
		cli(bot, 1500, 524, wait);
		return "";
	}

	public static void dopress(Robot bot, int event) throws InterruptedException {
		bot.keyPress(event);
		bot.keyRelease(event);
		Thread.sleep(wait);
	}

	public static void doCombo(Robot bot, int one, int two) throws InterruptedException {
		bot.keyPress(one);
		bot.keyPress(two);
		Thread.sleep(shortwait);
		bot.keyRelease(one);
		bot.keyRelease(two);
	}

	public static void cli(Robot bot, int x, int y, int dur) throws InterruptedException {
		bot.mouseMove(x, y);
		doclick(bot, dur);
	}

	public static void doclick(Robot bot, int dur) throws InterruptedException {
		bot.mousePress(InputEvent.BUTTON1_DOWN_MASK);
		Thread.sleep(dur);
		bot.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
	}

}