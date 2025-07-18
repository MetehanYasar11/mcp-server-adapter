# MCP Vision Adapter - N8N Compatible

Bu proje, **Model Context Protocol (MCP)** ve **n8n** ile uyumlu bir görüntü işleme adapter'ıdır. YOLO tabanlı nesne tespiti ve Ultralytics CLI komutlarını çalıştırmak için geliştirilmiştir.

## 🌟 Özellikler

- ✅ **N8N MCP Client Tool** ile tamamen uyumlu
- ✅ **Server-Sent Events (SSE)** protokolü
- ✅ **YOLO nesne tespiti** görüntü/video dosyalarında 
- ✅ **Ultralytics CLI** komutları desteği
- ✅ **Health monitoring** ve durum kontrolü
- ✅ **Docker** ile kolay deployment

## 🚀 Hızlı Başlangıç

### Docker ile Çalıştırma

```bash
# Tüm servisleri başlat
docker-compose up --build

# Sadece adapter servisini başlat
docker-compose up --build adapter
```

### Manuel Çalıştırma

```bash
# Node.js bağımlılıklarını yükle
cd mcp_vision_adapter
npm install

# Serveri başlat
npm start
```

## 🔧 Konfigürasyon

### Ortam Değişkenleri

- `YOLO_SERVICE_URL`: YOLO servisinin URL'i (varsayılan: `http://localhost:8080`)
- `PORT`: Adapter servisinin portu (varsayılan: `3000`)

### N8N MCP Client Tool Ayarları

1. N8N'de **MCP Client Tool** node'unu ekleyin
2. **Server URL** olarak ayarlayın: `http://localhost:3000/sse`
3. **Transport** olarak **SSE** seçin

## 📡 API Endpoints

### SSE (Server-Sent Events) - N8N için

- **GET** `/sse` - SSE bağlantısı kurar
- **POST** `/messages` - MCP mesajlarını işler

### Health Check

- **GET** `/health` - Servis durumu kontrolü

### Legacy Endpoints

- **GET** `/manifest` - Tool tanımlarını döner

## 🛠️ Available Tools

### 1. detect_objects

Görüntü veya video dosyasında nesne tespiti yapar.

**Parametreler:**
- `image_path` (string, gerekli): Görüntü/video dosyası yolu
- `manual_result` (string, opsiyonel): Manuel sonuç override

**Örnek kullanım:**
```javascript
{
  "tool": "detect_objects",
  "input": {
    "image_path": "/app/test.jpg"
  }
}
```

### 2. yolo_cli

Ultralytics YOLO CLI komutlarını çalıştırır.

**Parametreler:**
- `args` (string, gerekli): YOLO CLI argümanları

**Örnek kullanım:**
```javascript
{
  "tool": "yolo_cli", 
  "input": {
    "args": "predict model=yolov8n.pt source=test.jpg"
  }
}
```

## 🔄 Servis Yapısı

```
mcp-server-adapter/
├── docker-compose.yml          # Ana compose dosyası
├── Dockerfile.adapter          # Adapter için Dockerfile
├── mcp_vision_adapter/
│   ├── vision-mcp-server-sse.js # Ana SSE server
│   ├── package.json            # Node.js bağımlılıkları
│   └── main.py                 # Legacy Python implementasyonu
└── yolov8_service/             # YOLO service
```

## 🐳 Docker Services

### yolo service
- **Container:** `yolov8`
- **Ports:** `8080:8080`, `8501:8501`
- **Health Check:** `http://localhost:8080/health`

### adapter service  
- **Container:** `mcp-vision-adapter`
- **Port:** `3000:3000`
- **Health Check:** `http://localhost:3000/health`
- **Depends on:** `yolo`

## 🔍 Troubleshooting

### Servis Durumu Kontrolü

```bash
# Health check
curl http://localhost:3000/health

# Active sessions kontrolü
curl http://localhost:3000/health | jq '.activeSessions'

# YOLO service kontrolü  
curl http://localhost:8080/health
```

### Log Kontrolü

```bash
# Container logları
docker-compose logs adapter
docker-compose logs yolo

# Real-time log takibi
docker-compose logs -f adapter
```

### N8N Bağlantı Problemleri

1. **SSE URL'ini kontrol edin:** `http://localhost:3000/sse`
2. **Transport tipini kontrol edin:** SSE olmalı
3. **Network connectivity:** Docker network ayarlarını kontrol edin
4. **Health check:** `/health` endpoint'i çalışıyor mu kontrol edin

## 🚦 Development

### Geliştirme Modu

```bash
cd mcp_vision_adapter
npm run dev  # nodemon ile otomatik restart
```

### Test Dosyaları

- `test.jpg` - Test görüntüsü
- Container içinde `/app/test.jpg` olarak mount edilir

## 📚 Kaynaklar

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [N8N MCP Client Tool Documentation](https://docs.n8n.io/)
- [Ultralytics YOLO Documentation](https://docs.ultralytics.com/)

## 📄 License

MIT License - Detaylar için LICENSE dosyasına bakın.
