package harpoon;

import harpoon.mouse.position.getpos;

public class app {

	// edit is 653 32
	// screen is 653 232
	public static void main(String[] args) throws Exception {

		while (true) {
			Thread.sleep(10000);
			getpos.getPos();
			getpos.click(653, 232);

		}
	}

}