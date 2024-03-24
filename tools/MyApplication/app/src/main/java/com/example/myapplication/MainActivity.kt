package com.example.myapplication

import android.app.DownloadManager
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.os.StrictMode
import android.os.StrictMode.ThreadPolicy
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import java.io.BufferedReader
import java.io.File
import java.io.FileInputStream
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL
import java.util.regex.Pattern


var alreadyFile = "alreadydone.txt"
var basepath = "https:/www.google.com/"
var nextfile = basepath
var pathf = File("")

class MainActivity : ComponentActivity() {
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
            pathf =
                Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
            looper()
        }
    }

    fun looper(){
        while(true) {
            var filesd = readfile(alreadyFile)
            if(filesd.contains(nextfile)) continue
            if(!nextfile.contains(basepath)) continue
            var f = sendGet(basepath)
            val listOfUrls = getHyperLinks(f)
            for (i in listOfUrls) {
            }
            break
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
    writefile(alreadyFile,name)
}

fun appendfile(name:String, content:String){
    var foo = readfile(name)
    var sb = StringBuilder()
    sb.append(foo)
    writefile(name,sb.toString())
}

fun readfile(name: String): String{
    val file = File(pathf, name)
    Log.d("ffer",file.toString())
    file.appendText("foo")
    file.createNewFile()
    return FileInputStream(file).bufferedReader().use { it.readText() }
}

fun getfullfilename(name:String): String{
    var sb = StringBuilder()
    sb.append(pathf)
    sb.append("/")
    sb.append(name)
    return sb.toString()
}

fun writefile(pp:String,name:String){
    //name is data
    //p is path
    Log.d("initialname",name)
    Log.d("pper1",pp)
    var pp1 = getfullfilename(pp)
    Log.d("pper2",pp1)
    var bar = pp1.split("//")
    var newname = pp1.split("//")[bar.size-1]
    var foo = StringBuilder()
    foo.append(pathf)
    Log.d("fooer",foo.toString())
    Log.d("nane",newname)
    val file = File(newname)
    Log.d("existfoo",newname)
    file.createNewFile()
    file.appendText(pp1+"\n")
}

fun sendGet(name: String ):String {
    val sb = StringBuilder()
    val url = URL(name)
    with(url.openConnection() as HttpURLConnection) {
        requestMethod = "GET"
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
    appendfile(alreadyFile,name+"\n")
    return sb.toString()
}