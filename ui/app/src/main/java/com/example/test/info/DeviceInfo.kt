package com.example.test.info

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.test.Menu
import com.example.test.WelcomeCard
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog

class DeviceInfo : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            DeviceInfoScreen(
                deviceName = intent.getStringExtra("deviceName") ?: "Unknown Device",
                onBack = { finish() }
            )
        }
    }
}


@Composable
fun DeviceInfoScreen(deviceName: String, onBack: () -> Unit) {
    val context = LocalContext.current

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        // Header
        Text(
            text = "Device Page: $deviceName",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(bottom = 16.dp)
        )

        // Device Information
        Text(
            text = "IP/Domain Name: 192.168.1.1",
            style = MaterialTheme.typography.bodyLarge,
            modifier = Modifier.padding(bottom = 8.dp)
        )
        Text(
            text = "MAC Address: 00:1A:2B:3C:4D:5E",
            style = MaterialTheme.typography.bodyLarge,
            modifier = Modifier.padding(bottom = 8.dp)
        )
        Text(
            text = "Port: 8080",
            style = MaterialTheme.typography.bodyLarge,
            modifier = Modifier.padding(bottom = 16.dp)
        )

        // Buttons Column
        Column(
            modifier = Modifier.fillMaxWidth(),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            // Whitelist Button
            Button(
                onClick = {
                    //val intent = Intent(context, WhitelistActivity::class.java)
                    //context.startActivity(intent)
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Whitelist")
            }

            // Blacklist Button
            Button(
                onClick = {
                    //val intent = Intent(context, BlacklistActivity::class.java)
                    //context.startActivity(intent)
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Blacklist")
            }

            // Quarantine Button
            Button(
                onClick = {
                    //val intent = Intent(context, QuarantineActivity::class.java)
                    //context.startActivity(intent)
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Quarantine")
            }
        }

        // Back Button
        Spacer(modifier = Modifier.weight(1f))
        Button(
            onClick = onBack,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Back")
        }
    }
}
