package com.alesoftware.podridascoring

import android.annotation.SuppressLint
import android.os.Bundle
import android.util.Log
import android.view.View
import android.webkit.ConsoleMessage
import android.webkit.WebChromeClient
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import kotlinx.coroutines.*

class MainActivity : AppCompatActivity() {
    
    private lateinit var webView: WebView
    private lateinit var loadingProgress: ProgressBar
    private lateinit var loadingText: TextView
    private var flaskJob: Job? = null
    private val serverPort = 5000
    private val serverUrl = "http://127.0.0.1:$serverPort"
    private val TAG = "PodridaScoring"
    
    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        Log.d(TAG, "onCreate: Iniciando aplicación")
        
        // Inicializar vistas
        webView = findViewById(R.id.webView)
        loadingProgress = findViewById(R.id.loadingProgress)
        loadingText = findViewById(R.id.loadingText)
        
        // Configurar WebView
        setupWebView()
        
        // Configurar manejo de botón atrás
        setupBackPressedHandler()
        
        // Inicializar Python y arrancar Flask
        startFlaskServer()
    }
    
    @SuppressLint("SetJavaScriptEnabled")
    private fun setupWebView() {
        Log.d(TAG, "setupWebView: Configurando WebView")
        
        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            // databaseEnabled is deprecated, DOM storage is sufficient
            allowFileAccess = true
            allowContentAccess = true
            setSupportZoom(true)
            builtInZoomControls = false
            displayZoomControls = false
            loadWithOverviewMode = true
            useWideViewPort = true
        }
        
        // Cliente para manejar navegación
        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView, url: String): Boolean {
                Log.d(TAG, "WebViewClient: Navegando a $url")
                view.loadUrl(url)
                return true
            }
            
            override fun onPageFinished(view: WebView, url: String) {
                super.onPageFinished(view, url)
                Log.d(TAG, "WebViewClient: Página cargada: $url")
                hideLoading()
            }
            
            override fun onReceivedError(
                view: WebView,
                request: WebResourceRequest,
                error: WebResourceError
            ) {
                super.onReceivedError(view, request, error)
                Log.e(TAG, "WebViewClient: Error ${error.errorCode}: ${error.description} en ${request.url}")
                
                // Reintentar carga después de un delay
                if (request.url.toString() == serverUrl) {
                    showLoading("Error de conexión. Reintentando...")
                    webView.postDelayed({
                        Log.d(TAG, "Reintentando cargar Flask...")
                        webView.loadUrl(serverUrl)
                    }, 2000)
                }
            }
        }
        
        // Cliente para consola y títulos
        webView.webChromeClient = object : WebChromeClient() {
            override fun onConsoleMessage(consoleMessage: ConsoleMessage): Boolean {
                Log.d(TAG, "Console: ${consoleMessage.message()}")
                return true
            }
            
            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                super.onProgressChanged(view, newProgress)
                if (newProgress == 100) {
                    Log.d(TAG, "WebChromeClient: Página completamente cargada")
                }
            }
        }
    }
    
    private fun startFlaskServer() {
        Log.d(TAG, "startFlaskServer: Iniciando servidor Flask")
        
        // Inicializar Python si no está inicializado
        if (!Python.isStarted()) {
            Log.d(TAG, "Iniciando Python...")
            Python.start(AndroidPlatform(this))
        }
        
        showLoading("Iniciando servidor Flask...")
        
        // Ejecutar Flask en un thread separado
        flaskJob = CoroutineScope(Dispatchers.IO).launch {
            try {
                val py = Python.getInstance()
                Log.d(TAG, "Python inicializado correctamente")
                
                withContext(Dispatchers.Main) {
                    showLoading("Cargando módulos Python...")
                }
                
                // Ejecutar código Python directamente
                Log.d(TAG, "Configurando entorno Android...")
                
                // Programar carga del WebView para dar tiempo a que arranque el servidor
                withContext(Dispatchers.Main) {
                    showLoading("Arrancando servidor local...")
                    Log.d(TAG, "Programando carga de WebView en 3s...")
                    webView.postDelayed({
                        loadFlaskApp()
                    }, 3000)
                }
                
                // Ejecutar Flask (bloqueante) - Iniciar inmediatamente
                Log.d(TAG, "Ejecutando servidor Flask...")
                val runAndroid = py.getModule("run_android")
                runAndroid.callAttr("start_server")
                
            } catch (e: Exception) {
                Log.e(TAG, "Error al iniciar servidor Flask", e)
                withContext(Dispatchers.Main) {
                    val message = "Error al iniciar servidor: ${e.message}"
                    Toast.makeText(
                        this@MainActivity,
                        message,
                        Toast.LENGTH_LONG
                    ).show()
                    showLoading("Error: ${e.message}")
                }
            }
        }
    }
    
    private fun loadFlaskApp() {
        Log.d(TAG, "loadFlaskApp: Cargando $serverUrl")
        webView.loadUrl(serverUrl)
        showLoading("Conectando al servidor...")
    }
    
    private fun showLoading(message: String) {
        runOnUiThread {
            Log.d(TAG, "showLoading: $message")
            loadingText.text = message
            loadingProgress.visibility = View.VISIBLE
            loadingText.visibility = View.VISIBLE
            webView.visibility = View.GONE
        }
    }
    
    private fun hideLoading() {
        runOnUiThread {
            Log.d(TAG, "hideLoading: Ocultando pantalla de carga")
            loadingProgress.visibility = View.GONE
            loadingText.visibility = View.GONE
            webView.visibility = View.VISIBLE
        }
    }
    
    private fun setupBackPressedHandler() {
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                // Manejar navegación hacia atrás en WebView
                if (webView.canGoBack()) {
                    Log.d(TAG, "onBackPressed: Navegando atrás en WebView")
                    webView.goBack()
                } else {
                    Log.d(TAG, "onBackPressed: Saliendo de la aplicación")
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                }
            }
        })
    }
    
    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, "onDestroy: Finalizando aplicación")
        // Cancelar el job de Flask
        flaskJob?.cancel()
    }
    
    override fun onPause() {
        super.onPause()
        Log.d(TAG, "onPause: Aplicación en pausa")
        webView.onPause()
    }
    
    override fun onResume() {
        super.onResume()
        Log.d(TAG, "onResume: Aplicación reanudada")
        webView.onResume()
    }
}
