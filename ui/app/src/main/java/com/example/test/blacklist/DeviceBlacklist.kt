package com.example.test.whitelist

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
import androidx.compose.material.icons.filled.Check
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

class DeviceBlacklist : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            BlacklistScreen { selectedDevices -> println("selectedDevices: $selectedDevices") }
        }
    }
}

@Composable
fun BlacklistScreen(onWhitelistClick: (List<String>) -> Unit) {
    // Sample list of devices
    val devices = remember { mutableStateOf(listOf("Device 1", "Device 2", "Device 3", "Device 4")) }
    val selectedDevices = remember { mutableStateOf(setOf<String>()) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        // Header
        Text(
            text = "Device Blacklist",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(bottom = 16.dp)
        )

        // List of Devices
        LazyColumn(
            modifier = Modifier.weight(1f)
        ) {
            items(devices.value) { device ->
                val isSelected = selectedDevices.value.contains(device)
                DeviceBlacklistItem(
                    device = device,
                    isSelected = isSelected,
                    onToggleSelection = {
                        if (isSelected) {
                            selectedDevices.value = selectedDevices.value - device
                        } else {
                            selectedDevices.value = selectedDevices.value + device
                        }
                    }
                )
            }
        }

        // Whitelist Button
        Button(
            onClick = {
                // Pass the selected devices to the callback
                onWhitelistClick(selectedDevices.value.toList())
                // Clear the selection
                selectedDevices.value = emptySet()
            },
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 16.dp),
            enabled = selectedDevices.value.isNotEmpty()
        ) {
            Text("Whitelistlist")
        }
    }
}

@Composable
fun DeviceBlacklistItem(device: String, isSelected: Boolean, onToggleSelection: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp)
            .clickable { onToggleSelection() },
        colors = CardDefaults.cardColors(
            containerColor = if (isSelected) MaterialTheme.colorScheme.primaryContainer
            else MaterialTheme.colorScheme.surface
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            // Device Name
            Text(
                text = device,
                style = MaterialTheme.typography.bodyLarge
            )

            // Selection Indicator
            if (isSelected) {
                Icon(
                    imageVector = Icons.Default.Check,
                    contentDescription = "Selected",
                    tint = MaterialTheme.colorScheme.primary
                )
            }
        }
    }
}

