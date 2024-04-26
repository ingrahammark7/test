package test.wndows.copier;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class pixer {

  public static String cok =
      "first_visit_datetime_pc=2024-03-25%2015%3A35%3A56; p_ab_id=3; p_ab_id_2=2; p_ab_d_id=1866268001; yuid_b=FYIkEHY; PHPSESSID=78437197_2clPVwjU5ierDRImm1sdsq4aDqHgwPva; privacy_policy_agreement=6; _ga_MZ1NL4PHH0=GS1.1.1711350424.1.1.1711350468.0.0.0; c_type=23; privacy_policy_notification=0; a_type=0; b_type=1; _gcl_au=1.1.827437291.1711376157; login_ever=yes; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=78437197=1^9=p_ab_id=3=1^10=p_ab_id_2=2=1^11=lang=en=1; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; __utmz=235335808.1713821263.12.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _gid=GA1.2.857461378.1713954108; _ga_75BBYNYN9J=deleted; cf_clearance=4Z4d7huC7qnlzO8WkbBPiMTMyfGA_AQ9gaYORRnnZqM-1714100011-1.0.1.1-xEJsX6P7KWmNATxzUUYXQtsB8_epYM1rTlOFA8IqvmQoUkWqNjS_mXle5VrSK4lgHf.CvZ8KYEWGeLpAdzq34Q; __cf_bm=9OHGDK4fUZeyOS3ho55jwn1HcjkYkRuNqc8MwbTEk2A-1714128811-1.0.1.1-d0DT0pnUzDHUfNE0AFclVZJw0iX6moiOFyy5cGFJ0IAmLYtPH0.RgTd6Wh2NTYZ4n2IGKAGR_nrmlUO2dHrG57zm8ED7sgqHxxOtzzxSB4c; __utma=235335808.474191161.1711348576.1714113425.1714128812.17; _ga=GA1.1.487725691.1711349186; __utmc=235335808; __utmt=1; __utmb=235335808.3.10.1714128812; _ga_75BBYNYN9J=GS1.1.1714128819.4.1.1714129665.0.0.0";
  public static String c2 = "Accept:\r\n"
      + "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\n"
      + "Accept-Encoding:\r\n" + "gzip, deflate, br, zstd\r\n" + "Accept-Language:\r\n"
      + "en-US,en;q=0.9,zu;q=0.8,vi;q=0.7,fa;q=0.6\r\n" + "Cache-Control:\r\n" + "max-age=0\r\n"
      + "Cookie:\r\n"
      + "first_visit_datetime_pc=2024-03-25%2015%3A35%3A56; p_ab_id=3; p_ab_id_2=2; p_ab_d_id=1866268001; yuid_b=FYIkEHY; PHPSESSID=78437197_2clPVwjU5ierDRImm1sdsq4aDqHgwPva; privacy_policy_agreement=6; _ga_MZ1NL4PHH0=GS1.1.1711350424.1.1.1711350468.0.0.0; c_type=23; privacy_policy_notification=0; a_type=0; b_type=1; _gcl_au=1.1.827437291.1711376157; login_ever=yes; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=78437197=1^9=p_ab_id=3=1^10=p_ab_id_2=2=1^11=lang=en=1; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; __utmz=235335808.1713821263.12.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _gid=GA1.2.857461378.1713954108; _ga_75BBYNYN9J=deleted; cf_clearance=4Z4d7huC7qnlzO8WkbBPiMTMyfGA_AQ9gaYORRnnZqM-1714100011-1.0.1.1-xEJsX6P7KWmNATxzUUYXQtsB8_epYM1rTlOFA8IqvmQoUkWqNjS_mXle5VrSK4lgHf.CvZ8KYEWGeLpAdzq34Q; __cf_bm=9OHGDK4fUZeyOS3ho55jwn1HcjkYkRuNqc8MwbTEk2A-1714128811-1.0.1.1-d0DT0pnUzDHUfNE0AFclVZJw0iX6moiOFyy5cGFJ0IAmLYtPH0.RgTd6Wh2NTYZ4n2IGKAGR_nrmlUO2dHrG57zm8ED7sgqHxxOtzzxSB4c; __utma=235335808.474191161.1711348576.1714113425.1714128812.17; _ga=GA1.1.487725691.1711349186; __utmc=235335808; __utmt=1; __utmb=235335808.3.10.1714128812; _ga_75BBYNYN9J=GS1.1.1714128819.4.1.1714129665.0.0.0\r\n"
      + "Dnt:\r\n" + "1\r\n" + "Priority:\r\n" + "u=0, i\r\n" + "Sec-Ch-Ua:\r\n"
      + "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"\r\n"
      + "Sec-Ch-Ua-Mobile:\r\n" + "?0\r\n" + "Sec-Ch-Ua-Platform:\r\n" + "\"Windows\"\r\n"
      + "Sec-Fetch-Dest:\r\n" + "document\r\n" + "Sec-Fetch-Mode:\r\n" + "navigate\r\n"
      + "Sec-Fetch-Site:\r\n" + "same-origin\r\n" + "Sec-Fetch-User:\r\n" + "?1\r\n"
      + "Upgrade-Insecure-Requests:\r\n" + "1\r\n" + "User-Agent:\r\n"
      + "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36";

  public static void pixef() throws Exception {
    URL url = new URL("https://www.pixiv.net/");
    HttpURLConnection con = (HttpURLConnection) url.openConnection();
    con.setRequestMethod("GET");
    con = conner(con);
    BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
    String inputLine;
    StringBuffer content = new StringBuffer();
    while ((inputLine = in.readLine()) != null) {
      content.append(inputLine);
    }
    in.close();
    System.out.println(in.toString());
  }

  public static HttpURLConnection conner(HttpURLConnection con) throws Exception {
    String[] ff = c2.split(":\r\n");
    String key = "";
    String value = "";
    for (int i = 0; i < ff.length; ++i) {
      if (i == 0) {
        key = ff[0];
        continue;
      }
      if (i == ff.length - 1) {
        value = ff[i];
        con.setRequestProperty(key, value);
        return con;
      }
      String gg = ff[i];
      String[] fo = gg.split("\r\n");
      key = fo[1];
      value = fo[0];
      value = value.replace("\r\n", "");
      System.out.println("key " + key);
      System.out.println("val " + value);
      con.addRequestProperty(key, value);
    }
    return con;

  }

}
