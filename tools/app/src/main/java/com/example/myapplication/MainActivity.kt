package com.example.myapplication

import android.os.Bundle
import android.util.Log.*
import androidx.activity.ComponentActivity


class MainActivity : ComponentActivity(){
    private var s: String = "foo"
    override fun onCreate(savedInstanceState: Bundle?){
        super.onCreate(savedInstanceState)
        d(s,s)
        }
   }




