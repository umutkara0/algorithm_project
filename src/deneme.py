from sentence_transformers import SentenceTransformer, util

# Model yükle (Türkçe destekli, hızlı ve küçük bir model)
# model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Synonym map yerine "soru temaları"
temalar = {
    "yaş": ["Yaşınız kaç?", "Doğum yılınız nedir?", "Kaç yaşındasınız?"],
    "gelir": ["Aylık geliriniz nedir?", "Maaş aralığınız nedir?", "Gelir durumunuz nedir?"],
    "evlilik": ["Medeni durumunuz nedir?", "Evli misiniz?", "Bekar mısınız?"],
    "askerlik": ["Askerlik yaptınız mı?", "Askerlik durumunuz nedir?", "Askerlikten muaf mısınız?"],
    "cinsiyet": ["Cinsiyetiniz nedir?", "Kendinizi hangi cinsiyette tanımlıyorsunuz?", "Doğumda atanmış cinsiyetiniz nedir?"],
    "eğitim": ["Eğitim düzeyiniz nedir?", "Hangi okuldan mezun oldunuz?", "En son hangi eğitimi aldınız?"],
    "meslek": ["Mesleğiniz nedir?", "Hangi sektörde çalışıyorsunuz?", "İşiniz nedir?"],
    "şehir": ["Hangi şehirde yaşıyorsunuz?", "İkamet ettiğiniz şehir nedir?", "Yaşadığınız şehir neresi?"],
    "ülke": ["Hangi ülkede yaşıyorsunuz?", "Vatandaşı olduğunuz ülke nedir?", "Şu anda hangi ülkedesiniz?"],
    "din": ["Dini inancınız nedir?", "Bir dine mensup musunuz?", "İnanç sisteminiz nedir?"],
    "etnik_kimlik": ["Etnik kökeniniz nedir?", "Kendinizi hangi etnik gruba ait hissediyorsunuz?", "Etnik kimliğinizi nasıl tanımlarsınız?"],
    "dil": ["Ana diliniz nedir?", "Hangi dilleri konuşuyorsunuz?", "Evde hangi dili konuşuyorsunuz?"],
    "çocuk": ["Çocuğunuz var mı?", "Kaç çocuğunuz var?", "Çocuk sahibi olmayı düşünüyor musunuz?"],
    "hayvan": ["Evcil hayvanınız var mı?", "Hangi hayvanları besliyorsunuz?", "Hayvan sever misiniz?"],
    "sigara": ["Sigara kullanıyor musunuz?", "Ne sıklıkla sigara içersiniz?", "Sigara içme alışkanlığınız var mı?"],
    "alkol": ["Alkol tüketiyor musunuz?", "Ne sıklıkla alkol alırsınız?", "Alkol kullanım durumunuz nedir?"],
    "uyku": ["Günde kaç saat uyursunuz?", "Uyku düzeniniz nasıl?", "Uykusuzluk problemi yaşıyor musunuz?"],
    "spor": ["Spor yapıyor musunuz?", "Hangi sporu yapıyorsunuz?", "Ne sıklıkla spor yaparsınız?"],
    "diyet": ["Diyet yapıyor musunuz?", "Beslenme alışkanlıklarınız nelerdir?", "Sağlıklı beslenmeye dikkat eder misiniz?"],
    "sosyal_medya": ["Hangi sosyal medya platformlarını kullanıyorsunuz?", "Günde ne kadar sosyal medya kullanıyorsunuz?", "Sosyal medya ile ilişkiniz nasıl?"],
    "internet": ["İnterneti ne amaçla kullanıyorsunuz?", "Günde kaç saat internettesiniz?", "İnternet alışkanlıklarınız nelerdir?"],
    "cep_telefonu": ["Ne marka telefon kullanıyorsunuz?", "Telefonunuzu ne sıklıkla değiştirirsiniz?", "Telefon kullanım süreniz nedir?"],
    "tatil": ["Yılda kaç kez tatile çıkarsınız?", "En son ne zaman tatile gittiniz?", "Tatil tercihiniz nedir?"],
    "yurt_dışı": ["Yurt dışına çıktınız mı?", "Hangi ülkelere gittiniz?", "Yurt dışı seyahat sıklığınız nedir?"],
    "trafik": ["Araç kullanıyor musunuz?", "Günde ne kadar süre trafikte kalıyorsunuz?", "Toplu taşıma mı özel araç mı kullanırsınız?"],
    "okuma": ["Kitap okur musunuz?", "Ayda kaç kitap okursunuz?", "En son hangi kitabı okudunuz?"],
    "film": ["Film izlemeyi sever misiniz?", "En son hangi filmi izlediniz?", "Hangi film türlerini seversiniz?"],
    "müzik": ["Hangi müzik türlerini seversiniz?", "Günde ne kadar müzik dinlersiniz?", "En sevdiğiniz sanatçı kim?"],
    "oyun": ["Video oyunu oynar mısınız?", "Hangi oyunları oynuyorsunuz?", "Günde kaç saat oyun oynarsınız?"],
    "psikoloji": ["Kendinizi mutlu hissediyor musunuz?", "Anksiyete yaşıyor musunuz?", "Psikolojik destek aldınız mı?"],
    "hobiler": ["Hobileriniz nelerdir?", "Boş zamanlarınızı nasıl değerlendirirsiniz?", "Yeni hobi edinir misiniz?"],
    "alışveriş": ["Online alışveriş yapar mısınız?", "En çok ne satın alırsınız?", "Alışverişe ayırdığınız bütçe nedir?"],
    "marka": ["Marka tercihleriniz var mı?", "Sadık olduğunuz markalar hangileri?", "Marka mı kalite mi sizin için önemli?"],
    "moda": ["Modayı takip eder misiniz?", "Kıyafet alışverişini nereden yaparsınız?", "Moda sizin için ne kadar önemli?"],
    "sağlık": ["Genel sağlık durumunuz nasıl?", "Son 1 yılda doktora gittiniz mi?", "Kronik hastalığınız var mı?"],
    "ilaç": ["Düzenli kullandığınız ilaç var mı?", "Reçetesiz ilaç kullanır mısınız?", "İlaç kullanma sıklığınız nedir?"],
    "kronik_hastalık": ["Herhangi bir kronik hastalığınız var mı?", "Tedavi görüyor musunuz?", "Sağlık geçmişinizde önemli bir hastalık var mı?"],
    "sigorta": ["Sağlık sigortanız var mı?", "Hangi sigorta şirketindensiniz?", "Özel mi devlet sigortası mı kullanıyorsunuz?"],
    "trafik_cezası": ["Hiç trafik cezası aldınız mı?", "En son ne zaman ceza yediniz?", "Ceza aldığınızda ne hissediyorsunuz?"],
    "ehliyet": ["Ehliyetiniz var mı?", "Hangi sınıf ehliyete sahipsiniz?", "Ne zamandan beri araç kullanıyorsunuz?"],
    "ulaşım": ["Toplu taşıma mı özel araç mı kullanırsınız?", "En sık kullandığınız ulaşım aracı nedir?", "Ulaşımda karşılaştığınız sorunlar nelerdir?"],
    "iklim": ["İklim değişikliği sizi endişelendiriyor mu?", "Geri dönüşüm yapıyor musunuz?", "Çevre bilinciniz ne düzeyde?"],
    "enerji": ["Tasarruflu ürünler tercih eder misiniz?", "Elektrik faturanızı nasıl düşürüyorsunuz?", "Yenilenebilir enerjiye yatırım yapar mısınız?"],
    "gıda": ["Organik gıda tüketir misiniz?", "Market alışverişini nereden yaparsınız?", "Gıda güvenliği sizin için önemli mi?"],
    "kariyer": ["Kariyer hedefleriniz nelerdir?", "Mevcut işinizden memnun musunuz?", "Kariyer planı yapar mısınız?"],
    "motivasyon": ["Sizi ne motive eder?", "Başarının tanımı sizin için nedir?", "Kendinizi nasıl geliştirirsiniz?"],
    "zaman": ["Zaman yönetimi konusunda başarılı mısınız?", "Zamanınızı nasıl planlarsınız?", "En çok zaman harcadığınız şey nedir?"],
    "stres": ["Stresle başa çıkma yöntemleriniz nelerdir?", "Sık stres yaşar mısınız?", "Stresli anlarda ne yaparsınız?"],
    "teknoloji": ["Teknolojiye ilgili misiniz?", "Yeni teknolojileri takip eder misiniz?", "Hangi teknolojik ürünleri kullanıyorsunuz?"],
    "veri_güvenliği": ["Kişisel verilerinizin güvende olduğunu düşünüyor musunuz?", "Parolalarınızı nasıl saklarsınız?", "Veri ihlali yaşadınız mı?"],
    "finans": ["Bütçe planlaması yapar mısınız?", "Aylık giderlerinizi takip eder misiniz?", "Tasarruf yapıyor musunuz?"],
    "kripto": ["Kripto para yatırımınız var mı?", "Hangi coinleri takip ediyorsunuz?", "Kripto para riskli mi sizce?"],
    "yatırım": ["Yatırım yapıyor musunuz?", "Hangi yatırım araçlarını kullanıyorsunuz?", "Yatırım yaparken neye dikkat edersiniz?"],
    "borç": ["Kredi kartı borcunuz var mı?", "Borçlarınızı düzenli öder misiniz?", "Kredi kullanma sıklığınız nedir?"],
    "emeklilik": ["Emeklilik planınız var mı?", "Ne zaman emekli olmayı düşünüyorsunuz?", "Bireysel emeklilik sistemine katıldınız mı?"],
    "gönüllülük": ["Gönüllü faaliyetlerde bulunuyor musunuz?", "Hangi STK'lara destek veriyorsunuz?", "Sosyal sorumluluk projelerine katılır mısınız?"],
    "politik": ["Siyasi görüşünüzü paylaşır mısınız?", "Oy kullanıyor musunuz?", "Gündemi takip eder misiniz?"],
    "haber": ["Haberleri nereden takip ediyorsunuz?", "Günde kaç kez haber okursunuz?", "Haber kaynaklarına güveniyor musunuz?"],
    "sanat": ["Sanatla ilgileniyor musunuz?", "En son ne zaman müze gezdiniz?", "Sanat sizin için ne ifade ediyor?"],
    "dizi": ["Dizi izler misiniz?", "En sevdiğiniz dizi hangisi?", "Yeni dizileri takip eder misiniz?"],
    "standartlar": ["Kendi standartlarınıza göre mi yaşarsınız?", "Toplum baskısı hissediyor musunuz?", "Kendi değerleriniz nelerdir?"],
    "özgüven": ["Kendinize güvenir misiniz?", "Özgüvenli biri misiniz?", "Kendinizi ne zaman güçlü hissedersiniz?"],
    "kişilik": ["Kendinizi içe dönük mü yoksa dışa dönük mü tanımlarsınız?", "Kişilik tipiniz nedir?", "Sosyal ortamlarda rahat mısınız?"],
    "uyum": ["Yeni ortamlara kolay alışır mısınız?", "Değişime açık mısınız?", "Çevrenizle kolay uyum sağlar mısınız?"],
    "karar": ["Karar verirken neye göre hareket edersiniz?", "Karar almakta zorlanır mısınız?", "Planlı mısınız yoksa anlık mı yaşarsınız?"],
    "hafıza": ["Unutkan mısınız?", "Hatırlamak için not alır mısınız?", "Dijital ajanda kullanır mısınız?"],
    "öğrenme": ["Yeni şeyler öğrenmeyi sever misiniz?", "Hangi alanlarda kendinizi geliştiriyorsunuz?", "Online eğitim alır mısınız?"],
    "yazılım": ["Kodlama biliyor musunuz?", "Hangi yazılım dillerine aşinasınız?", "Yazılım alanında çalışmak ister misiniz?"],
    "girişimcilik": ["Girişimcilik fikriniz var mı?", "Hiç kendi işinizi kurmayı düşündünüz mü?", "Risk almaktan korkar mısınız?"],
    "zihinsel_sağlık": ["Zihinsel sağlığınıza önem verir misiniz?", "Meditasyon yapar mısınız?", "Zihinsel yorgunluk yaşar mısınız?"],
    "dinlenme": ["Nasıl dinlenirsiniz?", "Kendinize zaman ayırır mısınız?", "Hafta sonlarını nasıl geçirirsiniz?"],
    "sosyal_çevre": ["Arkadaş çevreniz geniş midir?", "Yeni insanlarla tanışmayı sever misiniz?", "Yakın arkadaşlarınızla ne sıklıkla görüşürsünüz?"],
    "iletişim": ["İletişim becerilerinize güvenir misiniz?", "İyi bir dinleyici misiniz?", "Konuşma sırasında kendinizi rahat hisseder misiniz?"],
    "empati": ["Empati kurar mısınız?", "Başkalarının duygularını anlayabilir misiniz?", "Duygusal zekânız gelişmiş midir?"],
    "yardımseverlik": ["İnsanlara yardım etmeyi sever misiniz?", "Sık sık yardım kampanyalarına katılır mısınız?", "Gönüllü çalışmalara ilginiz var mı?"]
}


# Yeni gelen bir soru
# yeni_soru = "Dizi izlemeyi sever misiniz?"

# # Her tema için ortalama embedding hesapla
# tema_embeddings = {}
# for tema, sorular in temalar.items():
#     embeddings = model.encode(sorular, convert_to_tensor=True)
#     tema_embeddings[tema] = embeddings.mean(dim=0)

# # Yeni sorunun embedding'i
# soru_embedding = model.encode(yeni_soru, convert_to_tensor=True)

# # Benzerlikleri hesapla
# benzerlikler = {}
# for tema, emb in tema_embeddings.items():
#     skor = util.cos_sim(soru_embedding, emb).item()
#     benzerlikler[tema] = skor

# # En benzer temayı bul
# en_benzer = max(benzerlikler, key=benzerlikler.get)

# print("Soru:", yeni_soru)
# print("En benzer tema:", en_benzer)
# print("Benzerlik skorları:", benzerlikler)