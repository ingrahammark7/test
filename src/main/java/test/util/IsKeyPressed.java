package test.util;

import java.io.File;
import java.util.Scanner;

public class IsKeyPressed {
  public static boolean wpressed = false;

  // windows N creates f.txt

  public static boolean iswpressed() {
    try {
      File f = new File("c:\\users\\a\\documents\\f.txt");
      if (f.isFile() == true)
        return true;
      Scanner myr = new Scanner(f);
      while (myr.hasNextLine()) {
        String foo = myr.nextLine();
        System.out.println(foo);
      }
    } catch (Exception e) {
      return wpressed;
    }
    return true;

  }

}
