from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
import random

# Arayüz Tasarımı
Builder.load_string('''
<SadeTop>:
    size: 30, 30
    canvas:
        Color:
            rgb: self.renk
        Ellipse:
            pos: self.pos
            size: self.size

<SadeKafaOyuncu>:
    size: self.mevcut_boyut
    canvas:
        Color:
            rgb: self.renk
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10,]

<SadeKafaOyun>:
    oyuncu_bir: mavi_kafa_id
    rakip_bot: rakip_id

    canvas:
        Color:
            rgb: (0, 0.2, 0) 
        Rectangle:
            pos: self.pos
            size: self.size
        
        Color:
            rgb: (1, 1, 1) 
        Line:
            rectangle: (0, 0, self.width, self.height)
            width: 2
        Line:
            points: [0, self.center_y, self.width, self.center_y]
            width: 1

    BoxLayout:
        orientation: 'vertical'
        size_hint: (None, None)
        size: (200, 100)
        pos: 20, root.height - 110
        Label:
            id: skor_label
            text: "SKOR: " + str(root.skor_degeri)
            font_size: 30
            halign: 'left'
            color: (1, 1, 0, 1)
        Label:
            id: rekor_label
            text: "REKOR: " + str(root.en_yuksek_skor)
            font_size: 25
            halign: 'left'
            color: (1, 0.8, 0, 1)

    Button:
        id: durdur_btn
        text: "DURDUR" if root.oyun_aktif else "BASLAT"
        size: 120, 50
        pos: root.width - 140, root.height - 70
        background_color: (0.8, 0.2, 0.2, 1) if root.oyun_aktif else (0.2, 0.8, 0.2, 1)
        on_press: root.durum_degistir()

    SadeKafaOyuncu:
        id: mavi_kafa_id
        renk: (0.2, 0.6, 1, 1)
        center_x: root.center_x
        y: 40

    SadeKafaOyuncu:
        id: rakip_id
        renk: (1, 0.2, 0.2, 1)
        center_x: root.center_x
        top: root.top - 40

    Button:
        id: restart_btn
        text: "YENIDEN BASLA"
        size: 250, 80
        center: root.center
        opacity: 0
        disabled: True
        on_press: root.yeniden_baslat()
''')

class SadeTop(Widget):
    renk = ListProperty([1, 1, 0, 1])
    tip = StringProperty("normal")
    hiz_x = NumericProperty(7)
    hiz_y = NumericProperty(7)
    hiz = ReferenceListProperty(hiz_x, hiz_y)

    def hareket_et(self):
        self.pos = Vector(*self.hiz) + self.pos

class SadeKafaOyuncu(Widget):
    renk = ListProperty([1, 1, 1, 1])
    mevcut_boyut = ListProperty([110, 30])

class SadeKafaOyun(Widget):
    oyuncu_bir = ObjectProperty(None)
    rakip_bot = ObjectProperty(None)
    skor_degeri = NumericProperty(0)
    en_yuksek_skor = NumericProperty(0)
    toplar = ListProperty([])
    aktif_tuslar = set()
    oyun_aktif = True

    def __init__(self, **kwargs):
        super(SadeKafaOyun, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down, on_key_up=self._on_key_up)
        
        Clock.schedule_once(lambda dt: self.yeni_top_ekle(), 1)
        Clock.schedule_interval(self.yeni_top_ekle, 30.0)
        Clock.schedule_interval(self.kirmizi_top_ekle, 45.0)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down, on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.aktif_tuslar.add(keycode[1])
        return True

    def _on_key_up(self, keyboard, keycode):
        if keycode[1] in self.aktif_tuslar:
            self.aktif_tuslar.remove(keycode[1])
        return True

    def durum_degistir(self):
        self.oyun_aktif = not self.oyun_aktif

    def yeni_top_ekle(self, dt=0):
        if self.oyun_aktif:
            top = SadeTop(renk=[1, 1, 0, 1], tip="normal")
            top.center = self.center
            top.hiz = (random.choice([-7, 7]), random.choice([-7, 7]))
            self.add_widget(top)
            self.toplar.append(top)

    def kirmizi_top_ekle(self, dt=0):
        if self.oyun_aktif:
            for t in self.toplar:
                if t.tip == "ozel": return 
            
            top = SadeTop(renk=[1, 0, 0, 1], tip="ozel")
            top.center = self.center
            top.hiz = (random.choice([-10, 10]), random.choice([-10, 10]))
            self.add_widget(top)
            self.toplar.append(top)

    def boyutu_normale_dondur(self, dt):
        self.oyuncu_bir.mevcut_boyut = [110, 30]

    def yeniden_baslat(self):
        for top in self.toplar: self.remove_widget(top)
        self.toplar = []
        self.skor_degeri = 0
        self.oyun_aktif = True
        self.oyuncu_bir.mevcut_boyut = [110, 30]
        self.ids.skor_label.text = "SKOR: 0"
        self.ids.restart_btn.opacity = 0
        self.ids.restart_btn.disabled = True
        self.yeni_top_ekle()

    def update(self, dt):
        if not self.oyun_aktif: return

        if self.skor_degeri > self.en_yuksek_skor:
            self.en_yuksek_skor = self.skor_degeri

        # Dokunmatik Kontrol (Telefonda APK kurunca çalışması için)
        for touch in Window.touches.values():
            if touch.x < self.width / 2:
                if self.oyuncu_bir.x > 0: self.oyuncu_bir.x -= 18
            else:
                if self.oyuncu_bir.right < self.width: self.oyuncu_bir.x += 18

        # Klavye Kontrolü (PC testi için)
        if 'left' in self.aktif_tuslar and self.oyuncu_bir.x > 0:
            self.oyuncu_bir.x -= 18
        if 'right' in self.aktif_tuslar and self.oyuncu_bir.right < self.width:
            self.oyuncu_bir.x += 18

        if self.toplar:
            hedef = self.toplar[0]
            if self.rakip_bot.center_x < hedef.center_x: self.rakip_bot.x += 8
            else: self.rakip_bot.x -= 8

        for top in self.toplar[:]:
            top.hareket_et()

            if self.oyuncu_bir.collide_widget(top):
                top.hiz_y = abs(top.hiz_y)
                if top.tip == "ozel":
                    self.oyuncu_bir.mevcut_boyut = [220, 30]
                    Clock.unschedule(self.boyutu_normale_dondur)
                    Clock.schedule_once(self.boyutu_normale_dondur, 10.0)
                    self.remove_widget(top)
                    self.toplar.remove(top)
                    continue
                self.skor_degeri += 1
                
            if self.rakip_bot.collide_widget(top):
                top.hiz_y = -abs(top.hiz_y)

            if top.x < 0 or top.right > self.width: top.hiz_x *= -1
            
            if top.top > self.height:
                self.skor_degeri += 5
                if top.tip == "ozel":
                    self.remove_widget(top)
                    self.toplar.remove(top)
                else:
                    top.center = self.center
            
            if top.y < 0:
                if top.tip == "ozel":
                    self.oyuncu_bir.mevcut_boyut = [55, 30]
                    Clock.unschedule(self.boyutu_normale_dondur)
                    Clock.schedule_once(self.boyutu_normale_dondur, 10.0)
                    self.remove_widget(top)
                    self.toplar.remove(top)
                else:
                    top.center = self.center
                
                self.skor_degeri -= 3
                if self.skor_degeri <= -10:
                    self.oyun_aktif = False
                    self.ids.restart_btn.opacity = 1
                    self.ids.restart_btn.disabled = False

class SadeKafaApp(App):
    def build(self):
        oyun = SadeKafaOyun()
        Clock.schedule_interval(oyun.update, 1.0 / 60.0)
        return oyun

if __name__ == '__main__':
    SadeKafaApp().run()
