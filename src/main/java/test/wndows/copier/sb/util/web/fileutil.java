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
      "https://web.archive.org/web/20100422134339/http://www.zik.ru/products/ml_en.htm\r\n"
          + "https://web.archive.org/web/20130506132453/http://www.raspletin.ru/tsentr-mniire-altair-oao-gskb-almaz-antey\r\n"
          + "https://web.archive.org/web/20200831195841/https://rosim.ru/\r\n"
          + "https://web.archive.org/web/20131219000018/http://www.biplanes.de/bilderserien/bremen_09/index.php\r\n"
          + "https://web.archive.org/web/20070927045017/http://www.ajbs.fr/musee/stieglitz.php\r\n"
          + "https://web.archive.org/web/20060706120321/http://armor.yurteh.net/Tanks/Modern/roket/roket1.html\r\n"
          + "https://web.archive.org/web/20070928042154/http://www.russarms.com/land/msv/T-62/tech-tank-t-62-a.asp\r\n"
          + "https://web.archive.org/web/20030514161321/http://armoured.vif2.ru/o287.htm\r\n"
          + "https://web.archive.org/web/20080226215231/http://www.megakm.ru/Weaponry/encyclop.asp?TopicNumber=1727\r\n"
          + "https://web.archive.org/web/20180516034759/https://militaryparitet.com/nomen/russia/rocket/rocketcomplex/data/ic_nomenrussiarocketrocketcomplex/5/\r\n"
          + "https://web.archive.org/web/20150714163908/http://warfare.be/db/catid/263/linkid/2084/\r\n"
          + "https://web.archive.org/web/20050227221236/http://hs-ships.ru/e_pages.phtm?f=2&p=1\r\n"
          + "https://web.archive.org/web/20070202164833/http://aquaglide.ru/history_e.htm\r\n"
          + "https://web.archive.org/web/20110814161738/http://igor113.livejournal.com/51213.html\r\n"
          + "https://web.archive.org/web/20200217121237/http://students.uni-vologda.ac.ru/pages/pm07/evn/km.htm\r\n"
          + "https://web.archive.org/web/20230313233659/http://www.ckbspk.ru/en/about/press/\r\n"
          + "https://web.archive.org/web/20120113102538/http://www.beriev.com/eng/core_e.html\r\n"
          + "https://web.archive.org/web/20190313125015/https://www.redstar.gr/index.php?Itemid=526&catid=413&id=2156%3Abe-200-multipurpose-amphibian-aircraft&lang=en&option=com_content&view=article\r\n"
          + "https://web.archive.org/web/20070317005310/http://www.irkutseaplane.com/be200.html\r\n"
          + "https://web.archive.org/web/20080925172707/http://www.irkut.com/en/services/production/BE200/\r\n"
          + "https://web.archive.org/web/20220202064639/http://www.samoupravlenie.ru/\r\n"
          + "4https://web.archive.org/web/20160923164242/http://www.ctrl-c.liu.se/misc/ram/mbr-2m17.html\r\n"
          + "https://web.archive.org/web/20140512233028/http://vazduhoplovnetradicijesrbije.rs/index.php/istorija/276-dornije-do-j\r\n"
          + "https://web.archive.org/web/20171120065512/http://ram-home.com/ram-old/stal-2.html\r\n"
          + "https://web.archive.org/web/20120819215958/http://www.sailplanedirectory.com/PlaneDetails.cfm?PlaneID=37\r\n"
          + "https://web.archive.org/web/20100420012244/http://www.ae.illinois.edu/m-selig/ads/aircraft.html\r\n"
          + "https://web.archive.org/web/20100430002641/http://www.xcor.com/products/vehicles/lynx_suborbital.html\r\n"
          + "https://web.archive.org/web/20160303182045/http://www.rocketracingleague.com/\r\n"
          + "https://web.archive.org/web/20180314043154/https://www4.vintagesailplanes.de/\r\n"
          + "https://web.archive.org/web/20181016032601/http://www.piotrp.de/SZYBOWCE/pszdc.htm\r\n"
          + "https://web.archive.org/web/20090916142935/http://www.szdjezow.com.pl/ofirmie_eng.html\r\n"
          + "https://web.archive.org/web/20090621000722/https://www.aeroklub.wroc.pl/node/114\r\n"
          + "https://web.archive.org/web/20111003130422/http://jarek24.w.interia.pl/pw/pw2/pw2-photo-html/pw2-05.htm\r\n"
          + "https://web.archive.org/web/20040929031950/http://www.duotone.com/coldwar/abm/\r\n"
          + "https://web.archive.org/web/20121021040710/http://www.railuk.info/steam/getsteam.php?row_id=10538\r\n"
          + "https://web.archive.org/web/20150805041910/http://amhistory.si.edu/archives/d8523.htm\r\n"
          + "https://web.archive.org/web/20030210095430/https://www.auswaertiges-amt.de/www/en/laenderinfos/laender/laender_ausgabe_html?type_id=14&land_id=63\r\n"
          + "https://web.archive.org/web/20010420084329/http://www.1stof46.com/\r\n"
          + "https://web.archive.org/web/20090714020340/https://www.lzhurricane.com/\r\n"
          + "https://web.archive.org/web/20050323230638/https://bgmarrs2.tripod.com/\r\n"
          + "https://web.archive.org/web/20240225152803/http://1_14thfa.tripod.com/\r\n"
          + "https://web.archive.org/web/20011222013214/http://www.airborne-ranger.com/~brizendine/\r\n"
          + "";

  public static void d3() {
    String arch = "https://web.archive.org/web/";
    String[] f2 = ff.split("\r\n");
    StringBuilder sb = new StringBuilder();
    StringBuilder s2 = new StringBuilder();
    for (int i = 0; i < f2.length; ++i) {
      String m = f2[i];
      m = m.replace(arch, "");
      System.out.println(m);
      m = m.split("http")[1];
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
