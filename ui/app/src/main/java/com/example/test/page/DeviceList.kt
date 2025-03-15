package com.example.test.page

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
import com.example.test.info.DeviceInfo

class DeviceList : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            DeviceListScreen()
        }
    }
}

@Composable
fun DeviceListScreen() {
    var devices by remember { mutableStateOf<List<String>>(emptyList()) }
    var selectedDevice by remember { mutableStateOf<String?>(null) }
    var showAddDialog by remember { mutableStateOf(false) }
    val context = LocalContext.current

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        // Header
        Text(
            text = "Device List",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(bottom = 16.dp)
        )

        // List of Devices with Background
        Card(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth(),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.surfaceVariant
            )
        ) {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(8.dp)
            ) {
                items(devices) { device ->
                    val isSelected = device == selectedDevice
                    DeviceItem(
                        device = device,
                        isSelected = isSelected,
                        onClick = { selectedDevice = device }

                    )
                }
            }
        }

        // Add and Remove Buttons
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            // Add Button
            Button(
                onClick = { showAddDialog = true },
                modifier = Modifier.weight(1f).padding(end = 8.dp)
            ) {
                Icon(Icons.Default.Add, contentDescription = "Add")
                Text("Add")
            }

            // Remove Button
            Button(
                onClick = {
                    if (selectedDevice != null) {
                        devices = devices.filter { it != selectedDevice }
                        selectedDevice = null
                    }
                },
                modifier = Modifier.weight(1f).padding(start = 8.dp),
                enabled = selectedDevice != null
            ) {
                Icon(Icons.Default.Delete, contentDescription = "Remove")
                Text("Remove")
            }
        }
    }

    // Add Device Dialog
    if (showAddDialog) {
        AddDeviceDialog(
            onDismiss = { showAddDialog = false },
            onAddDevice = { ip ->
                if (ip.isNotBlank()) {
                    devices = devices + ip
                }
            }
        )
    }
}

@Composable
fun DeviceItem(device: String, isSelected: Boolean, onClick: () -> Unit) {
    val context = LocalContext.current

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp)
            .clickable { onClick() },
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

            // Info Button
            Button(
                onClick = {
                    // Navigate to DeviceInfo page
                    val intent = Intent(context, DeviceInfo::class.java)
                    context.startActivity(intent)
                },
                modifier = Modifier.wrapContentWidth()
            ) {
                Text("Info")
            }

            Button(
                onClick = {}
            ) {
                Text("Quarantine")
            }
        }
    }
}

@Composable
fun AddDeviceDialog(onDismiss: () -> Unit, onAddDevice: (String) -> Unit) {
    var ipAddress by remember { mutableStateOf("") }
    var isError by remember { mutableStateOf(false) }

    Dialog(onDismissRequest = onDismiss) {
        Card(
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(16.dp)
            ) {
                Text(
                    text = "Add Device",
                    style = MaterialTheme.typography.headlineSmall,
                    modifier = Modifier.padding(bottom = 16.dp)
                )

                // IP Address Input
                TextField(
                    value = ipAddress,
                    onValueChange = { newText ->
                        if (newText.matches(Regex("^([0-9]{1,3}\\.){0,3}[0-9]{0,3}$"))) {
                            ipAddress = newText
                            isError = false
                        } else {
                            isError = true
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    isError = isError,
                    keyboardOptions = KeyboardOptions.Default.copy(
                        keyboardType = KeyboardType.Number
                    ),
                    placeholder = { Text("Enter IP Address") },
                    trailingIcon = {
                        if (isError) {
                            Icon(Icons.Default.Warning, contentDescription = "Error", tint = MaterialTheme.colorScheme.error)
                        }
                    }
                )

                // Add Button in Dialog
                Button(
                    onClick = {
                        if (ipAddress.matches(Regex("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"))) {
                            onAddDevice(ipAddress)
                            onDismiss()
                        } else {
                            isError = true
                        }
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 16.dp)
                ) {
                    Text("Add Device")
                }
            }
        }
    }
}

@Preview
@Composable
fun Prev()
{
    DeviceListScreen()
}
