package test.wndows.copier.sb.util.web;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.FilenameFilter;
import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;

public class fileutil {

  public static void write(String s) throws Exception {
    writenew(s, "foo.txt");
  }

  public static void replacefile(String filename, String newtext) throws Exception {
    delete(filename);
    writenew(newtext, filename);
  }

  public static void writenew(String s, String name) throws Exception {
    s = s.replace(" ", "");
    String str = s;
    BufferedWriter writer = new BufferedWriter(new FileWriter(name, true));
    writer.write(str);
    writer.close();
  }

  public static void removelast(String s) throws Exception {
    String ss = read(s);
    String[] f = ss.split("\n");
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < f.length - 1; ++i) {
      sb.append(f[i]);
      if (i < f.length - 2)
        sb.append("\n");
    }
    delete(s);
    writenew(sb.toString(), s);
  }

  public static void append(String s, String name) throws Exception {
    String f = read(name) + s;
    delete(name);
    writenew(f, name);
  }

  public static String read(String s) throws Exception {
    s = s.replace(" ", "");
    BufferedReader readre = new BufferedReader(new FileReader(s));
    StringBuilder content = new StringBuilder();
    int nextChar;
    while ((nextChar = readre.read()) != -1) {
      content.append((char) nextChar);
    }
    readre.close();
    return String.valueOf(content);
  }

  public static void makedir(String s) throws Exception {
    s = s.replace(" ", "");
    File f = new File(s);
    f.mkdirs();
    f.createNewFile();
  }

  public static void delete(String s) {
    s = s.replace(" ", "");
    File f = new File(s);
    f.delete();
  }

  public static String[] list2array(ArrayList<String> array) {
    String[] newf = new String[array.size()];
    for (int i = 0; i < newf.length; ++i) {
      newf[i] = array.get(i);
    }
    return newf;
  }

  public static String removelastpath(String s) {
    s = s.replace("\\", "/");
    String[] f = s.split("/");
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < f.length; ++i) {
      if (i == f.length - 1)
        continue;
      sb.append(f[i] + "/");
    }
    return sb.toString();
  }

  public static Boolean isempty(String savedir) throws IOException {
    DirectoryStream<Path> directory = Files.newDirectoryStream(Path.of(savedir));
    if (directory.iterator().hasNext()) {
      directory.close();
      return false;
    }
    directory.close();
    return true;
  }

  public static String[] subdirs(String s) {
    File f = new File(s);
    String[] dirs = f.list(new FilenameFilter() {
      @Override
      public boolean accept(File current, String name) {
        return new File(current, name).isDirectory();
      }
    });
    return dirs;
  }

  public static boolean containsarray(String s, String[] arr) {
    for (String ss : arr) {
      if (ss.equals(s))
        return true;
    }
    return false;
  }

  public static String ff =
      "https://web.archive.org/web/20010823152817/http://www.aeronautics.ru/archive/fleet/russian/1144.htm\r\n"
          + "https://web.archive.org/web/20071013132209/http://bjmb.gov.cn/en/wmod.asp\r\n"
          + "https://web.archive.org/web/20070928055736/http://www.mbda-systems.com/mbda/site/FO/scripts/siteFO_contenu.php?lang=EN&noeu_id=169\r\n"
          + "https://www.pas.rochester.edu/~emamajek/memo_star_dens.html\r\n"
          + "https://people.duke.edu/~charvey/index.html\r\n"
          + "http://stars.astro.illinois.edu/sow/sowlist.html\r\n"
          + "https://faculty.wcas.northwestern.edu/infocom/My%20Site/index.html\r\n"
          + "https://www.nasa.gov/history/alsj/\r\n"
          + "https://web.archive.org/web/20090131070033/http://chevron.com/products/sitelets/richmond/about/history.aspx\r\n"
          + "https://web.archive.org/web/20041209111217/http://www.conicyt.cl/~egoles/cultura/mercurio/index-prensa-escrita.html\r\n"
          + "https://web.archive.org/web/20180129193513/http://www.yak.ru/ENG/FIRM/HISTMOD/yak-38.php\r\n"
          + "https://uregina.ca/~gingrich/mar1298.htm\r\n"
          + "https://web.archive.org/web/20051104041256/http://home19.inet.tele.dk/airwing/ships/sovremen.htm\r\n"
          + "https://web.archive.org/web/20240701133449/https://www.forecastinternational.com/\r\n"
          + "https://web.archive.org/web/20070220202453/http://web.ukonline.co.uk/aj.cashmore/russia/cruisers/slava/index.html\r\n"
          + "https://web.archive.org/web/20130304160608/http://www.navy.mil/navydata/ships/lists/shipalpha.asp\r\n"
          + "https://web.archive.org/web/20101101112252/http://kbarsenal.ru/a192.php\r\n"
          + "https://web.archive.org/web/20131002195204/http://www.kreiserkirov.ru/zakaz800/I.htm\r\n"
          + "https://web.archive.org/web/20091212215558/http://www.milrus.com/vmf/956.shtml\r\n"
          + "https://web.archive.org/web/20131013050633/http://flot.sevastopol.info/arms/guns/ak130.htm\r\n"
          + "https://web.archive.org/web/20181010204413/http://www.rusarmy.com/pvo/pvo_vmf/su_ak_mr-184.html\r\n"
          + "https://web.archive.org/web/20210611223609/https://dfnc.ru/katalog-vooruzhenij/artilleriya-vmf/ak-130/\r\n"
          + "https://web.archive.org/web/20210122050418/https://bastion-karpenko.ru/\r\n"
          + "http://home.moravian.edu/users/phys/mejjg01/retirement%20activities/pages/geo/149-Pompeii.html\r\n"
          + "https://web.archive.org/web/20120204093137/http://home.eznet.net/~dminor/Canals.html\r\n"
          + "https://web.archive.org/web/20170125164419/http://www.nyc-architecture.com/MID/MID-TimesSquare3.htm\r\n"
          + "https://web.archive.org/web/20220124205201/https://nssd.navy.mil.bd/https://web.archive.org/web/20240613195746/https://nsdctg.navy.mil.bd/\r\n"
          + "https://web.archive.org/web/20180523083914/https://www.indiannavy.nic.in/1138\r\n"
          + "\r\n"
          + "https://web.archive.org/web/20150812061546/http://cherokeeregistry.com/index.php?option=com_content&view=article&id=217&Itemid=293\r\n"
          + "https://web.archive.org/web/20120629091519/http://www.humantouchofchemistry.com/ardaseer-cursetjee-wadia.htm\r\n"
          + "https://web.archive.org/web/20210206115417/https://francoprussianwar.com/\r\n"
          + "https://web.archive.org/web/20190123040230/http://rgsmuseum.ru/\r\n"
          + "https://www.hawaii.edu/powerkills/NAZIS.CHAP1.HTM\r\n"
          + "https://web.archive.org/web/20040122083250/http://britwar.co.uk/\r\n"
          + "https://web.archive.org/web/20010202072800/https://history.vif2.ru/https://web.archive.org/web/20210119145644/https://archive.mil.ru/archival_service/central/history.htm\r\n"
          + "\r\n";

  public static void d3() {
    String arch = "https://web.archive.org/web/";
    String[] f2 = ff.split("\r\n");
    StringBuilder sb = new StringBuilder();
    StringBuilder s2 = new StringBuilder();
    for (int i = 0; i < f2.length; ++i) {
      String m = f2[i];
      m = m.replace(arch, "");
      System.out.println(m);
      try {
        m = m.split("http")[1];
      } catch (Exception e) {
      }
      m = m.replace("://", "");
      m = m.split("/")[0];
      m = "+*" + m + "* ";
      sb.append(m);
    }
    for (String sf : f2) {
      s2.append(sf + " ");
    }
    String s3 = s2.toString().replace("www.", "");
    s3 = removeq(s3);
    String m = "nohup httrack " + s3 + " -* " + sb.toString()
        + "+*.jpg -*.wiki* --near --advanced-maxlinks=10000000000000 -s0 > s.txt &";
    System.out.println(m);

  }

  public static String removeq(String s) {
    String[] ff = s.split(" ");
    StringBuilder sb = new StringBuilder();
    for (String f3 : ff) {
      f3 = f3.replace("?", " ");
      f3 = f3.split(" ")[0];
      sb.append(f3 + " ");
    }
    String s3 = sb.toString();
    return s3;
  }

}
