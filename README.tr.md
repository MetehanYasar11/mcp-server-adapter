# MCP Vision Adapter

<p align="center">
  <img src="https://img.shields.io/badge/YOLOv8-Powered-blue" alt="YOLOv8 Powered"/>
  <img src="https://img.shields.io/badge/REST%20API-Ready-green" alt="REST API Ready"/>
  <img src="https://img.shields.io/badge/VS%20Code%20Copilot-Agent%20Mode-orange" alt="VS Code Copilot Agent Mode"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License"/>
</p>

**MCP Vision Adapter**: Ultralytics YOLOv8 tabanlı, REST/STDIO destekli, VS Code Copilot Agent Mode ile tam entegre, modern ve açık kaynak bir görsel algı platformu.

---

## 🚀 Öne Çıkan Özellikler

- **Ultralytics YOLOv8 Entegrasyonu:** Hızlı ve doğru nesne tespiti, segmentasyon ve pose tahmini.
- **REST & STDIO API:** Hem HTTP/REST hem de stdio üzerinden kolay entegrasyon.
- **Web UI ile Model Takibi:** Dahili Streamlit arayüzü ile modelleri yükle, değiştir, yönet ve canlı sonuçları gör.
- **VS Code Copilot Agent Mode:** VS Code ile doğal entegrasyon, otomatik testler ve kod asistanı desteği.
- **Docker & Compose ile Kolay Kurulum:** Tek komutla tüm servisleri ayağa kaldır.
- **Tamamen Açık Kaynak & MIT Lisanslı:** Kurumsal ve bireysel kullanıma uygun, özgürce geliştirilebilir.
- **Test Kapsamı:** Pytest ile uçtan uca testler, örnek test görselleri ve otomasyon.
- **Video & Görüntü Desteği:** Video dosyalarında zaman dilimi veya kare bazlı analiz.
- **Model Hot-Swap:** Çalışan serviste model dosyasını kolayca değiştir.
- **Kapsamlı API:** Kolayca genişletilebilir endpoint yapısı.

---

## 🚦 Hızlı Başlangıç

### Docker Compose (YOLOv8 + Adapter)
```powershell
docker-compose up --build
```

- YOLOv8 service: [http://localhost:8080](http://localhost:8080)
- Adapter: [http://localhost:3000](http://localhost:3000)

#### YOLOv8 Servisini Test Et
```powershell
curl -F file=@test.jpg http://localhost:8080/detect
```

#### Adapter'ı Test Et (YOLO'ya proxy)
```powershell
Invoke-RestMethod -Uri "http://localhost:3000/execute" -Method Post -ContentType "application/json" -Body '{"tool":"detect_objects","input":{"image_path":"test.jpg"}}'
```

### STDIO Modu
```
python -m mcp_vision_adapter.main
```

### HTTP/SSE Modu
```
uvicorn mcp_vision_adapter.main:app --port 3000
```

---

## 🦾 YOLOv8 Microservice

Tüm detaylar ve gelişmiş kullanım için [`yolov8_service/README.md`](yolov8_service/README.md) dosyasına bakın.

**Model klasörünü bağla:**
```powershell
docker run -v ${PWD}/models:/weights ...
```
Varsayılan ağırlık dosyası: `/weights/yolov8n.pt`

---

## 🧩 VS Code MCP Entegrasyonu

Örnek `.vscode/mcp.json`:
```jsonc
{
  "servers": {
    "vision-http": {
      "type": "http",
      "url": "http://127.0.0.1:3000"
    },
    "vision-stdio": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mcp_vision_adapter.main"]
    }
  }
}
```

---

## 🧪 Testler

```powershell
pip install fastapi uvicorn pytest
pytest -q
```

Testler:
- `test_service_detect.py`: YOLOv8 servisi (doğrudan)
- `test_adapter_proxy.py`: Adapter → YOLOv8 servisi
- `test_stdio_exec.py`, `test_exec_env.py`: STDIO ve env testleri
- Tüm testler otomatik ve uçtan uca

---

## 📝 Notlar

- Video için `start`/`end` (örn: `?start=2s&end=5s`) veya `frame` parametrelerini kullanabilirsin.
- `manual_result` veya `MANUAL_RESULT` ayarlı değilse ve adapter TTY'de çalışmıyorsa, placeholder döner.

---

### ⚠️ Port Çakışması

Eğer Uvicorn 3000 portu meşgulse, önceki süreci durdur (CTRL-C) veya `--port 3001` ile başlatıp `mcp.json`'u güncelle.

---

## 🌍 Açık Kaynak ve Lisans

Bu proje MIT lisansı ile açık kaynak olarak sunulmaktadır. Katkılarınızı bekliyoruz!

---

## Güvenlik ve Gizlilik

- Projede herhangi bir gizli anahtar, parola veya erişim token'ı bulunmamaktadır.
- GITHUB_PERSONAL_ACCESS_TOKEN gibi örnekler sadece dokümantasyon ve test ortamı içindir, lütfen kendi anahtarınızı kullanırken dikkatli olun.
