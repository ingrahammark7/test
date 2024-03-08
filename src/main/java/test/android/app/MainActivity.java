package test.android.app;

import android.os.AsyncTask;
import android.os.Bundle;
import android.webkit.WebView;



public class MainActivity {// extends AppCompatActivity {

  private WebView webView;

  protected void onCreate(Bundle savedInstanceState) {

    new DownloadWebsiteTask().execute();
  }

  private class DownloadWebsiteTask extends AsyncTask<Void, Void, Boolean> {

    @Override
    protected Boolean doInBackground(Void... voids) {
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

    }


  }
}

