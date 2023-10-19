package test.copier;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.math.BigInteger;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;

public class Copier {

  public static String p1 = "D:\\2023\\foo\\";
  public static String p2 = "C:\\Users\\a\\Documents\\files\\";
  public static String p3 = "t4xph68cjydb1.jpg";
  public static ArrayList<String> allfiles = new ArrayList<String>();
  public static int copcount = 0;

  public static void dof() throws Exception {
    walk(p2);
    for (String s : allfiles) {
      doFile(s);
    }
  }

  public static int countperiods(String in) {
    char someChar = '.';
    int count = 0;
    for (int i = 0; i < in.length(); ++i) {
      if (in.charAt(i) == someChar) {
        count++;
      }
    }
    return count;
  }

  public static String doperiods(String in) {
    String[] str = in.split(".");
    String ext = str[str.length - 1];
    String without = in.replace(ext, "");
    without = without.replace(".", "");
    in = without + "." + ext;
    return in;

  }

  public static void doFile(String copyf) {
    try {
      System.out.println("copying " + copyf);
      File copy = new File(copyf);
      String temp = copyf.replace("\\", "\\");
      temp = temp.replace(p2, "");
      if (countperiods(temp) > 1) {
        System.out.println("too many periods");
        temp = doperiods(temp);
      }
      String copiedto = temp;
      System.out.println(copiedto);
      File copied = new File(p1 + copiedto);
      InputStream in = new BufferedInputStream(new FileInputStream(copy));
      System.out.println("input opened");
      if (!copied.getParentFile().exists()) {
        System.out.println("making dir");
        copied.getParentFile().mkdirs();
      }
      int total = allfiles.size();
      copcount += 1;
      System.out.println("count is " + copcount + " of " + total);
      OutputStream out = new BufferedOutputStream(new FileOutputStream(copied));
      System.out.println("output opened");
      byte[] buffer = new byte[1000000000];
      int lengthRead;
      System.out.println("beginning read");
      while ((lengthRead = in.read(buffer)) > 0) {
        System.out.println("writing buffer");
        out.write(buffer, 0, lengthRead);
        System.out.println("done writing");
        out.flush();
        System.out.println("flushing");
      } ;
      System.out.println("here ending");
      in.close();
      System.out.println("in close");
      out.close();
      System.out.println("out close");
    } catch (Exception e) {
      System.out.println("fail");
      e.printStackTrace();
      System.exit(0);
    }
  }

  public static void walk(String path) {
    File root = new File(path);
    File[] list = root.listFiles();
    if (list == null)
      return;
    for (File f : list) {
      if (f.isDirectory()) {
        walk(f.getAbsolutePath());
        System.out.println("path " + f.getAbsolutePath());
      } else {
        System.out.println("File: " + f.getAbsoluteFile());
        allfiles.add(f.getAbsolutePath());
      }
    }
  }

  public static void bar() throws NoSuchAlgorithmException, IOException {
    System.out.println("Are identical: " + isIdentical("c:\\myfile.txt", "c:\\myfile2.txt"));
  }

  public static boolean isIdentical(String leftFile, String rightFile)
      throws IOException, NoSuchAlgorithmException {
    return md5(leftFile).equals(md5(rightFile));
  }

  private static String md5(String file) throws IOException, NoSuchAlgorithmException {
    MessageDigest digest = MessageDigest.getInstance("MD5");
    File f = new File(file);
    InputStream is = new FileInputStream(f);
    byte[] buffer = new byte[8192];
    int read = 0;
    try {
      while ((read = is.read(buffer)) > 0) {
        digest.update(buffer, 0, read);
      }
      byte[] md5sum = digest.digest();
      BigInteger bigInt = new BigInteger(1, md5sum);
      String output = bigInt.toString(16);
      return output;
    } finally {
      is.close();
    }
  }

}
