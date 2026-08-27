import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

function App() {
  const [oturumlar, setOturumlar] = useState([]);
  const [aktifOturum, setAktifOturum] = useState(null);
  const [mesajlar, setMesajlar] = useState([]);
  const [input, setInput] = useState('');
  const [yukleniyor, setYukleniyor] = useState(false);

  const karsilamaMesaji = { gonderen: 'şef', metin: 'Merhaba! Ben NutriCoach uygulamasının zeki beslenme koçuyum. Bugün sana nasıl yardımcı olabilirim?' };

  useEffect(() => {
    oturumlarıYukle();
  }, []);

  useEffect(() => {
    if (aktifOturum) {
      gecmisiYukle(aktifOturum);
    }
  }, [aktifOturum]);

  const oturumlarıYukle = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/oturumlar');
      const data = await response.json();
      if (data.oturumlar && data.oturumlar.length > 0) {
        setOturumlar(data.oturumlar);
        setAktifOturum(data.oturumlar[0].id);
      } else {
        yeniOturumAc();
      }
    } catch (error) { console.error('Oturumlar yüklenemedi:', error); }
  };

  const yeniOturumAc = async () => {
    // 🚀 DÜZELTME: Eğer şu an ekranda açık olan sohbet zaten boşsa (sadece şefin 1 mesajı varsa), boş yere yeni klasör açma!
    if (oturumlar.length > 0 && mesajlar.length <= 1) {
      return; 
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/yeni_oturum', { method: 'POST' });
      const data = await response.json();
      setOturumlar((prev) => [{ id: data.id, baslik: data.baslik }, ...prev]);
      setAktifOturum(data.id);
      setMesajlar([karsilamaMesaji]);
    } catch (error) { console.error('Yeni oturum açılamadı:', error); }
  };

  const gecmisiYukle = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/gecmis/${id}`);
      const data = await response.json();
      const eskiMesajlar = data.mesajlar.map(m => ({
        gonderen: m.rol === 'user' ? 'kullanici' : 'şef',
        metin: m.icerik
      }));
      setMesajlar([karsilamaMesaji, ...eskiMesajlar]);
    } catch (error) { console.error('Geçmiş yüklenemedi:', error); }
  };

  const oturumuSil = async (id) => {
    setOturumlar((prev) => prev.filter(o => o.id !== id));
    
    const aktifSiliyoruz = (aktifOturum === id);
    if (aktifSiliyoruz) {
       setAktifOturum(null);
       setMesajlar([]);
    }

    try {
      await fetch(`http://127.0.0.1:8000/temizle/${id}`, { method: 'DELETE' });
      if (aktifSiliyoruz) {
        oturumlarıYukle(); 
      }
    } catch (error) {
      console.error('Oturum silinemedi:', error);
    }
  };

  const mesajGonder = async () => {
    if (!input.trim() || !aktifOturum) return; 

    const yeniMesaj = { gonderen: 'kullanici', metin: input };
    setMesajlar((onceki) => [...onceki, yeniMesaj]);
    setInput('');
    setYukleniyor(true);

    try {
      const response = await fetch(`http://127.0.0.1:8000/sohbet/${aktifOturum}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mesaj: input }),
      });
      const data = await response.json();
      setMesajlar((onceki) => [...onceki, { gonderen: 'şef', metin: data.cevap }]);
      
      const listResponse = await fetch('http://127.0.0.1:8000/oturumlar');
      const listData = await listResponse.json();
      setOturumlar(listData.oturumlar);

    } catch (error) {
      setMesajlar((onceki) => [...onceki, { gonderen: 'şef', metin: 'Bağlantı hatası!' }]);
    } finally {
      setYukleniyor(false);
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh', backgroundColor: '#f4f6f8', fontFamily: '"Inter", "Segoe UI", sans-serif' }}>
      
      <div style={{ width: '280px', backgroundColor: '#ffffff', borderRight: '1px solid #e1e4e8', padding: '20px', display: 'flex', flexDirection: 'column' }}>
        <h2 style={{ color: '#2b2d42', margin: '0 0 5px 0', fontSize: '24px', fontWeight: '800' }}>NutriCoach</h2>
        <p style={{ color: '#8d99ae', margin: '0 0 25px 0', fontSize: '13px', fontWeight: '500' }}>AI Beslenme Koçu</p>
        
        <button 
          onClick={yeniOturumAc}
          style={{ width: '100%', padding: '12px', backgroundColor: '#2b2d42', color: 'white', border: 'none', borderRadius: '12px', cursor: 'pointer', fontSize: '14px', fontWeight: '600', marginBottom: '20px', boxShadow: '0 4px 15px rgba(43, 45, 66, 0.2)' }}
        >
          + Yeni Sohbet
        </button>

        <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {oturumlar.map(o => (
            <div 
              key={o.id} 
              style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 12px', backgroundColor: aktifOturum === o.id ? '#eef2f6' : 'transparent', borderRadius: '8px' }}
            >
              <div 
                onClick={() => setAktifOturum(o.id)}
                style={{ flex: 1, cursor: 'pointer', overflow: 'hidden' }}
              >
                <span style={{ fontSize: '14px', color: aktifOturum === o.id ? '#2b2d42' : '#5c6ac4', fontWeight: aktifOturum === o.id ? '600' : '400', whiteSpace: 'nowrap' }}>
                  💬 {o.baslik}
                </span>
              </div>
              
              <button 
                onClick={() => oturumuSil(o.id)} 
                style={{ background: 'none', border: 'none', color: '#ff4d4d', cursor: 'pointer', fontSize: '18px', padding: '0 5px', fontWeight: 'bold' }}
              >
                ×
              </button>
            </div>
          ))}
        </div>
      </div>

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: '40px', maxWidth: '900px', margin: '0 auto' }}>
        
        <div style={{ flex: 1, backgroundColor: '#ffffff', borderRadius: '24px', padding: '30px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '20px', boxShadow: '0 10px 40px rgba(0,0,0,0.04)' }}>
          {mesajlar.map((m, index) => (
            <div key={index} style={{ alignSelf: m.gonderen === 'kullanici' ? 'flex-end' : 'flex-start', backgroundColor: m.gonderen === 'kullanici' ? '#2b2d42' : '#f8f9fa', color: m.gonderen === 'kullanici' ? '#ffffff' : '#2b2d42', padding: '16px 24px', borderRadius: m.gonderen === 'kullanici' ? '24px 24px 4px 24px' : '24px 24px 24px 4px', maxWidth: '80%', lineHeight: '1.6', fontSize: '15px', boxShadow: m.gonderen === 'kullanici' ? '0 8px 20px rgba(43, 45, 66, 0.2)' : '0 4px 15px rgba(0,0,0,0.05)' }}>
              <ReactMarkdown>{m.metin}</ReactMarkdown>
            </div>
          ))}
          {yukleniyor && (
            <div style={{ alignSelf: 'flex-start', color: '#8d99ae', fontStyle: 'italic', fontSize: '14px', padding: '10px 20px' }}>NutriCoach yazıyor...</div>
          )}
        </div>

        <div style={{ display: 'flex', gap: '15px', marginTop: '20px' }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && mesajGonder()}
            placeholder="Antrenman nasıldı? Ne yemeliyiz?..."
            style={{ flex: 1, padding: '20px 25px', borderRadius: '20px', border: '1px solid #e1e4e8', outline: 'none', fontSize: '16px', backgroundColor: '#ffffff', boxShadow: '0 8px 25px rgba(0,0,0,0.02)', color: '#2b2d42' }}
            disabled={yukleniyor || !aktifOturum}
          />
          <button
            onClick={mesajGonder}
            style={{ padding: '0 30px', backgroundColor: '#2b2d42', color: 'white', border: 'none', borderRadius: '20px', cursor: 'pointer', fontSize: '16px', fontWeight: '600', boxShadow: '0 8px 25px rgba(43, 45, 66, 0.3)' }}
            disabled={yukleniyor || !aktifOturum}
          >
            Gönder
          </button>
        </div>
      </div>
      
    </div>
  );
}

export default App;