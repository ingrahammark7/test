package test.android.app;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.webkit.CookieManager;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MainActivity extends AppCompatActivity {

  private WebView webView;
  private static final String USER_LOGIN_COOKIE = "user_login_cookie=your_cookie_value_here";
  private static final int MIN_THREADS = 1;
  private static final int MAX_THREADS = 10;
  private ExecutorService executorService;
  private Timer timer;

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);

    webView = findViewById(R.id.webView);
    webView.setWebViewClient(new WebViewClient() {
      @Override
      public void onPageFinished(WebView view, String url) {
        webView.evaluateJavascript("window.scrollTo(0, document.body.scrollHeight)", null);
      }
    });

    // Enable JavaScript (required for many websites)
    WebSettings webSettings = webView.getSettings();
    webSettings.setJavaScriptEnabled(true);

    // Enable cookie acceptance
    CookieManager cookieManager = CookieManager.getInstance();
    cookieManager.setAcceptCookie(true);

    // Set user login cookie
    cookieManager.setCookie("https://example.com", USER_LOGIN_COOKIE);

    // Initialize thread pool with minimum threads
    executorService = Executors.newFixedThreadPool(MIN_THREADS);

    // Start timer for dynamic thread adjustment
    timer = new Timer();
    timer.scheduleAtFixedRate(new ThreadAdjustmentTask(), 0, 60 * 1000); // Adjust threads every
                                                                         // minute

    // Start crawling task
    new WebsiteCrawler().execute();
  }

  @Override
  protected void onDestroy() {
    super.onDestroy();
    // Shutdown thread pool and stop timer
    executorService.shutdown();
    timer.cancel();
  }

  private class ThreadAdjustmentTask extends TimerTask {
    @Override
    public void run() {
      // Measure crawling speed and network bandwidth
      // Adjust thread count based on measured metrics
      int optimalThreadCount = calculateOptimalThreadCount();
      adjustThreadCount(optimalThreadCount);
    }
  }

  private int calculateOptimalThreadCount() {
    // Placeholder for calculating optimal thread count based on crawling speed and network
    // bandwidth
    // For demonstration purposes, returning a constant value
    return 5;
  }

  private void adjustThreadCount(int count) {
    if (count < MIN_THREADS) {
      count = MIN_THREADS;
    } else if (count > MAX_THREADS) {
      count = MAX_THREADS;
    }
    executorService.shutdown();
    executorService = Executors.newFixedThreadPool(count);
  }

  private class WebsiteCrawler extends AsyncTask<Void, Void, Boolean> {
    @Override
    protected Boolean doInBackground(Void... voids) {
      HashSet<String> visitedUrls = new HashSet<>();
      try {
        webView.loadUrl("https://example.com");
        return true;
      } catch (Exception e) {
        e.printStackTrace();
        return false;
      }
    }

    @Override
    protected void onPostExecute(Boolean result) {
      super.onPostExecute(result);
      if (result) {
        Toast.makeText(MainActivity.this, "Website download started", Toast.LENGTH_SHORT).show();
        // Start infinite scrolling after a delay
        webView.postDelayed(() -> {
          new InfiniteScroller().simulateInfiniteScroll();
        }, 5000);
      } else {
        Toast.makeText(MainActivity.this, "Failed to load website", Toast.LENGTH_SHORT).show();
      }
    }
  }

  private class InfiniteScroller {
    public void simulateInfiniteScroll() {
      // Simulate scrolling to the bottom of the page multiple times
      for (int i = 0; i < 10; i++) {
        webView.postDelayed(() -> {
          webView.evaluateJavascript("window.scrollTo(0, document.body.scrollHeight)", null);
        }, i * 2000);
      }
      // After all scrolling is done, wait for additional time before extracting content
      webView.postDelayed(() -> {
        String htmlContent = new HtmlExtractor().getHtmlContent(webView);
        if (htmlContent != null) {
          List<String> imageUrls = new ImageExtractor().getImageUrls(htmlContent);
          new ContentSaver().saveHtmlContent(webView.getUrl(), htmlContent);
          new ContentSaver().saveImageUrls(webView.getUrl(), imageUrls);
        } else {
          Toast.makeText(MainActivity.this, "Failed to download website", Toast.LENGTH_SHORT)
              .show();
        }
      }, 20000);
    }
  }

  private class HtmlExtractor {
    public String getHtmlContent(WebView webView) {
      final StringBuilder htmlContent = new StringBuilder();
      webView.evaluateJavascript(
          "(function() { return document.getElementsByTagName('html')[0].innerHTML; })();",
          value -> {
            if (!value.isEmpty() && !"null".equals(value)) {
              htmlContent.append(value);
            }
          });
      return htmlContent.toString();
    }
  }

  private class ImageExtractor {
    public List<String> getImageUrls(String htmlContent) {
      List<String> imageUrls = new ArrayList<>();
      Document document = Jsoup.parse(htmlContent);
      Elements imgElements = document.getElementsByTag("img");
      for (Element imgElement : imgElements) {
        String imageUrl = imgElement.absUrl("src");
        if (!imageUrl.isEmpty()) {
          imageUrls.add(imageUrl);
        }
      }
      return imageUrls;
    }
  }

  private class ContentSaver {

    public void saveHtmlContent(String url, String htmlContent) {
      try {
        String fileName = generateFileName(url, "html");
        File outputFile = new File(Environment.getExternalStorageDirectory(), fileName);
        FileWriter writer = new FileWriter(outputFile);
        writer.write(htmlContent);
        writer.close();
        Toast.makeText(MainActivity.this, "Website downloaded successfully", Toast.LENGTH_SHORT)
            .show();
      } catch (IOException e) {
        e.printStackTrace();
        Toast.makeText(MainActivity.this, "Failed to save website", Toast.LENGTH_SHORT).show();
      }
    }

    public void saveImageUrls(String url, List<String> imageUrls) {
      for (String imageUrl : imageUrls) {
        try {
          String fileName = generateFileName(imageUrl, "jpg");
          File outputFile = new File(Environment.getExternalStorageDirectory(), fileName);
          // Download the image and save it to outputFile
        } catch (IOException e) {
          e.printStackTrace();
          Toast.makeText(MainActivity.this, "Failed to save image", Toast.LENGTH_SHORT).show();
        }
      }
}

private String generateFileName(String url, String extension) {
            String fileName = url.substring(url.lastIndexOf("/") + 1);
            fileName = fileName.isEmpty



import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;


public class MainActivity extends AppCompatActivity {

  private WebView webView;

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);

    webView = findViewById(R.id.webView);
    webView.setWebViewClient(new WebViewClient() {
      @Override
      public void onPageFinished(WebView view, String url) {
        webView.evaluateJavascript("window.scrollTo(0, document.body.scrollHeight)", null);
      }
    });

    new DownloadWebsiteTask().execute();
  }

  private class DownloadWebsiteTask extends AsyncTask<Void, Void, Boolean> {

    @Override
    protected Boolean doInBackground(Void... voids) {
      HashSet<String> visitedUrls = new HashSet<>();
      try {
        webView.loadUrl("https://example.com");
        return true;
      } catch (Exception e) {
        e.printStackTrace();
        return false;
      }
    }

    @Override
    protected void onPostExecute(Boolean result) {
      super.onPostExecute(result);
      if (result) {
        Toast.makeText(MainActivity.this, "Website download started", Toast.LENGTH_SHORT).show();
        webView.postDelayed(() -> {
          simulateInfiniteScroll();
        }, 5000);
      } else {
        Toast.makeText(MainActivity.this, "Failed to load website", Toast.LENGTH_SHORT).show();
      }
    }

    private void simulateInfiniteScroll() {
      for (int i = 0; i < 10; i++) {
        webView.postDelayed(() -> {
          webView.evaluateJavascript("window.scrollTo(0, document.body.scrollHeight)", null);
        }, i * 2000);
      }
      webView.postDelayed(() -> {
        String htmlContent = getHtmlContent(webView);
        if (htmlContent != null) {
          List<String> imageUrls = getImageUrls(htmlContent);
          saveHtmlContent(htmlContent);
          saveImageUrls(imageUrls);
        } else {
          Toast.makeText(MainActivity.this, "Failed to download website", Toast.LENGTH_SHORT)
              .show();
        }
      }, 20000);
    }

    private String getHtmlContent(WebView webView) {
      final StringBuilder htmlContent = new StringBuilder();
      webView.evaluateJavascript(
          "(function() { return document.getElementsByTagName('html')[0].innerHTML; })();",
          value -> {
            if (!value.isEmpty() && !"null".equals(value)) {
              htmlContent.append(value);
            }
          });
      return htmlContent.toString();
    }

    private List<String> getImageUrls(String htmlContent) {
      List<String> imageUrls = new ArrayList<>();
      Document document = Jsoup.parse(htmlContent);
      Elements imgElements = document.getElementsByTag("img");
      for (Element imgElement : imgElements) {
        String imageUrl = imgElement.absUrl("src");
        if (!imageUrl.isEmpty()) {
          imageUrls.add(imageUrl);
        }
      }
      return imageUrls;
    }

    private void saveHtmlContent(String htmlContent) {
      try {
        File outputFile =
            new File(Environment.getExternalStorageDirectory(), "downloaded_website.html");
        FileWriter writer = new FileWriter(outputFile);
        writer.write(htmlContent);
        writer.close();
        Toast.makeText(MainActivity.this, "Website downloaded successfully", Toast.LENGTH_SHORT)
            .show();
      } catch (IOException e) {
        e.printStackTrace();
        Toast.makeText(MainActivity.this, "Failed to save website", Toast.LENGTH_SHORT).show();
      }
    }

    private void saveImageUrls(List<String> imageUrls) {
      for (String imageUrl : imageUrls) {
        Log.d("Image URL", imageUrl);
      }
      // You can save the image URLs to a file or database here
    }
  }
}

