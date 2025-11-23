import sys
import pandas as pd
from DrissionPage import ChromiumPage, ChromiumOptions
from loguru import logger
from datetime import datetime
import os
import json
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class SelectorAPIHandler(BaseHTTPRequestHandler):
    """API handler untuk menerima selector dari browser extension"""

    def __init__(self, scraper_instance, *args, **kwargs):
        self.scraper = scraper_instance
        super().__init__(*args, **kwargs)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode('utf-8'))

            # Proses selector yang diterima
            selector = data.get('selector', '')
            action = data.get('action', 'check')

            result = self.scraper.process_selector_from_extension(selector, action)

            response = {
                'status': 'success',
                'result': result,
                'timestamp': datetime.now().isoformat()
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            error_response = {
                'status': 'error',
                'message': str(e)
            }

            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())

    def log_message(self, format, *args):
        # Disable default HTTP logging
        pass

class EnhancedProScraper:
    def __init__(self):
        logger.info("Menginisialisasi Enhanced ProScraper...")

        # Mengatur koneksi ke Chrome yang sudah terbuka (Port 9222)
        co = ChromiumOptions()
        co.set_local_port(9222) # Connect ke browser manual

        try:
            self.page = ChromiumPage(addr_or_opts=co)
            logger.success("Berhasil terhubung ke Browser Chrome!")
        except Exception as e:
            logger.critical(f"Gagal terhubung ke Chrome. Pastikan Chrome jalan di port 9222. Error: {e}")
            sys.exit(1)

        # Storage untuk hasil scraping
        self.scraped_data = {}
        self.server_thread = None
        self.api_server = None

        # Start API server untuk menerima data dari extension
        self.start_api_server()

    def start_api_server(self):
        """Start HTTP server untuk komunikasi dengan browser extension"""
        def handler(*args, **kwargs):
            SelectorAPIHandler(self, *args, **kwargs)

        self.api_server = HTTPServer(('localhost', 8888), handler)
        self.server_thread = threading.Thread(target=self.api_server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

        logger.info("🌐 API Server started on http://localhost:8888")
        logger.info("📡 Extension dapat mengirim selector ke scraper ini")

    def process_selector_from_extension(self, selector, action='check'):
        """Memproses selector yang dikirim dari browser extension"""
        logger.info(f"🔌 Menerima selector dari extension: {selector}")

        if action == 'check':
            return self.check_element_with_info(selector)
        elif action == 'scrape':
            return self.quick_scrape(selector)
        else:
            return self.check_element_with_info(selector)

    def check_element_with_info(self, selector):
        """Enhanced check dengan info detail"""
        try:
            elems = self.page.eles(selector)
            count = len(elems)

            if count > 0:
                # Gather info about elements
                element_info = []
                for i, el in enumerate(elems[:5]):  # Max 5 elements
                    info = {
                        'index': i,
                        'tag': el.tag,
                        'text': el.text[:100] if el.text else '',
                        'attributes': {}
                    }

                    # Get some common attributes
                    try:
                        info['attributes']['class'] = el.attr('class')
                        info['attributes']['id'] = el.attr('id')
                        info['attributes']['href'] = el.attr('href')
                    except:
                        pass

                    element_info.append(info)

                # Highlight elements
                for el in elems:
                    self.page.run_js("""
                        arguments[0].style.outline = '3px solid #ff4757';
                        arguments[0].style.outlineOffset = '2px';
                        arguments[0].style.backgroundColor = 'rgba(255, 71, 87, 0.1)';

                        // Remove highlight after 3 seconds
                        setTimeout(() => {
                            arguments[0].style.outline = '';
                            arguments[0].style.outlineOffset = '';
                            arguments[0].style.backgroundColor = '';
                        }, 3000);
                    """, el)

                result = {
                    'found': True,
                    'count': count,
                    'selector': selector,
                    'elements': element_info,
                    'message': f'✅ Ditemukan {count} elemen'
                }

                logger.success(f"✅ Extension selector check: {count} elemen ditemukan")
                return result

            else:
                result = {
                    'found': False,
                    'count': 0,
                    'selector': selector,
                    'elements': [],
                    'message': f'❌ Elemen tidak ditemukan: {selector}'
                }

                logger.warning(f"❌ Extension selector not found: {selector}")
                return result

        except Exception as e:
            result = {
                'found': False,
                'error': str(e),
                'message': f'❌ Error: {str(e)}'
            }
            logger.error(f"Error checking extension selector: {e}")
            return result

    def quick_scrape(self, selector):
        """Quick scrape dari extension"""
        try:
            elems = self.page.eles(selector)
            if not elems:
                return {'success': False, 'message': 'Tidak ada elemen ditemukan'}

            data = []
            for el in elems:
                text_val = el.text
                if text_val:
                    data.append(text_val)

            # Store data temporarily
            key = f"scrape_{datetime.now().strftime('%H%M%S')}"
            self.scraped_data[key] = data

            result = {
                'success': True,
                'count': len(data),
                'data': data[:10],  # Preview 10 items
                'key': key,
                'message': f'✅ Berhasil scrape {len(data)} data'
            }

            logger.success(f"✅ Extension quick scrape: {len(data)} data")
            return result

        except Exception as e:
            result = {
                'success': False,
                'error': str(e),
                'message': f'❌ Gagal scrape: {str(e)}'
            }
            logger.error(f"Error in extension quick scrape: {e}")
            return result

    def check_element(self, selector):
        """Memeriksa apakah elemen ada di halaman saat ini"""
        try:
            elems = self.page.eles(selector)
            count = len(elems)
            if count > 0:
                logger.info(f"Ditemukan {count} elemen dengan selector: '{selector}'")

                # Visual Feedback: Highlight element di browser
                for el in elems:
                    # Enhanced highlighting dengan animasi
                    self.page.run_js("""
                        arguments[0].style.transition = 'all 0.3s ease';
                        arguments[0].style.outline = '3px solid #ff4757';
                        arguments[0].style.outlineOffset = '2px';
                        arguments[0].style.backgroundColor = 'rgba(255, 71, 87, 0.1)';
                        arguments[0].style.transform = 'scale(1.02)';

                        setTimeout(() => {
                            arguments[0].style.outline = '';
                            arguments[0].style.outlineOffset = '';
                            arguments[0].style.backgroundColor = '';
                            arguments[0].style.transform = '';
                        }, 2000);
                    """, el)
                return True
            else:
                logger.warning(f"Elemen tidak ditemukan: {selector}")
                return False
        except Exception as e:
            logger.error(f"Error saat checking elemen: {e}")
            return False

    def extract_data(self, selector, key_name):
        """Ekstraksi data teks"""
        data_list = []
        try:
            # Mengambil semua elemen
            elems = self.page.eles(selector)

            if not elems:
                logger.error("Data kosong, tidak bisa di-scrape.")
                return None

            logger.info(f"Mulai ekstraksi {len(elems)} data...")

            for el in elems:
                # DrissionPage sangat pintar mengambil text (termasuk text tersembunyi di child)
                text_val = el.text
                if text_val:
                    data_list.append(text_val)

            logger.success(f"Berhasil mengambil {len(data_list)} baris data.")
            return data_list

        except Exception as e:
            logger.error(f"Gagal ekstraksi: {e}")
            return None

    def save_data(self, data, column_name, format_type):
        if not data:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not os.path.exists("results"):
            os.makedirs("results")

        df = pd.DataFrame(data, columns=[column_name])

        filename = f"results/scrape_{timestamp}"

        try:
            if format_type == 'csv':
                full_path = f"{filename}.csv"
                df.to_csv(full_path, index=False)
            elif format_type == 'excel':
                full_path = f"{filename}.xlsx"
                df.to_excel(full_path, index=False, engine='xlsxwriter')
            elif format_type == 'json':
                full_path = f"{filename}.json"
                df.to_json(full_path, orient='records', indent=4)

            logger.success(f"File tersimpan di: {full_path}")
        except Exception as e:
            logger.error(f"Gagal menyimpan file: {e}")

    def show_extension_data(self):
        """Menampilkan data yang telah dikumpulkan dari extension"""
        if not self.scraped_data:
            print("📭 Belum ada data dari extension")
            return

        print("\n" + "="*50)
        print("📊 DATA DARI EXTENSION")
        print("="*50)

        for key, data in self.scraped_data.items():
            print(f"\n🔑 Key: {key}")
            print(f"📈 Jumlah: {len(data)} data")
            print(f"📋 Preview: {data[:3]}")

        print(f"\n💾 Total data tersimpan: {len(self.scraped_data)} sets")

    def start_interactive_mode(self):
        print("\n" + "="*70)
        print("   🚀 ENHANCED DRISSIONPAGE SCRAPER WITH EXTENSION SUPPORT")
        print("   1. 🌐 Install browser extension untuk hover-to-select")
        print("   2. 🎯 Hover di browser untuk copy selector otomatis")
        print("   3. 📡 Extension akan mengirim ke scraper ini")
        print("   4. 🎮 Gunakan menu manual atau extension data")
        print("="*70 + "\n")

        print(f"🌐 Extension API: http://localhost:8888")
        print(f"📌 Status: {'✅ Active' if self.server_thread.is_alive() else '❌ Inactive'}")

        while True:
            current_url = self.page.url
            print(f"\n[📍 Active URL]: {current_url}")

            print("\n📋 Menu Options:")
            print("  check     - Test selector manual")
            print("  scrape    - Scrape data dengan selector manual")
            print("  extension - Tampilkan data dari extension")
            print("  export    - Export data dari extension")
            print("  exit      - Keluar")

            command = input("\nMenu pilihan: ").lower().strip()

            if command == "exit":
                logger.info("Menutup sesi...")
                if self.api_server:
                    self.api_server.shutdown()
                break

            elif command == "check":
                sel = input("Masukkan Selector/XPath: ")
                self.check_element(sel)

            elif command == "scrape":
                sel = input("Masukkan Selector target: ")

                if not self.check_element(sel):
                    continue

                col_name = input("Nama Kolom (Header Excel): ")
                result = self.extract_data(sel, col_name)

                if result:
                    print(f"Preview Data: {result[:3]}")
                    save_fmt = input("Simpan ke (csv/excel/json): ").lower()
                    if save_fmt in ['csv', 'excel', 'json']:
                        self.save_data(result, col_name, save_fmt)
                    else:
                        logger.warning("Format tidak dikenali, skip simpan.")

            elif command == "extension":
                self.show_extension_data()

            elif command == "export":
                if not self.scraped_data:
                    print("📭 Tidak ada data dari extension untuk diexport")
                    continue

                print("📊 Data yang tersedia:")
                for i, key in enumerate(self.scraped_data.keys(), 1):
                    print(f"  {i}. {key} ({len(self.scraped_data[key])} items)")

                try:
                    choice = input("Pilih nomor atau 'all' untuk export semua: ")
                    if choice.lower() == 'all':
                        # Export semua data
                        all_data = []
                        for data in self.scraped_data.values():
                            all_data.extend(data)

                        col_name = "exported_data"
                        result = self.extract_data_manual(all_data, col_name)
                        if result:
                            save_fmt = input("Simpan ke (csv/excel/json): ").lower()
                            if save_fmt in ['csv', 'excel', 'json']:
                                self.save_data(result, col_name, save_fmt)
                    else:
                        # Export data tertentu
                        key_list = list(self.scraped_data.keys())
                        index = int(choice) - 1
                        if 0 <= index < len(key_list):
                            key = key_list[index]
                            data = self.scraped_data[key]
                            col_name = f"extension_data_{key}"

                            save_fmt = input("Simpan ke (csv/excel/json): ").lower()
                            if save_fmt in ['csv', 'excel', 'json']:
                                self.save_data(data, col_name, save_fmt)
                except (ValueError, IndexError):
                    print("❌ Pilihan tidak valid")

    def extract_data_manual(self, data_list, column_name):
        """Extract data manual untuk export"""
        if not data_list:
            return None
        logger.info(f"Export {len(data_list)} data...")
        return data_list

if __name__ == "__main__":
    bot = EnhancedProScraper()
    bot.start_interactive_mode()