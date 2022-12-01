package com.example.proyectofinaldespliegue

import android.annotation.SuppressLint
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.Request
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import org.json.JSONObject

class MainActivity : AppCompatActivity(), SensorEventListener {

    private lateinit var sensorManager: SensorManager
    private var mAccelerometer : Sensor ?= null
    private var resume = false
    private lateinit var btnPrediction:Button
    private lateinit var textPrediction:TextView


    @SuppressLint("MissingInflatedId")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        sensorManager = getSystemService(SENSOR_SERVICE) as SensorManager

        mAccelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)

        btnPrediction = findViewById(R.id.start)
        textPrediction = findViewById(R.id.textViewPrediction)

        apiHealth()
    }

    @SuppressLint("SetTextI18n")
    override fun onSensorChanged(event: SensorEvent?) {

        if (event != null && resume) {
            if (event.sensor.type == Sensor.TYPE_ACCELEROMETER) {
                findViewById<TextView>(R.id.sensor_value).text =
                    "Axis X: " + event.values[0].toString() +
                            "\nAxis Y: " + event.values[1].toString() + "\nAxis Z: " + event.values[2].toString()
                val url = "http://192.168.1.1:8080/exercises/predict"
                val queue = Volley.newRequestQueue(this)

                val jsonObject = JSONObject()
                jsonObject.put("axis_x", event.values[0])
                jsonObject.put("axis_y", event.values[1])
                jsonObject.put("axis_z", event.values[2])

                val request = JsonObjectRequest(
                    Request.Method.POST, url, jsonObject, { response ->
                        Log.d("API POST SUCCESS", response.toString())
                        textPrediction.setText(response.toString())
                    },
                    { error ->
                        Log.d("API POST ERROR", error.message.toString())
                    }
                )

                queue.add(request)
            }
        }
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
        return
    }

    override fun onDestroy() {
        sensorManager.unregisterListener(this  )
        super.onDestroy()
    }

    override fun onResume() {
        super.onResume()
        sensorManager.registerListener(this, mAccelerometer, SensorManager.SENSOR_DELAY_NORMAL)
    }

    override fun onPause() {
        super.onPause()
        sensorManager.unregisterListener(this)
    }

    fun resumeReading(view: View) {
        this.resume = true
    }

    fun pauseReading(view: View) {
        this.resume = false
    }

    fun apiHealth() {
        val result = findViewById<TextView>(R.id.textView)
        val url = "http://192.168.1.1:8080/exercises/health"
        val queue = Volley.newRequestQueue(this)

        val request = StringRequest(
            Request.Method.GET, url, {
                    response ->
                try {
                    Log.d("API RESPONSE", response.toString())
                    result.setTextColor(this.getColor(R.color.green))
                    result.text = response.toString()
                    btnPrediction.isEnabled = true
                } catch (e: Exception) {
                    Log.d("api error", e.message.toString())
                    result.setTextColor(this.getColor(R.color.red))
                    result.text = "No connection to server"
                }
            },
            {
                    error ->
                Log.d("api error", error.message.toString())
                result.text = "No connection to server"
                result.setTextColor(this.getColor(R.color.red))
            }
        )

        queue.add(request)
    }
}