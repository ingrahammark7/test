package com.example.myapplication

import android.R.attr.action
import android.R.id
import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.os.CountDownTimer
import android.os.StrictMode
import android.os.StrictMode.ThreadPolicy
import android.view.View
import android.widget.Button
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.Text
import androidx.compose.ui.input.key.Key.Companion.Calendar
import java.io.BufferedReader
import java.net.HttpURLConnection
import java.net.URL
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Locale


class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        printDifferenceDateForHours()
        setContent {
            val policy = ThreadPolicy.Builder().permitAll().build()
            StrictMode.setThreadPolicy(policy)
            var foo = sendGet("https://www.google.com/")
            Text(foo)
            foo = sendGet("https://www.facebook.com/")
            Text(foo)
        }
    }
}


private var Int.text: String
    get() {
        return "0"
    }
    set(foo: String){

     }
private lateinit var countDownTimer: CountDownTimer

fun printDifferenceDateForHours() {

    val currentTime = java.util.Calendar.getInstance().time
    val endDateDay = "03/02/2020 21:00:00"
    val format1 = SimpleDateFormat("dd/MM/yyyy hh:mm:ss", Locale.getDefault())
    val endDate = format1.parse(endDateDay)

    val txt_timeleft = 0
    //milliseconds
    var different = endDate.time - currentTime.time
    countDownTimer = object : CountDownTimer(different, 1000) {

        override fun onTick(millisUntilFinished: Long) {
            var diff = millisUntilFinished
            val secondsInMilli: Long = 1000
            val minutesInMilli = secondsInMilli * 60
            val hoursInMilli = minutesInMilli * 60
            val daysInMilli = hoursInMilli * 24

            val elapsedDays = diff / daysInMilli
            diff %= daysInMilli

            val elapsedHours = diff / hoursInMilli
            diff %= hoursInMilli

            val elapsedMinutes = diff / minutesInMilli
            diff %= minutesInMilli

            val elapsedSeconds = diff / secondsInMilli

            txt_timeleft.text = "$elapsedDays days $elapsedHours hs $elapsedMinutes min $elapsedSeconds sec"
        }

        override fun onFinish() {
            txt_timeleft.text = "done!"
        }
    }.start()
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