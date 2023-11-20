package test.copier;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import org.apache.http.client.utils.URIBuilder;

public class Copier {

  public static String p1 = "D:\\2023\\foo\\";
  public static String p2 = "C:\\Users\\a\\Downloads\\";
  public static String p3 = "https://vk.com/wall-200782618?offset=";
  public static ArrayList<String> allfiles = new ArrayList<String>();
  public static int increment = 20;
  public static int pages = 430;
  public static int offset = increment * pages;
  public static String p4 = p3 + offset;


  public static void dof() {
    try {
      URIBuilder builder = new URIBuilder();
      builder.setScheme("http");
      builder.setHost("vk.com");
      builder.setPath("/wall-200782618");
      builder.addParameter("offset", String.valueOf(offset));
      URL url = builder.build().toURL();
      HttpURLConnection con = (HttpURLConnection) url.openConnection();
      con.setRequestMethod("GET");
      Map<String, String> parameters = new HashMap<String, String>();
      con.setDoOutput(true);
      DataOutputStream out = new DataOutputStream(con.getOutputStream());
      out.writeBytes(getParamsString(parameters));
      out.flush();
      out.close();

      con.setConnectTimeout(5000);
      con.setReadTimeout(5000);
      con.disconnect();
      con = (HttpURLConnection) url.openConnection();
      con.setInstanceFollowRedirects(false);
      int status = con.getResponseCode();
      if (status == HttpURLConnection.HTTP_MOVED_TEMP
          || status == HttpURLConnection.HTTP_MOVED_PERM) {
        URL newUrl = url;
        con = (HttpURLConnection) newUrl.openConnection();
      }
      System.out.println("url " + url.toString());
      BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
      String inputLine;
      StringBuffer content = new StringBuffer();
      while ((inputLine = in.readLine()) != null) {
        content.append(inputLine);
      }
      in.close();
      con.disconnect();
      int status1 = con.getResponseCode();

      Reader streamReader = null;

      if (status1 > 299) {
        streamReader = new InputStreamReader(con.getInputStream());
      } else {
        streamReader = new InputStreamReader(con.getInputStream());
      }
      System.out.println(streamReader.toString());
      StringBuilder sb = new StringBuilder();
      sb.append(con.getResponseCode()).append(" ").append(con.getResponseMessage()).append("\n");
      Set<Entry<String, List<String>>> f = con.getHeaderFields().entrySet();
      Iterator<Entry<String, List<String>>> en = f.iterator();
      while (en.hasNext()) {
        Entry<String, List<String>> e = en.next();
        String r = e.getKey();
        System.out.println(r);
        List<String> vs = e.getValue();
        Iterator<String> i = vs.iterator();
        while (i.hasNext()) {
          String res = i.next();
          System.out.println(res);
        }
      }
    } catch (Exception e) {
      e.printStackTrace();
      System.exit(0);
    }
  }

  public static String getParamsString(Map<String, String> params)
      throws UnsupportedEncodingException {
    StringBuilder result = new StringBuilder();

    for (Map.Entry<String, String> entry : params.entrySet()) {
      result.append(URLEncoder.encode(entry.getKey(), "UTF-8"));
      result.append("=");
      result.append(URLEncoder.encode(entry.getValue(), "UTF-8"));
      result.append("&");
    }

    String resultString = result.toString();
    return resultString.length() > 0 ? resultString.substring(0, resultString.length() - 1)
        : resultString;
  }

}
