package test.wndows.copier.sb.util;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.function.Consumer;

public class SBmain implements Runnable {

  public InputStream inputStream;
  public Consumer<String> consumer;


  public SBmain(InputStream inputStream2, Consumer<String> dis) {}



  @Override
  public void run() {
    new BufferedReader(new InputStreamReader(inputStream)).lines().forEach(consumer);
  }

  public static void doer() throws Exception {
    List<String> commands = new ArrayList<String>();
    commands.add("cmd.exe");
    commands.add("dir");
    ProcessBuilder pb = new ProcessBuilder(commands);
    pb.directory(new File("c:/windows/system32/"));
    pb.redirectErrorStream(true);
    Process process = pb.start();
    StringBuilder out = new StringBuilder();
    BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream()));
    String line = "", previous = "";
    while ((line = br.readLine()) != null) {
      if (line.equals(previous)) {
        previous = line;
        out.append(line).append('\n');
        System.out.println(line);
      }
      if (process.waitFor() == 0) {
        System.out.println("suces");
        System.exit(0);
      }
      System.out.println(commands);
      System.out.println(out.toString());
      System.exit(0);
    }
  }

  public static void do2() throws Exception {
    Process process;
    String[] f = new String[1];
    f[0] = "C";
    process = Runtime.getRuntime().exec("cmd.exe", f);
    Consumer<String> dis = a -> System.out.println(a);
    SBmain streamGobbler = new SBmain(process.getInputStream(), dis);
    ExecutorService executorService = Executors.newFixedThreadPool(10);
    Future<?> future = executorService.submit(streamGobbler);
    executorService.execute(streamGobbler);
    future.get(10, TimeUnit.SECONDS);
    executorService.shutdown();
  }

}
