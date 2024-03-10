package test.android.app;

import org.apache.http.HttpResponse;
import org.apache.http.StatusLine;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.HttpClientBuilder;



public class MainActivity {// extends AppCompatActivity {

  public static void main(String[] args) {
    DownloadWebsiteTask();
  }


  public static void DownloadWebsiteTask() {

    try {
      HttpClient httpClient = HttpClientBuilder.create().build();
      HttpResponse response = httpClient.execute(new HttpGet("https://www.example.com"));
      StatusLine statusLine = response.getStatusLine();
      statusLine.toString();
      System.out.println("here");
      System.out.println(statusLine.toString());
      return;
    } catch (Exception e) {
      e.printStackTrace();
      return;
    }
  }



}

