# 🚀 QUICKSTART - MCP Vision Adapter for N8N

Bu rehber size **5 dakikada** MCP Vision Adapter'ı N8N ile çalıştırmayı gösterir.

## ⚡ 3 Adımda Başla

### 1️⃣ Repo'yu İndir ve Çalıştır
```bash
git clone https://github.com/MetehanYasar11/mcp-server-adapter.git
cd mcp-server-adapter
docker-compose up -d
```

### 2️⃣ N8N'i MCP Network'e Bağla
```bash
# Mevcut N8N container'ını MCP network'e bağla
docker network connect mcp_network n8n

# Veya N8N'i yeniden başlat (önerilen)
docker stop n8n
docker run -d \
  --name n8n \
  --network mcp_network \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

### 3️⃣ N8N'de MCP Client Tool Ayarı
1. N8N workflow'unda **"MCP Client Tool"** node'u ekle
2. Ayarları yapılandır:
   - **Connection Type**: `Server-Sent Events (SSE)`
   - **SSE Endpoint**: `http://mcp-vision-adapter:3000/sse`
   - **Authentication**: `None`

## ✅ Test Et

### N8N Workflow Test
```json
{
  "tool": "detect_objects",
  "input": {
    "image_path": "test.jpg",
    "confidence": 0.5
  }
}
```

### Manual Test (opsiyonel)
```bash
# Health check
curl http://localhost:3000/health

# Object detection test
curl -X POST http://localhost:3000/execute \
  -H "Content-Type: application/json" \
  -d '{"tool":"detect_objects","input":{"image_path":"test.jpg"}}'
```

## 🎯 İlk YOLO Workflow'u

1. **Trigger Node** ekle (Manual/Webhook)
2. **MCP Client Tool** node'u ekle ve yukarıdaki ayarları yap
3. **Tool** olarak `detect_objects` seç
4. **Input** olarak:
   ```json
   {
     "image_path": "test.jpg",
     "confidence": 0.5,
     "model": "yolov8n.pt"
   }
   ```
5. Workflow'u çalıştır! 🎉

## 🛠️ Sorun Giderme

### Container'lar çalışıyor mu?
```bash
docker ps
```
`yolov8` ve `mcp-vision-adapter` container'ları **UP** durumunda olmalı.

### Network bağlantısı var mı?
```bash
docker exec n8n curl http://mcp-vision-adapter:3000/health
```
`{"status":"healthy"}` döner.

### YOLO Service çalışıyor mu?
```bash
curl http://localhost:8080/docs
```
FastAPI dokümantasyonu açılmalı.

## 🎨 Web UI

- **YOLO Streamlit UI**: http://localhost:8501
- **YOLO API Docs**: http://localhost:8080/docs  
- **MCP Health Check**: http://localhost:3000/health

## 📚 Daha Fazla

- **Tam dokümantasyon**: [README.md](README.md)
- **YOLO Service detayları**: [yolov8_service/README.md](yolov8_service/README.md)
- **Custom model yükleme**: `models/` klasörüne `.pt` dosyası ekle

---

**🎉 Tebrikler!** Artık N8N workflow'larınızda YOLO object detection kullanabilirsiniz.
docker network connect mcp_network <n8n-container-name>
```

Sonra N8N'de: `http://mcp-vision-adapter:3000/sse`

---
**Ready to use with N8N MCP Client Tool! 🚀**
