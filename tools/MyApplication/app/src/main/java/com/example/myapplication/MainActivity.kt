package com.example.myapplication

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.os.Build
import android.os.Bundle
import android.os.StrictMode
import android.os.StrictMode.ThreadPolicy
import android.view.View
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import java.io.BufferedReader
import java.net.HttpURLConnection
import java.net.URL


class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        val policy = ThreadPolicy.Builder().permitAll().build()
        StrictMode.setThreadPolicy(policy)
        super.onCreate(savedInstanceState)
        setContentView(MyView (this));
    }


}


class MyView(context: Context?) : View(context) {
    var paint: Paint? = null

    init {
        paint = Paint()
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val x = width
        val y = height
        val radius: Int
        radius = 100
        paint!!.style = Paint.Style.FILL
        paint!!.color = Color.WHITE
        canvas.drawPaint(paint!!)
        // Use Color.parseColor to define HTML colors
        paint!!.color = Color.parseColor("#CD5C5C")
        canvas.drawCircle((x / 2).toFloat(), (y / 2).toFloat(), radius.toFloat(), paint!!)
    }
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