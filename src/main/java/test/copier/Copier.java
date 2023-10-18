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

public class Copier {

  public static String p1 = "D:\\2023\\foo\\";
  public static String p2 = "C:\\Users\\a\\Documents\\files\\";
  public static String p3 = "t4xph68cjydb1.jpg";

  public static void dof() throws Exception {
    walk(p2);
  }

  public static void doFile(String copyf, String copiedf) {
    try {
      System.out.println("here");
      File copy = new File(p2 + copyf);
      File copied = new File(p1 + copiedf);
      InputStream in = new BufferedInputStream(new FileInputStream(copy));
      OutputStream out = new BufferedOutputStream(new FileOutputStream(copied));
      byte[] buffer = new byte[1024];
      int lengthRead;
      while ((lengthRead = in.read(buffer)) > 0) {
        out.write(buffer, 0, lengthRead);
        out.flush();
      } ;
      in.close();
      out.close();
    } catch (Exception e) {
      System.out.println("fail");
      e.printStackTrace();
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
