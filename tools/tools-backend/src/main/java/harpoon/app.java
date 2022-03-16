package harpoon;

import harpoon.mouse.position.getpos;

public class app {

	// edit is 653 32
	// screen is 653 232
	public static void main(String[] args) throws Exception {
		while (true) {
			int x = getpos.left + (int) (Math.random() * (getpos.right - getpos.left));
			int y = getpos.top + (int) (Math.random() * (getpos.bottom - getpos.top));
			Thread.sleep(10000);
			getpos.getPos();
			getpos.click(x, y);
		}
	}

}