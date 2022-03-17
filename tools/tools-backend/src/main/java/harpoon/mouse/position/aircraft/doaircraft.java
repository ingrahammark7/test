package harpoon.mouse.position.aircraft;

import java.awt.Robot;
import java.awt.event.KeyEvent;

import harpoon.mouse.position.getpos;

public class doaircraft {
	public static int continuex = 414;
	public static int continuey = 435;

//414 435
	// Five page downs max
	// Adds aircraft
	public static void doa() throws Exception {
		Robot bot = new Robot();
		getpos.dopress(bot, KeyEvent.VK_E);
		getpos.dopress(bot, KeyEvent.VK_U);
		getpos.dopress(bot, KeyEvent.VK_E);
		getpos.doCombo(bot, KeyEvent.VK_ALT, KeyEvent.VK_A);
		getpos.dopress(bot, KeyEvent.VK_PAGE_DOWN);
		getpos.dopress(bot, KeyEvent.VK_PAGE_DOWN);
		getpos.dopress(bot, KeyEvent.VK_PAGE_DOWN);
		getpos.dolocationclick(bot, getpos.selectlocationx - 100, getpos.selectlocationy);
		getpos.doOK(bot);
		getpos.doOK(bot);
		getpos.dolocationclick(bot, continuex, continuey);
	}

	// adds planes to mission
	public static void dom(Robot bot) throws Exception {
		getpos.doCombo(bot, KeyEvent.VK_ALT, KeyEvent.VK_M);
		getpos.dopress(bot, KeyEvent.VK_E);

	}

}