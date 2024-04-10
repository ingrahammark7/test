package test.wndows.copier.sb.util;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

public class SBmain implements Runnable {

  public InputStream inputStream;
  public Consumer<String> consumer;


  public SBmain(InputStream inputStream2, Consumer<String> dis) {}



  @Override
  public void run() {
    new BufferedReader(new InputStreamReader(inputStream)).lines().forEach(consumer);
  }

  public static List<String> builderc(String command, List<String> in) {
    String[] fs = command.split(" ");
    for (int i = 0; i < fs.length; ++i) {
      in.add(fs[i]);
    }
    return in;
  }

  public static void doer(String c2) throws Exception {
    List<String> commands = new ArrayList<String>();
    commands.add("cmd.exe");
    commands.add("/C");
    commands = builderc(c2, commands);
    ProcessBuilder pb = new ProcessBuilder(commands);
    pb.directory(new File("c:/windows/system32/"));
    pb.redirectErrorStream(true);
    Process process = pb.start();
    StringBuilder out = new StringBuilder();
    BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream()));
    String line = null, previous = null;
    System.out.println("here");
    while ((line = br.readLine()) != null) {
      if (line.equals(previous)) {
        System.out.println("ff34");
        previous = line;
        out.append(line).append('\n');
        System.out.println(line);
        System.out.println("ff");
      }
      if (process.isAlive()) {
        System.out.println("suces");
        System.out.println(out.toString());
        System.exit(0);
      }
      System.out.println("ff2");
      System.out.println("ff4");
      System.out.println(commands);
      System.out.println(out.toString());
      System.exit(0);
    }
  }

}
