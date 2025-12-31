# Simple HTTP Server using PowerShell
# Run this to start the web demo

$port = 8000
$path = Get-Location

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Product Recommendation Web Demo Server" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Directory: $path" -ForegroundColor Yellow
Write-Host "Server: http://localhost:$port" -ForegroundColor Green
Write-Host "Web App: http://localhost:$port/web/index.html" -ForegroundColor Green
Write-Host ""
Write-Host "Opening browser..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Open browser
Start-Process "http://localhost:$port/web/index.html"

# Start HTTP Listener
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")
$listener.Start()

Write-Host "Server is running..." -ForegroundColor Green
Write-Host ""

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        # Get requested file path
        $urlPath = $request.Url.LocalPath
        if ($urlPath -eq '/') {
            $urlPath = '/web/index.html'
        }
        
        $filePath = Join-Path $path $urlPath.TrimStart('/')
        
        # Check if file exists
        if (Test-Path $filePath -PathType Leaf) {
            # Read file
            $content = [System.IO.File]::ReadAllBytes($filePath)
            
            # Set content type
            $extension = [System.IO.Path]::GetExtension($filePath)
            $contentType = switch ($extension) {
                '.html' { 'text/html; charset=utf-8' }
                '.css'  { 'text/css; charset=utf-8' }
                '.js'   { 'application/javascript; charset=utf-8' }
                '.json' { 'application/json; charset=utf-8' }
                '.csv'  { 'text/csv; charset=utf-8' }
                '.png'  { 'image/png' }
                '.jpg'  { 'image/jpeg' }
                '.gif'  { 'image/gif' }
                default { 'text/plain; charset=utf-8' }
            }
            
            $response.ContentType = $contentType
            $response.ContentLength64 = $content.Length
            $response.StatusCode = 200
            $response.OutputStream.Write($content, 0, $content.Length)
            
            Write-Host "200 OK: $urlPath" -ForegroundColor Green
        }
        else {
            # File not found
            $responseString = "404 - File Not Found: $urlPath"
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($responseString)
            $response.ContentLength64 = $buffer.Length
            $response.StatusCode = 404
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
            
            Write-Host "404 Not Found: $urlPath" -ForegroundColor Red
        }
        
        $response.Close()
    }
}
finally {
    $listener.Stop()
    Write-Host ""
    Write-Host "Server stopped." -ForegroundColor Yellow
}
