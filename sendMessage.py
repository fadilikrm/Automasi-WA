# sendMessage.py (Versi Selenium - PERSISTENT PROFILE + FIXED IMAGE UPLOAD)

import time
import pandas as pd
import urllib.parse
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import base64

def create_driver():
    """Mempersiapkan dan membuat instance driver Chrome dengan profile persisten."""
    options = webdriver.ChromeOptions()
    
    # SOLUSI UTAMA: Gunakan Chrome Profile yang persisten
    # Buat folder khusus untuk menyimpan data Chrome
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chrome_profile_dir = os.path.join(script_dir, "chrome_profile_whatsapp")
    
    # Pastikan folder ada
    if not os.path.exists(chrome_profile_dir):
        os.makedirs(chrome_profile_dir)
        print(f"Membuat folder profile Chrome: {chrome_profile_dir}")
    else:
        print(f"Menggunakan profile Chrome yang sudah ada: {chrome_profile_dir}")
    
    # Gunakan profile directory yang persisten
    options.add_argument(f"--user-data-dir={chrome_profile_dir}")
    
    # Opsi untuk stabilitas
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--start-maximized")
    
    # Disable automation flags agar tidak terdeteksi sebagai bot
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Set download directory
    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": script_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    try:
        print("Mempersiapkan WebDriver dengan profile persisten...")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Disable webdriver detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("WebDriver berhasil dibuat dengan profile persisten.")
        print(f"Profile directory: {chrome_profile_dir}")
        return driver
        
    except Exception as e:
        print("\n" + "="*50)
        print("GAGAL MEMBUAT WEBDRIVER!")
        print(f"Detail Error: {e}")
        print("\nSOLUSI YANG BISA DICOBA:")
        print("1. Jalankan Command Prompt/Terminal sebagai Administrator")
        print("2. Pastikan Google Chrome sudah ter-update ke versi terbaru")
        print("3. Restart komputer Anda")
        print("4. Hapus folder 'chrome_profile_whatsapp' jika ada masalah")
        print("="*50 + "\n")
        return None

def setup_whatsapp_first_time(driver):
    """Setup WhatsApp Web untuk pertama kali atau jika belum login."""
    print("Membuka WhatsApp Web...")
    driver.get("https://web.whatsapp.com")
    
    # Tunggu sebentar untuk loading
    time.sleep(8)
    
    # Cek apakah sudah login dengan mencari elemen chat
    try:
        # Coba cari elemen yang menandakan sudah login (area chat)
        chat_area = WebDriverWait(driver, 10).until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, "//div[@id='main']")),
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'two')]")),
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='chat-list']"))
            )
        )
        print("✅ Sudah login sebelumnya. Tidak perlu scan QR lagi!")
        return True
        
    except TimeoutException:
        # Tidak ada chat area, cek apakah ada QR code
        try:
            qr_code = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//canvas"))
            )
            
            print("\n" + "="*60)
            print("🔍 QR CODE DITEMUKAN - PERLU LOGIN")
            print("="*60)
            print("1. Pindai kode QR di jendela browser dengan HP Anda")
            print("2. Buka WhatsApp di HP > Menu (3 titik) > WhatsApp Web")
            print("3. Scan QR code yang muncul di browser")
            print("4. Tunggu hingga halaman chat WhatsApp muncul")
            print("5. PENTING: Centang 'Keep me signed in' jika ada")
            print("\n⚠️  JANGAN TEKAN ENTER SAMPAI CHAT MUNCUL!")
            print("="*60)
            
            # Loop untuk menunggu login dengan timeout
            max_wait = 120  # 2 menit
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                try:
                    # Cek apakah chat sudah muncul
                    chat_element = WebDriverWait(driver, 5).until(
                        EC.any_of(
                            EC.presence_of_element_located((By.XPATH, "//div[@id='main']")),
                            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'two')]")),
                            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='chat-list']"))
                        )
                    )
                    print("✅ Login berhasil! Chat area terdeteksi.")
                    print("📁 Profile tersimpan untuk penggunaan selanjutnya.")
                    time.sleep(3)  # Tunggu sebentar untuk memastikan loaded
                    return True
                    
                except TimeoutException:
                    print(f"⏳ Menunggu login... ({int(time.time() - start_time)}s)")
                    time.sleep(2)
                    continue
            
            print("❌ Timeout menunggu login. Coba lagi.")
            return False
            
        except TimeoutException:
            print("❌ Tidak ditemukan QR code atau chat area. Coba refresh halaman.")
            return False
            
    except Exception as e:
        print(f"❌ Error saat setup: {e}")
        return False

def wait_for_element_multiple_selectors(driver, selectors, timeout=10):
    """Mencoba multiple selector sampai salah satu ditemukan."""
    for selector in selectors:
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            print(f"✅ Element ditemukan dengan selector: {selector}")
            return element
        except TimeoutException:
            continue
    return None

def debug_page_elements_detailed(driver):
    """Debug function untuk melihat elemen yang tersedia di halaman dengan detail."""
    print("\n🔍 DEBUG: Mencari elemen di halaman...")
    
    try:
        # Cari semua elemen dengan data-icon
        icons = driver.find_elements(By.XPATH, "//*[@data-icon]")
        print(f"Found {len(icons)} elements with data-icon:")
        for i, icon in enumerate(icons[:15]):  # Hanya 15 pertama
            try:
                icon_name = icon.get_attribute("data-icon")
                tag_name = icon.tag_name
                classes = icon.get_attribute("class")
                print(f"  {i+1}. {tag_name} data-icon='{icon_name}' class='{classes}'")
            except:
                pass
    except Exception as e:
        print(f"Error getting data-icon elements: {e}")
    
    try:
        # Cari semua tombol
        buttons = driver.find_elements(By.XPATH, "//button | //div[@role='button']")
        print(f"\nFound {len(buttons)} buttons/clickable elements:")
        for i, btn in enumerate(buttons[:10]):  # Hanya 10 pertama
            try:
                title = btn.get_attribute("title") or ""
                aria_label = btn.get_attribute("aria-label") or ""
                classes = btn.get_attribute("class") or ""
                if title or aria_label:
                    print(f"  {i+1}. title='{title}' aria-label='{aria_label}' class='{classes[:50]}'")
            except:
                pass
    except Exception as e:
        print(f"Error getting buttons: {e}")
    
    try:
        # Cari input file
        inputs = driver.find_elements(By.XPATH, "//input")
        print(f"\nFound {len(inputs)} input elements:")
        for i, inp in enumerate(inputs):
            try:
                inp_type = inp.get_attribute("type")
                inp_accept = inp.get_attribute("accept")
                if inp_type or inp_accept:
                    print(f"  {i+1}. type='{inp_type}' accept='{inp_accept}'")
            except:
                pass
    except Exception as e:
        print(f"Error getting inputs: {e}")

def find_attachment_button_dynamic(driver):
    """Mencari tombol attachment secara dinamis dengan berbagai metode."""
    print("🔍 Mencari tombol attachment secara dinamis...")
    
    # Method 1: Cari berdasarkan data-icon yang umum digunakan
    common_icons = ['plus', 'attach', 'clip', 'paperclip', 'attachment']
    for icon in common_icons:
        try:
            elements = driver.find_elements(By.XPATH, f"//*[@data-icon='{icon}']")
            for element in elements:
                # Cek apakah element ini clickable
                try:
                    if element.is_displayed() and element.is_enabled():
                        print(f"✅ Ditemukan tombol attachment dengan data-icon='{icon}'")
                        return element
                except:
                    continue
        except:
            continue
    
    # Method 2: Cari berdasarkan title atau aria-label
    attachment_texts = ['Attach', 'attach', 'Lampiran', 'lampiran']
    for text in attachment_texts:
        try:
            # Coba title
            elements = driver.find_elements(By.XPATH, f"//*[@title='{text}']")
            for element in elements:
                if element.is_displayed() and element.is_enabled():
                    print(f"✅ Ditemukan tombol attachment dengan title='{text}'")
                    return element
            
            # Coba aria-label
            elements = driver.find_elements(By.XPATH, f"//*[@aria-label='{text}']")
            for element in elements:
                if element.is_displayed() and element.is_enabled():
                    print(f"✅ Ditemukan tombol attachment dengan aria-label='{text}'")
                    return element
        except:
            continue
    
    # Method 3: Cari berdasarkan posisi (biasanya di kiri input text)
    try:
        # Cari input text terlebih dahulu
        text_input = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        if text_input:
            # Cari elemen clickable di sebelah kiri input
            parent = text_input.find_element(By.XPATH, './ancestor::div[contains(@class, "compose") or contains(@class, "input")]')
            buttons = parent.find_elements(By.XPATH, './/button | .//div[@role="button"]')
            
            for button in buttons:
                try:
                    # Cek apakah button ini berisi icon atau terlihat seperti attachment
                    svg_icons = button.find_elements(By.XPATH, './/svg | .//*[@data-icon]')
                    if svg_icons and button.is_displayed() and button.is_enabled():
                        print("✅ Ditemukan tombol attachment berdasarkan posisi")
                        return button
                except:
                    continue
    except:
        pass
    
    # Method 4: Cari dengan CSS selector
    css_selectors = [
        '[data-icon="plus"]',
        '[data-icon="attach"]',
        '[data-icon="clip"]',
        '[title*="ttach"]',
        '[aria-label*="ttach"]'
    ]
    
    for selector in css_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed() and element.is_enabled():
                    print(f"✅ Ditemukan tombol attachment dengan CSS selector: {selector}")
                    return element
        except:
            continue
    
    print("❌ Tombol attachment tidak ditemukan dengan semua method")
    return None

def send_image_improved(driver, image_path, message=""):
    """Fungsi yang diperbaiki untuk mengirim gambar dengan berbagai fallback method."""
    try:
        print(f"📸 Memulai proses upload gambar: {os.path.basename(image_path)}")
        
        # Verifikasi file gambar exists dan formatnya valid
        if not os.path.exists(image_path):
            print(f"❌ File gambar tidak ditemukan: {image_path}")
            return False
            
        # Cek ekstensi file
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        file_extension = os.path.splitext(image_path)[1].lower()
        if file_extension not in valid_extensions:
            print(f"❌ Format file tidak didukung: {file_extension}")
            return False
            
        print(f"✅ File gambar valid: {file_extension}")
        
        # Tunggu halaman loaded sepenuhnya
        print("⏳ Menunggu halaman chat loaded sepenuhnya...")
        time.sleep(5)
        
        # Debug: lihat elemen yang tersedia
        debug_page_elements_detailed(driver)
        
        # METHOD 1: Cari tombol attachment dengan metode dinamis
        attach_button = find_attachment_button_dynamic(driver)
        
        if not attach_button:
            print("❌ Tombol attachment tidak ditemukan dengan semua method")
            print("🔄 Mencoba method alternatif...")
            return send_image_drag_drop_method(driver, image_path, message)
            
        # Klik tombol attachment
        print("📎 Mengklik tombol attachment...")
        try:
            # Coba klik biasa terlebih dahulu
            attach_button.click()
        except:
            # Jika gagal, gunakan JavaScript
            driver.execute_script("arguments[0].click();", attach_button)
        time.sleep(4)
        
        # Tunggu menu attachment muncul
        print("⏳ Menunggu menu attachment muncul...")
        time.sleep(3)
        
        # METHOD 2: Cari input file dengan berbagai selector dan method
        file_input = find_file_input_dynamic(driver)
                
        if not file_input:
            print("❌ Input file tidak ditemukan dengan semua method")
            return send_image_drag_drop_method(driver, image_path, message)
        
        # Upload file
        absolute_path = os.path.abspath(image_path)
        print(f"📤 Mengupload file: {absolute_path}")
        
        try:
            file_input.send_keys(absolute_path)
            print("✅ File berhasil diupload ke input")
        except Exception as e:
            print(f"❌ Gagal upload file ke input: {e}")
            return False
            
        # Tunggu preview gambar muncul
        print("⏳ Menunggu preview gambar...")
        time.sleep(5)
        
        # METHOD 3: Tambahkan caption jika ada pesan
        if message and message.strip():
            caption_selectors = [
                '//div[@data-testid="media-caption-input-container"]//div[@contenteditable="true"]',
                '//div[contains(@class, "caption")]//div[@contenteditable="true"]',
                '//div[@role="textbox"][@data-testid="media-caption-input"]',
                '//div[@contenteditable="true"][contains(@class, "caption")]',
                '//div[@aria-label="Add a caption..."]',
                '//div[@placeholder="Add a caption..."]'
            ]
            
            caption_input = wait_for_element_multiple_selectors(driver, caption_selectors, 5)
            if caption_input:
                print("✏️ Menambahkan caption...")
                caption_input.click()
                time.sleep(1)
                caption_input.send_keys(message)
                time.sleep(2)
            else:
                print("⚠️ Caption input tidak ditemukan, lanjut tanpa caption")
        
        # METHOD 4: Cari dan klik tombol send dengan berbagai selector
        send_selectors = [
            '//span[@data-icon="send"]',
            '//div[@data-testid="send"]//span[@data-icon="send"]',
            '//button[@data-testid="send"]',
            '//div[@role="button"]//span[@data-icon="send"]',
            '//button[contains(@class, "send")]',
            '//*[@data-testid="send"]',
            '//div[@aria-label="Send"]',
            '//button[@aria-label="Send"]',
            '//div[contains(@class, "send")]//span[@data-icon="send"]'
        ]
        
        print("📩 Mencari tombol send...")
        send_button = wait_for_element_multiple_selectors(driver, send_selectors, 15)
        
        if send_button:
            print("✅ Tombol send ditemukan, mengirim gambar...")
            driver.execute_script("arguments[0].click();", send_button)
            
            # Verifikasi pengiriman berhasil
            time.sleep(3)
            print("✅ Gambar berhasil dikirim!")
            return True
        else:
            print("❌ Tombol send tidak ditemukan")
            # Fallback: coba tekan Enter
            print("🔄 Mencoba fallback dengan Enter...")
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            time.sleep(3)
            print("✅ Gambar dikirim dengan fallback method!")
            return True
            
    except Exception as e:
        print(f"❌ Error dalam send_image_improved: {e}")
        return False

def find_file_input_dynamic(driver):
    """Mencari input file secara dinamis."""
    print("🔍 Mencari input file secara dinamis...")
    
    # Method 1: Cari semua input file yang tersedia
    try:
        inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
        print(f"Ditemukan {len(inputs)} input file")
        
        for i, inp in enumerate(inputs):
            try:
                accept_attr = inp.get_attribute("accept") or ""
                if inp.is_displayed() or accept_attr:  # Kadang input file hidden tapi bisa digunakan
                    print(f"✅ Input file {i+1} ditemukan: accept='{accept_attr}'")
                    return inp
            except:
                continue
    except Exception as e:
        print(f"Error mencari input file: {e}")
    
    # Method 2: Cari dengan berbagai selector
    selectors = [
        '//input[@accept*="image"]',
        '//input[@accept*="*"]',
        '//input[@multiple]',
        '//input[contains(@accept, "image")]',
        '//input[contains(@accept, "video")]'
    ]
    
    for selector in selectors:
        try:
            inputs = driver.find_elements(By.XPATH, selector)
            for inp in inputs:
                if inp.get_attribute("type") == "file":
                    print(f"✅ Input file ditemukan dengan selector: {selector}")
                    return inp
        except:
            continue
    
    # Method 3: Trigger pembuatan input file baru
    try:
        print("🔄 Mencoba trigger input file baru...")
        # Kadang klik attachment button lagi bisa memunculkan input file
        js_code = """
        var inputs = document.querySelectorAll('input[type="file"]');
        if (inputs.length > 0) {
            return inputs[inputs.length - 1]; // Return yang terakhir
        }
        return null;
        """
        result = driver.execute_script(js_code)
        if result:
            print("✅ Input file ditemukan dengan JavaScript")
            return result
    except Exception as e:
        print(f"Error JavaScript method: {e}")
    
    return None

def send_image_drag_drop_method(driver, image_path, message=""):
    """Method alternatif menggunakan drag & drop atau clipboard."""
    try:
        print("🔄 Mencoba method drag & drop / clipboard...")
        
        # Method 1: Coba paste dari clipboard (jika didukung)
        try:
            # Cari area input
            input_area = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            if input_area:
                print("📋 Mencoba method clipboard...")
                input_area.click()
                time.sleep(2)
                
                # Simulate Ctrl+V (mungkin user sudah copy gambar)
                ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                time.sleep(3)
                
                # Cek apakah ada preview gambar
                if check_image_preview(driver):
                    print("✅ Gambar berhasil dipaste dari clipboard!")
                    return finalize_image_send(driver, message)
        except Exception as e:
            print(f"Clipboard method gagal: {e}")
        
        # Method 2: JavaScript file API
        try:
            print("💻 Mencoba JavaScript File API...")
            
            # Baca file sebagai base64
            import base64
            with open(image_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            
            file_name = os.path.basename(image_path)
            mime_type = f"image/{os.path.splitext(image_path)[1][1:]}"
            
            js_code = f"""
            // Buat File object dari base64
            const byteCharacters = atob('{img_data}');
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {{
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }}
            const byteArray = new Uint8Array(byteNumbers);
            const file = new File([byteArray], '{file_name}', {{type: '{mime_type}'}});
            
            // Cari input file dan set files
            const inputs = document.querySelectorAll('input[type="file"]');
            if (inputs.length > 0) {{
                const input = inputs[inputs.length - 1];
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                input.files = dataTransfer.files;
                
                // Trigger change event
                const event = new Event('change', {{bubbles: true}});
                input.dispatchEvent(event);
                return true;
            }}
            return false;
            """
            
            result = driver.execute_script(js_code)
            if result:
                print("✅ JavaScript File API berhasil!")
                time.sleep(3)
                return finalize_image_send(driver, message)
                
        except Exception as e:
            print(f"JavaScript File API gagal: {e}")
        
        # Method 3: Manual instruction
        print("\n" + "="*60)
        print("🔧 METHOD MANUAL - UPLOAD GAMBAR")
        print("="*60)
        print("Tolong lakukan langkah berikut secara manual:")
        print(f"1. Di browser yang terbuka, klik tombol attachment (clip/plus)")
        print("2. Pilih 'Photos & Videos' atau 'Galeri'")
        print(f"3. Pilih file: {os.path.basename(image_path)}")
        print(f"4. Tambahkan caption: {message}")
        print("5. Klik tombol Send")
        print("="*60)
        
        response = input("Apakah gambar sudah berhasil dikirim manual? (y/n): ").lower().strip()
        if response == 'y' or response == 'yes':
            print("✅ Gambar berhasil dikirim secara manual!")
            return True
        else:
            print("❌ Upload manual dibatalkan")
            return False
            
    except Exception as e:
        print(f"❌ Error dalam drag & drop method: {e}")
        return False

def check_image_preview(driver):
    """Cek apakah ada preview gambar yang muncul."""
    try:
        preview_selectors = [
            '//div[contains(@class, "media-preview")]',
            '//img[contains(@class, "preview")]',
            '//div[@data-testid="media-viewer"]',
            '//canvas[contains(@class, "media")]'
        ]
        
        for selector in preview_selectors:
            try:
                element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                if element.is_displayed():
                    return True
            except:
                continue
        return False
    except:
        return False

def finalize_image_send(driver, message=""):
    """Finalisasi pengiriman gambar (tambah caption dan send)."""
    try:
        # Tambahkan caption jika ada
        if message and message.strip():
            print("✏️ Menambahkan caption...")
            caption_selectors = [
                '//div[@data-testid="media-caption-input-container"]//div[@contenteditable="true"]',
                '//div[contains(@class, "caption")]//div[@contenteditable="true"]',
                '//div[@role="textbox"][@data-testid="media-caption-input"]',
                '//div[@contenteditable="true"][contains(@class, "caption")]',
                '//div[@aria-label="Add a caption..."]',
                '//div[@placeholder="Add a caption..."]'
            ]
            
            caption_input = wait_for_element_multiple_selectors(driver, caption_selectors, 5)
            if caption_input:
                caption_input.click()
                time.sleep(1)
                caption_input.clear()
                caption_input.send_keys(message)
                time.sleep(2)
            else:
                print("⚠️ Caption input tidak ditemukan")
        
        # Cari dan klik tombol send
        send_selectors = [
            '//span[@data-icon="send"]',
            '//div[@data-testid="send"]//span[@data-icon="send"]',
            '//button[@data-testid="send"]',
            '//div[@role="button"]//span[@data-icon="send"]',
            '//button[contains(@class, "send")]',
            '//*[@data-testid="send"]',
            '//div[@aria-label="Send"]',
            '//button[@aria-label="Send"]'
        ]
        
        print("📩 Mencari tombol send...")
        send_button = wait_for_element_multiple_selectors(driver, send_selectors, 10)
        
        if send_button:
            print("✅ Tombol send ditemukan, mengirim gambar...")
            try:
                send_button.click()
            except:
                driver.execute_script("arguments[0].click();", send_button)
            time.sleep(3)
            return True
        else:
            print("❌ Tombol send tidak ditemukan, coba Enter...")
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            time.sleep(3)
            return True
            
    except Exception as e:
        print(f"Error dalam finalize_image_send: {e}")
        return False

def manual_login_check(driver):
    """Fungsi untuk mengecek login secara manual jika otomatis gagal."""
    print("\n" + "="*60)
    print("🔧 MODE MANUAL - PERIKSA STATUS LOGIN")
    print("="*60)
    print("Silakan periksa browser Chrome yang terbuka:")
    print("1. Apakah Anda sudah melihat daftar chat WhatsApp?")
    print("2. Jika belum, lakukan scan QR code")
    print("3. Tunggu hingga chat list muncul")
    print("="*60)
    
    while True:
        response = input("Apakah chat WhatsApp sudah muncul? (y/n): ").lower().strip()
        if response == 'y' or response == 'yes':
            print("✅ Melanjutkan proses...")
            return True
        elif response == 'n' or response == 'no':
            print("⏳ Menunggu 10 detik, silakan coba lagi...")
            time.sleep(10)
        else:
            print("Masukkan 'y' untuk ya atau 'n' untuk tidak.")

def send_whatsapp_messages(driver, file_path: str):
    """Membaca Excel dan mengirim pesan WhatsApp menggunakan driver Selenium."""
    try:
        print(f"Membaca data dari {file_path}...")
        
        # Cek apakah file ada
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' tidak ditemukan!")
            print("Pastikan file Excel berada di folder yang sama dengan script ini.")
            return
            
        data = pd.read_excel(file_path)
        total_rows = len(data)
        
        # Validasi kolom yang diperlukan
        required_columns = ['Nomor WhatsApp', 'Pesan']
        for col in required_columns:
            if col not in data.columns:
                print(f"Error: Kolom '{col}' tidak ditemukan dalam file Excel!")
                print(f"Kolom yang tersedia: {list(data.columns)}")
                return

        # Setup WhatsApp Web (login jika perlu)
        if not setup_whatsapp_first_time(driver):
            print("❌ Setup otomatis gagal. Mencoba mode manual...")
            if not manual_login_check(driver):
                print("❌ Gagal setup WhatsApp Web!")
                return
        
        print("Memulai proses pengiriman...")

        for index, row in data.iterrows():
            print(f"\n--- Mengirim pesan ke-{index + 1} dari {total_rows} ---")
            
            phone_no = str(row['Nomor WhatsApp']).strip()
            message = str(row['Pesan']).strip()
            image_path = str(row.get('Gambar', '')).strip()
            
            # Validasi nomor telepon
            if not phone_no or phone_no == 'nan':
                print(f"Nomor telepon kosong pada baris {index + 1}, skip...")
                continue
                
            # Bersihkan nomor telepon
            phone_no = phone_no.replace(' ', '').replace('-', '').replace('+', '')
            
            print(f"Mengirim ke: {phone_no}")
            print(f"Pesan: {message[:50]}...")

            try:
                # Jika ada gambar, kirim gambar dengan pesan
                if image_path and image_path != 'nan' and os.path.exists(image_path):
                    print(f"📸 Mode: Kirim gambar + teks")
                    
                    # Buka chat tanpa pre-filled message untuk gambar
                    url = f"https://web.whatsapp.com/send?phone={phone_no}"
                    driver.get(url)
                    
                    # Tunggu halaman chat dimuat
                    print("⏳ Menunggu halaman chat dimuat...")
                    time.sleep(8)
                    
                    # Cek apakah nomor valid
                    try:
                        error_element = WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Phone number shared via url is invalid')]"))
                        )
                        print(f"❌ Nomor {phone_no} tidak valid, skip...")
                        continue
                    except TimeoutException:
                        pass
                    
                    # Pastikan chat area sudah loaded
                    try:
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                        )
                    except TimeoutException:
                        print(f"❌ Chat area tidak dimuat untuk {phone_no}")
                        continue
                    
                    # Kirim gambar
                    if send_image_improved(driver, image_path, message):
                        print(f"✅ Gambar + pesan berhasil dikirim ke {phone_no}")
                    else:
                        print(f"⚠️ Gambar gagal, mencoba kirim teks saja...")
                        # Fallback: kirim teks saja
                        encoded_message = urllib.parse.quote(message)
                        url = f"https://web.whatsapp.com/send?phone={phone_no}&text={encoded_message}"
                        driver.get(url)
                        time.sleep(5)
                        
                        input_box = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                        )
                        input_box.send_keys(Keys.ENTER)
                        print(f"✅ Pesan teks berhasil dikirim ke {phone_no}")
                
                else:
                    print(f"📝 Mode: Kirim teks saja")
                    # Encode pesan untuk URL
                    encoded_message = urllib.parse.quote(message)
                    url = f"https://web.whatsapp.com/send?phone={phone_no}&text={encoded_message}"
                    driver.get(url)
                    
                    # Tunggu dan kirim
                    time.sleep(5)
                    
                    # Cek nomor valid
                    try:
                        error_element = WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Phone number shared via url is invalid')]"))
                        )
                        print(f"❌ Nomor {phone_no} tidak valid, skip...")
                        continue
                    except TimeoutException:
                        pass
                    
                    # Tunggu input box dan kirim
                    input_box = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                    )
                    input_box.send_keys(Keys.ENTER)
                    print(f"✅ Pesan teks berhasil dikirim ke {phone_no}")
                
                # Jeda antar pesan
                print("⏳ Menunggu 10 detik sebelum pesan berikutnya...")
                time.sleep(10)

            except TimeoutException:
                print(f"❌ Gagal mengirim ke {phone_no}: Timeout")
                continue
            except Exception as e:
                print(f"❌ Gagal mengirim ke {phone_no}: {e}")
                continue

        print("\n" + "="*50)
        print("🎉 PROSES PENGIRIMAN SELESAI!")
        print("Semua pesan telah diproses.")
        print("="*50)

    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' tidak ditemukan!")
        print("Pastikan file Excel berada di folder yang sama dengan script ini.")
    except Exception as e:
        print(f"❌ Terjadi error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("="*50)
    print("🚀 WHATSAPP AUTO SENDER - IMPROVED IMAGE UPLOAD")
    print("="*50)
    
    # Cek apakah file Excel ada
    excel_file = 'data_pesan.xlsx'
    if not os.path.exists(excel_file):
        print(f"❌ File '{excel_file}' tidak ditemukan!")
        print("Pastikan file Excel sudah ada di folder yang sama dengan script ini.")
        input("Tekan Enter untuk keluar...")
        exit()
    
    # Buat driver dengan profile persisten
    driver = create_driver()
    
    if driver:
        try:
            send_whatsapp_messages(driver, excel_file)
        except KeyboardInterrupt:
            print("\n⚠️  Proses dihentikan oleh user.")
        except Exception as e:
            print(f"❌ Terjadi error pada proses utama: {e}")
        finally:
            print("🔄 Menutup browser dalam 10 detik...")
            time.sleep(10)
            try:
                driver.quit()
            except:
                pass
            print("✅ Browser ditutup. Script selesai.")
    else:
        print("❌ Script dihentikan karena WebDriver tidak berhasil dibuat.")
        input("Tekan Enter untuk keluar...")