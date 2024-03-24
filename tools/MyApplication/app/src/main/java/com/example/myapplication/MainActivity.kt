package com.example.myapplication

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.os.StrictMode
import android.os.StrictMode.ThreadPolicy
import android.util.Log
import android.view.View
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import java.io.BufferedReader
import java.net.HttpURLConnection
import java.net.URL
import java.util.regex.Pattern


class MainActivity : ComponentActivity() {
    var alreadyFile = "alreadydone.txt"
    val urlPattern: Pattern = Pattern.compile(
        "(?:^|[\\W])((ht|f)tp(s?):\\/\\/|www\\.)"
                + "(([\\w\\-]+\\.){1,}?([\\w\\-.~]+\\/?)*"
                + "[\\p{Alnum}.,%_=?&#\\-+()\\[\\]\\*$~@!:/{};']*)",
        Pattern.CASE_INSENSITIVE or Pattern.MULTILINE or Pattern.DOTALL)
    fun alreadyDone() {
        var alreadyDone = mutableListOf<String>("foo","bar")
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        val policy = ThreadPolicy.Builder().permitAll().build()
        StrictMode.setThreadPolicy(policy)
        super.onCreate(savedInstanceState)

        setContent {
            var f = sendGet("https://www.google.com/")
            val listOfUrls = getHyperLinks(f)
            val pathf = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
            Log.d("filepath",pathf.absolutePath)
            //storage/emulated/0/Downloads
            for(i in listOfUrls){
        }
        }
    }

    fun getHyperLinks(s: String): List<String> {
        val urlList = mutableListOf<String>()
        val urlMatcher = urlPattern.matcher(s)
        var matchStart: Int
        var matchEnd: Int
        while (urlMatcher.find()) {
            matchStart = urlMatcher.start(1)
            matchEnd = urlMatcher.end()
            val url = s.substring(matchStart, matchEnd)
            urlList.add(url)
        }
        return urlList
    }
}

fun alreadyVisit(name: String){

}

fun appendfile(name:String, content:String){
    var foo = readfile(name)
    var sb = StringBuilder()
    sb.append(foo)
    writefile(name,sb.toString())
}

fun readfile(name: String): String{
    return ""
}

fun writefile(name:String, content:String){

}

fun sendGet(name: String ):String {
    val sb = StringBuilder()
    val url = URL(name)
    with(url.openConnection() as HttpURLConnection) {
        requestMethod = "GET"  // optional default is GET

        println("\nSent 'GET' request to URL : $url; Response Code : $responseCode")

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            inputStream.bufferedReader().use {
                it.lines().forEach { line ->
                    println(line)
                    sb.append(line)
                }
            }
        } else {
            val reader: BufferedReader = inputStream.bufferedReader()
            var line: String? = reader.readLine()
            while (line != null) {
                System.out.println(line)
                line = reader.readLine()
            }
            reader.close()

        }
    }
    System.gc()
    return sb.toString()
}