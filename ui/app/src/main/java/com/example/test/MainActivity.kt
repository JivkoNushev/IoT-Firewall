package com.example.test

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.collection.mutableObjectIntMapOf
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.tooling.preview.Preview
import com.example.test.ui.theme.TestTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.text.input.KeyboardType
import androidx. compose. ui. platform. LocalContext
import com.example.test.page.DeviceList

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            WelcomeCard()
            Menu()
        }
    }
}

@Composable
fun WelcomeCard()
{
    Row {
        Text(text = "Welcome to Гвинпин Firewall!", color = MaterialTheme.colorScheme.primary)
    }
}

@Composable
fun Menu()
{
    var text by remember { mutableStateOf("") }
    var isError by remember { mutableStateOf(false) }
    val context = LocalContext.current

    Column(modifier = Modifier.fillMaxSize().padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center)
    {
        Text(text = "Enter your IP:",
            color = MaterialTheme.colorScheme.secondary,
            style = MaterialTheme.typography.bodyLarge,
            modifier = Modifier.padding(bottom = 8.dp)
        )

        TextField(
            value = text,
            onValueChange = { newText ->
                if (newText.matches(Regex("^([0-9]{1,3}\\.){0,3}[0-9]{0,3}$"))) {
                    text = newText
                    isError = false
                } else {
                    isError = true
                }
            },
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            singleLine = true,
            keyboardOptions = KeyboardOptions.Default.copy(
                keyboardType = KeyboardType.Number
            ),
            isError = isError,
            placeholder = { Text("e.g., 192.168.1.1") },
            trailingIcon = {
                if (isError) {
                    Icon(Icons.Default.Warning, contentDescription = "Error", tint = MaterialTheme.colorScheme.error)
                }
            }
        )

        Button(
            onClick = {
                // Validate the final input before submission
                if (text.matches(Regex("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"))) {
                    println("Valid IP Address: $text")

                    // Navigate to AnotherActivity
                    val intent = Intent(context, DeviceList::class.java)
                    intent.putExtra("IP_ADDRESS", text) // Pass the IP address to the new activity
                    context.startActivity(intent)
                } else {
                    println("Invalid IP Address")
                    isError = true
                }
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Submit")
        }


    }
}


@Preview
@Composable
fun PrevWelc()
{
    WelcomeCard()
    Menu()
}




