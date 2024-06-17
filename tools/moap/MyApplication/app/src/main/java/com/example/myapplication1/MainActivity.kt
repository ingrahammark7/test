package com.example.myapplication1

import android.content.Intent
import android.os.Bundle
import android.os.Environment
import android.os.StrictMode
import android.os.StrictMode.ThreadPolicy
import android.provider.Settings
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.FileInputStream
import java.net.HttpURLConnection
import java.net.URL
import java.util.regex.Pattern


var alreadyFile = "alreadydone.txt"
var basepath = "https://www.facebook.com/"
var nextfile = basepath
var pathf = File("")
var acceptablepaths = ArrayList<String>()

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
        acceptablepaths.add("cdn")
        acceptablepaths.add("facebook")
        val policy = ThreadPolicy.Builder().permitAll().build()
        StrictMode.setThreadPolicy(policy)
        super.onCreate(savedInstanceState)
        setContent {
            if (!Environment.isExternalStorageManager()) {
                val intent: Intent = Intent(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION)
                startActivity(intent)
            }
            pathf =
                Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
            looper()
        }
    }

    fun checkf(name:String): Boolean{
        var filesd = readfile(alreadyFile)
        var sb = StringBuilder()
        sb.append(name)
        sb.append("!")
        if(filesd.contains(sb.toString())) return true
        return false
    }

    fun looper(){
        while(true) {
            filer(nextfile)
        }
    }

    public fun thread(start: Boolean=true, isDaemon: Boolean=false, contextClassLoader: ClassLoader? = null, name: String? = null, priority: Int = -1): Thread{
        Thread{
            thread()
        }.start()
        Thread{
            looper()
        }.start()
        System.gc()
        Log.d("her4","f")
        return Thread(Runnable{
           looper()
        })

    }

    fun checkpath(nexter: String): Boolean{
        for(i in acceptablepaths){
            if(nexter.contains(i)) return true
        }
        return false
    }

    fun filer(nexter:String){
        if(checkf(nexter)) return
        if(!checkpath(nexter)) return
        Log.d("foo", "filer: ")
        var f = sendGet(nexter)
        val listOfUrls = getHyperLinks(f)
        for (i in listOfUrls) {
            filer(i)
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

fun appendfile(name:String, content:String){
    var foo = readfile(name)
    var sb = StringBuilder()
    sb.append(foo)
    var sb1 = StringBuilder()
    sb1.append(pathf)
    sb1.append("/")
    sb1.append(name)
    var filef = File(sb1.toString())
    filef.appendText(content)
}

fun readfile(name: String): String{
    val file = File(pathf, name)
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

fun writefile(pp:String,name:ByteArrayOutputStream) {
    var pp1 = getfullfilename(pp)
    var file = File(pp1)
    var tempst = file.toString().replace(":", "")
    var temper = File(tempst)
    tempst = tempst.plus("/file")
    var file2 = File(tempst)
    temper.mkdirs()
    Log.d("made", temper.toString())
    file2.createNewFile()
    file2.appendBytes(name.toByteArray())
}

fun sendGet(name: String ):String {
    var sb = ByteArrayOutputStream()
    val url = URL(name)
    with(url.openConnection() as HttpURLConnection) {
        requestMethod = "GET"
        println("\nSent 'GET' request to URL : $url; Response Code : $responseCode")
        try {
            inputStream.use {
                it.copyTo(sb)
            }
        }catch(e: Exception){
            println("rror " + sb.toString())
        }
        //writefile(name,sb)
    }
    System.gc()
    //appendfile(alreadyFile,name+"!\n")
    return sb.toString()
}
