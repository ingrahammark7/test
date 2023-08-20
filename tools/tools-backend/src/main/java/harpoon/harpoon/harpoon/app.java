package harpoon.harpoon.harpoon;

import java.util.ArrayList;

public class app {
	
	public static void main(String args[]) {
		ArrayList<Double> foo = new ArrayList<Double>();
		double b = System.currentTimeMillis();
		int siz = 20000000;
		for(int i = 0; i < siz; ++i) {
			foo.add(i + Math.random());
		}
		b = b - System.currentTimeMillis();
		System.out.println(b);
		for(int i = 0; i < foo.size(); ++i) {
			System.out.println(foo.get(i));
		}
		System.out.println("time " + b);
		System.out.println("size " + siz);
	}

}
